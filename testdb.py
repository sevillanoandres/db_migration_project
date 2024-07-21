import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('migration.db')
cursor = conn.cursor()

# Define table names
tables = ['departments', 'jobs', 'employees']

# Query and print records from each table
for table_name in tables:
    
    print(f"Records in {table_name}:")
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("\n")

# Close the connection
conn.close()
