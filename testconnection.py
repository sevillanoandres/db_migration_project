import pyodbc

server = 'srvapichallenge.database.windows.net'
database = 'API_Challenge_DB'
username = 'apichallengeadmin'
password = 'Oscar1984$'
driver = '{ODBC Driver 18 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful")
except Exception as e:
    print("Connection failed")
    print(e)
