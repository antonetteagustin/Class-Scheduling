from app import app, db, Teacher, Subject, Section

with app.app_context():
    print("--- SECTIONS ---")
    sections = Section.query.all()
    for s in sections:
        print(f"ID: {s.id} | Name: {s.name} | Dept: {s.department} | GL: {s.grade_level!r} | Track: {s.track!r}")
    
    print("\n--- SUBJECTS ---")
    subjects = Subject.query.all()
    for sub in subjects:
        print(f"ID: {sub.id} | Name: {sub.name} | Dept: {sub.department} | GL: {sub.grade_level!r} | Track: {sub.track!r}")

    print("\n--- TEACHERS ---")
    teachers = Teacher.query.all()
    for t in teachers:
        print(f"ID: {t.id} | Name: {t.name} | GLs: {t.grade_levels!r} | Subs: {t.subjects!r}")
