from app import app, db
from sqlalchemy import text

def update():
    with app.app_context():
        try:
            db.session.execute(text('ALTER TABLE subject ADD COLUMN is_system BOOLEAN DEFAULT 0'))
            db.session.commit()
            print("Column 'is_system' added to 'subject' table.")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("Column 'is_system' already exists.")
            else:
                print(f"Error: {e}")

if __name__ == "__main__":
    update()
