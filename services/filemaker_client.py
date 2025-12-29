import jpype
from jpype import JClass
import jaydebeapi
import pyodbc
import os
from typing import List, Dict, Any


class FileMakerClient:
    def __init__(
        self,
        dsn: str | None = None,
        host: str = "192.168.10.216",
        db: str = "Crown",
        user: str = "nexus",
        password: str | None = None,
    ):
        self.dsn = dsn
        self.host = host
        self.db = db
        self.user = user
        self.password = password

    # ============================================================
    # CONNECTIONS
    # ============================================================

    def connect(self):
        if self.dsn:
            try:
                conn = pyodbc.connect(self.dsn, timeout=5)
                return ("odbc", conn)
            except Exception:
                pass

        return self._connect_jdbc()

    def _connect_jdbc(self):
        jar_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "fmjdbc.jar")
        )
        jvm = jpype.getDefaultJVMPath()

        if not jpype.isJVMStarted():
            jpype.startJVM(jvm, f"-Djava.class.path={jar_path}")

        url = f"jdbc:filemaker://{self.host}:2399/{self.db}"

        conn = jaydebeapi.connect(
            "com.filemaker.jdbc.Driver",
            url,
            [self.user, self.password],
        )
        return ("jdbc", conn)

    def _jdbc_metadata(self, conn):
        jconn = conn.jconn if hasattr(conn, "jconn") else conn._conn
        return jconn.getMetaData()

    def fetch(self, layout, fields, where=None, limit=None):
        if not fields:
            raise ValueError("At least one field must be selected")

        quoted_fields = ", ".join(f'"{f}"' for f in fields)
        query = f'SELECT {quoted_fields} FROM "{layout}"'

        if where:
            query += f" WHERE {where}"

        if limit:
            query += f" FETCH FIRST {int(limit)} ROWS ONLY"

        engine, conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)

        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        return [
            {
                col: (
                    value.replace("\x00", "")
                    if isinstance(value, str)
                    else value
                )
                for col, value in zip(columns, row)
            }
            for row in rows
        ]

    # ============================================================
    # IDENTIFIER / VALUE NORMALIZATION
    # ============================================================

    def _quote_identifier(self, name: str) -> str:
        escaped = name.replace('"', '""')
        return f'"{escaped}"'

    def _normalize_sample(self, value, max_len=120):
        if value is None:
            return None

        if not isinstance(value, (str, int, float, bool)):
            value = str(value)

        if isinstance(value, str):
            value = (
                value
                .replace("\r\n", " ⏎ ")
                .replace("\n", " ⏎ ")
                .replace("\r", " ⏎ ")
            )
            return value[:max_len] + ("…" if len(value) > max_len else "")

        return value

    # ============================================================
    # SCHEMA DISCOVERY
    # ============================================================

    def list_tables(self) -> List[str]:
        engine, conn = self.connect()

        if engine == "jdbc":
            meta = self._jdbc_metadata(conn)
            rs = meta.getTables(None, None, None, ["TABLE"])

            tables = []
            while rs.next():
                tables.append(str(rs.getString("TABLE_NAME")))

            rs.close()
            return sorted(set(tables))

        query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_type = 'TABLE'
                ORDER BY table_name \
                """
        cols, rows = self._execute(query)
        return [r[0] for r in rows]

    def describe_table(self, table: str) -> List[Dict[str, Any]]:
        engine, conn = self.connect()

        if engine == "jdbc":
            meta = self._jdbc_metadata(conn)
            DatabaseMetaData = JClass("java.sql.DatabaseMetaData")

            rs = meta.getColumns(None, None, table, None)
            columns = []

            while rs.next():
                nullable_flag = rs.getInt("NULLABLE")

                columns.append({
                    "column_name": str(rs.getString("COLUMN_NAME")),
                    "data_type": str(rs.getString("TYPE_NAME")),
                    "character_maximum_length": rs.getInt("COLUMN_SIZE") or None,
                    "numeric_precision": None,
                    "numeric_scale": None,
                    "is_nullable": (
                        "YES"
                        if nullable_flag == DatabaseMetaData.columnNullable
                        else "NO"
                    ),
                    "ordinal_position": rs.getInt("ORDINAL_POSITION"),
                })

            rs.close()
            return columns

        query = f"""
            SELECT
                column_name,
                data_type,
                character_maximum_length,
                numeric_precision,
                numeric_scale,
                is_nullable,
                ordinal_position
            FROM information_schema.columns
            WHERE table_name = '{table}'
            ORDER BY ordinal_position
        """
        cols, rows = self._execute(query)
        return [dict(zip(cols, row)) for row in rows]

    # ============================================================
    # DATA SAMPLING
    # ============================================================

    def sample_column(self, table: str, column: str, limit: int = 5) -> List[Any]:
        q_table = self._quote_identifier(table)
        q_column = self._quote_identifier(column)

        query = f"""
            SELECT {q_column}
            FROM {q_table}
            WHERE {q_column} IS NOT NULL
            FETCH FIRST {int(limit)} ROWS ONLY
        """

        engine, conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)

        return [
            self._normalize_sample(row[0])
            for row in cursor.fetchall()
        ]

    # ============================================================
    # FIELD CLASSIFICATION
    # ============================================================

    def classify_field(self, table: str, col: Dict[str, Any]) -> str:
        name = col["column_name"]
        dtype = col["data_type"].upper()

        if dtype == "CONTAINER":
            return "container"

        if name.startswith("_"):
            return "internal_or_calculated"

        if name.lower().endswith("_ids"):
            return "calculated_relationship_keys"

        try:
            samples = self.sample_column(table, name, limit=3)
        except Exception:
            return "unsafe_to_sample"

        if any(isinstance(v, str) and "⏎" in v for v in samples):
            return "calculated_list"

        return "stored_data"

    # ============================================================
    # FIELD DESCRIPTION
    # ============================================================

    def describe_field(self, table: str, col: Dict[str, Any]) -> Dict[str, Any]:
        try:
            samples = self.sample_column(table, col["column_name"], limit=3)
        except Exception:
            samples = []

        return {
            "field": col["column_name"],
            "type": col["data_type"],
            "nullable": col["is_nullable"],
            "classification": self.classify_field(table, col),
            "example_values": samples,
        }

    # ============================================================
    # TABLE DICTIONARY
    # ============================================================

    def describe_table_fully(self, table: str) -> Dict[str, Any]:
        columns = self.describe_table(table)

        return {
            "table": table,
            "field_count": len(columns),
            "fields": [
                self.describe_field(table, col)
                for col in columns
            ],
        }

    def export_data_dictionary(self, tables: List[str] | None = None) -> Dict[str, Any]:
        if tables is None:
            tables = self.list_tables()

        return {
            "database": self.db,
            "tables": {
                table: self.describe_table_fully(table)
                for table in tables
            },
        }
