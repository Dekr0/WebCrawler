import pyodbc


args = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",
    "SERVER": "localhost",
    "DATABASE": "Jobs",
    "UID": "SA",
    "PWD": "G12eT22Righ00t",
}

paramString = ";".join([f"{arg}={value}" for arg, value in args.items()])

conn = pyodbc.connect(paramString)

cursor = conn.cursor()

row = cursor.execute(f"SELECT * FROM Jobs.dbo.Indeed WHERE Id LIKE (?)", "%4d1940af6aed0707%")
