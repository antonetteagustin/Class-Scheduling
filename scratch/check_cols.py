from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('teacher')]
    print(f"Columns in 'teacher' table: {columns}")
