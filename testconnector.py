import sqlite3 as mdb
def chk_conn(conn):
     try:
        conn.cursor()
        return True
     except Exception as ex:
        return False

myconn = mdb.connect('apichallenge.db')
print(chk_conn(myconn))