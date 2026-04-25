from app import app
from models import Teacher, Subject

with app.app_context():
    physics_subs = Subject.query.filter(Subject.name.ilike('%Physics%')).all()
    print("PHYSICS SUBJECTS FOUND:")
    for s in physics_subs:
        print(f"ID: {s.id} | Name: {s.name} | Dept: {s.department}")
    
    print("\nQUALIFIED TEACHERS (Physics):")
    teachers = Teacher.query.all()
    for t in teachers:
        subs = [s.strip() for s in (t.subjects or "").split(',')]
        if any("Physics" in s for s in subs):
            print(f"Name: {t.name} | Grade Levels: {t.grade_levels} | Subjects: {t.subjects}")
