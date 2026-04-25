from app import app, db, Section, Teacher, Subject, Classroom

def compare_sections():
    with app.app_context():
        for name in ['Black_10', 'Gray_10']:
            sec = Section.query.filter_by(name=name).first()
            if not sec: continue
            print(f"Section {sec.name}: Adviser={sec.adviser.name if sec.adviser else 'None'}, Room={sec.room.name if sec.room else 'None'}")
            
if __name__ == "__main__":
    compare_sections()
