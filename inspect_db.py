import sqlite3
conn = sqlite3.connect('C:/Users/Edu/Documents/GitHub/KeplerDB_Gemini/kepler.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())
conn.close()
