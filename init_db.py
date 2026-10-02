import sqlite3

conn = sqlite3.connect("grades.db")
conn.executescript(open("schema.sql", encoding="utf-8").read())
conn.commit()
print(conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
conn.close()