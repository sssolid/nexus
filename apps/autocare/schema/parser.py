import re
from pathlib import Path

TABLE_RE = re.compile(
    r'CREATE TABLE\s+"(?P<table>\w+)"\s*\((?P<body>.*?)\);',
    re.S | re.I,
)

PK_RE = re.compile(r'PRIMARY KEY\s*\((?P<cols>[^)]+)\)', re.I)

FK_RE = re.compile(
    r'FOREIGN KEY\s*\("(?P<column>\w+)"\)\s+REFERENCES\s+"(?P<table>\w+)"\s*\("(?P<ref>\w+)"\)',
    re.I,
)

# Matches lines like:
# "Source" VARCHAR(10) DEFAULT NULL,
# "MakeID" INT NOT NULL,
# "LongDescription" varchar(200) NOT NULL,
# "SomeCol" character varying(50) NOT NULL,
# "SomeNum" numeric(10,2),
_COL_DEF_RE = re.compile(
    r'^\s*"(?P<name>[^"]+)"\s+'
    r'(?P<type>'
    r'(?:character\s+varying|double\s+precision|timestamp\s+with\s+time\s+zone|timestamp\s+without\s+time\s+zone|time\s+with\s+time\s+zone|time\s+without\s+time\s+zone|'
    r'varchar|char|text|int|integer|bigint|smallint|numeric|decimal|boolean|bool|date|timestamp|timestamptz|datetime)'
    r'(?:\(\s*\d+(?:\s*,\s*\d+)?\s*\))?'
    r')',
    re.I,
)


def _split_cols(cols: str) -> list[str]:
    return [c.strip().strip('"') for c in cols.split(",")]


def _parse_columns(body: str) -> dict[str, dict]:
    """
    Extract ONLY real column definitions.
    Ignore CONSTRAINT/PRIMARY KEY/FOREIGN KEY and any non-column lines.
    """
    columns: dict[str, dict] = {}

    for raw in body.splitlines():
        line = raw.strip().rstrip(",")

        # Skip blank lines
        if not line:
            continue

        # Skip table-level constraints
        u = line.upper()
        if u.startswith("PRIMARY KEY") or u.startswith("CONSTRAINT") or u.startswith("FOREIGN KEY"):
            continue

        m = _COL_DEF_RE.match(line)
        if not m:
            # Not a column definition line
            continue

        col_name = m.group("name")
        sql_type = m.group("type").strip()

        # Nullable unless explicitly NOT NULL
        nullable = "NOT NULL" not in u

        columns[col_name] = {"type": sql_type, "nullable": nullable}

    return columns


def parse_schema(sql_path: Path) -> dict:
    text = sql_path.read_text()
    tables = {}

    for match in TABLE_RE.finditer(text):
        table = match.group("table")
        body = match.group("body")

        columns = _parse_columns(body)

        pk_match = PK_RE.search(body)
        pk_cols = _split_cols(pk_match.group("cols")) if pk_match else []

        fks = []
        for fk in FK_RE.finditer(body):
            fks.append(
                {
                    "column": fk.group("column"),
                    "ref_table": fk.group("table"),
                    "ref_column": fk.group("ref"),
                }
            )

        tables[table] = {
            "columns": columns,
            "pk": pk_cols,
            "fks": fks,
        }

    return tables
