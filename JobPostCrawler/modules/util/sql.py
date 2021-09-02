import pyodbc


_ARGS = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",
    "SERVER": "localhost",
    "DATABASE": "Jobs",
    "UID": "sa",
    "PWD": "G12eT22Righ00t"
}

_p_str = ";".join([f"{arg}={value}" for arg, value in _ARGS.items()])


class SQLUtil:

    def __init__(self):
        self.__conn = pyodbc.connect(_p_str)
        self.__cursor = self.__conn.cursor()

    def table_exist(self, table):
        if self.__cursor.tables(table=table, tableType='TABLE').fetchone():
            return True

        return False

    def create_table(self, table, columns_def):
        column_declaration = ", ".join([f"{column_name} {_type}"
                            for column_name, _type in columns_def.items()])

        query = f"CREATE TABLE {table} (" + column_declaration + ")"

        self.__cursor.execute(query)
        self.__conn.commit()

    def record_exist(self, table, conditions):
        selector = " OR ".join([f"{column_name} LIKE '%{pattern}%'"
                    for column_name, pattern in conditions.items()])

        query = f"SELECT * FROM {_ARGS['DATABASE']}.dbo.{table} WHERE {selector}"

        row = self.__cursor.execute(query).fetchone()

        if row:
            return True

        return False

    def delete_rows(self, table, conditions):
        for pattern in conditions.values():
            if '\'' in pattern:
                pattern.replace("\'", "\'\'")

        selector = " OR ".join([f"{column_name} LIKE '%{pattern}%'"
                    for column_name, pattern in conditions.items()])

        query = f"DELETE FROM {_ARGS['DATABASE']}.dbo.{table} WHERE {selector}"

        self.__cursor.execute(query)
        self.__cursor.commit()

    def insert_row(self, table, data):
        column_definition = f"{', '.join([column_name for column_name in data.keys()])}"

        query = f"INSERT INTO {_ARGS['DATABASE']}.dbo.{table}({column_definition}) " \
                f"values ({', '.join(['?' for i in range(len(data))])})"

        self.__cursor.execute(query, *(data.values()))
        self.__cursor.commit()

    def close(self):
        self.__cursor.close()
        self.__conn.close()