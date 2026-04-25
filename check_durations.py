from app import app
from models import Subject

with app.app_context():
    subs = Subject.query.filter_by(department='JHS').all()
    print("--- JHS Subject Durations ---")
    for s in subs:
        print(f"{s.name}: {s.duration_mins} mins")
