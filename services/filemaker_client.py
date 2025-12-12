import jpype
import jaydebeapi
import pyodbc
import os

class FileMakerClient:
    def __init__(self, dsn=None, host="192.168.10.216", db="Crown", user="nexus", password=None):
        self.dsn = dsn
        self.host = host
        self.db = db
        self.user = user
        self.password = password

    def connect(self):
        # Attempt ODBC first
        if self.dsn:
            try:
                conn = pyodbc.connect(self.dsn, timeout=5)
                return ("odbc", conn)
            except Exception:
                pass

        # JDBC fallback
        return self._connect_jdbc()

    def _connect_jdbc(self):
        jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "fmjdbc.jar"))
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

    def fetch(self, layout, fm_query=None):
        # FileMaker SQL style:
        query = f"SELECT * FROM {layout}"
        if fm_query:
            query += f" WHERE {fm_query}"

        engine, conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)

        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

        return [
            {col: (value.replace("\x00", "") if isinstance(value, str) else value)
             for col, value in zip(columns, row)}
            for row in rows
        ]
