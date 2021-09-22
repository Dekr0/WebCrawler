import pyodbc


args = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",
    "SERVER": "localhost",
    "DATABASE": "TestDB",
    "UID": "SA",
    "PWD": "G12eT22Righ00t",
}

paramString = ";".join([f"{arg}={value}" for arg, value in args.items()])

conn = pyodbc.connect(paramString)

query = "CREATE TABLE "
