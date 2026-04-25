from app import app, db, Section, Classroom

def check():
    with app.app_context():
        secs = Section.query.all()
        for s in secs:
            print(f"Sec: {s.name}, Room: {s.room.name if s.room else None}")

if __name__ == "__main__":
    check()
