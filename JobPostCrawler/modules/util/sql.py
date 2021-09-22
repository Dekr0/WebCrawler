import pyodbc


_connectionParams = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",
    "SERVER": "localhost",
    "DATABASE": "Jobs",
    "UID": "SA",
    "PWD": "G12eT22Righ00t"
}

# String for connection of MS SQL server
_connectionString = ";".join([f"{param}={value}" for param, value in _connectionParams.items()])


class SQLUtil:

    def __init__(self, table):
        self.__conn = pyodbc.connect(_connectionString)
        self.__cursor = self.__conn.cursor()
        self.__table = table

    def hasTable(self):
        if self.__cursor.tables(table=self.__table, tableType='TABLE').fetchone():
            return True

        return False

    def createTable(self, fields):
        if self.hasTable():
            return

        nameTypePairs = []

        for columnName, columnType in fields.items():
            nameTypePairs.append(f"{columnName} {columnType}")

        columnDefinition = ", ".join(nameTypePairs)

        query = f"CREATE TABLE {self.__table} (" + columnDefinition + ")"

        self.__cursor.execute(query)
        self.__conn.commit()

    def hasRecord(self, conditions):
        columnList = []
        patternList = []

        for columnName, pattern in conditions.items():
            columnList.append(f"{columnName} LIKE (?)")
            patternList.append(f"%{pattern}%")

        selectors = " OR ".join(columnList)

        query = f"SELECT * FROM {_connectionParams['DATABASE']}.dbo.{self.__table} WHERE {selectors}"

        row = self.__cursor.execute(query, *patternList).fetchone()

        if row:
            return True

        return False

    def deleteRow(self, conditions):
        columnList = []
        patternList = []

        for columnName, pattern in conditions.items():
            columnList.append(f"{columnName} LIKE (?)")
            patternList.append(f"%{pattern}%")

        selectors = " OR ".join(columnList)

        query = f"DELETE FROM {_connectionParams['DATABASE']}.dbo.{self.__table} WHERE {selectors}"

        self.__cursor.execute(query, *patternList)
        self.__cursor.commit()

    def insertRow(self, fields):
        columnList = ", ".join(fields.keys())
        parameterizedString = ", ".join(["?" for i in range(len(fields))])


        query = f"INSERT INTO {_connectionParams['DATABASE']}.dbo.{self.__table}({columnList}) " \
                f"values ({parameterizedString})"

        self.__cursor.execute(query, *(fields.values()))
        self.__cursor.commit()

    def close(self):
        self.__cursor.close()
        self.__conn.close()