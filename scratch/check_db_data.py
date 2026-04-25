import sqlite3
import os

db_path = 'database.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, grade_level, department FROM section LIMIT 10")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    cursor.execute("SELECT key, value FROM setting WHERE key LIKE 'jhs_%' OR key LIKE 'shs_%'")
    rows = cursor.fetchall()
    print("\nSettings:")
    for row in rows:
        print(row)
    conn.close()
else:
    print("database.db not found")
