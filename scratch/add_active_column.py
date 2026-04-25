import sqlite3
import os

db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(teacher)")
        columns = [c[1] for c in cursor.fetchall()]
        
        if 'is_active' not in columns:
            print("Adding is_active column...")
            cursor.execute("ALTER TABLE teacher ADD COLUMN is_active BOOLEAN DEFAULT 1")
            conn.commit()
            print("Cleanup successful.")
        else:
            print("is_active column already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
