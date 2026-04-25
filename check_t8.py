from app import app, db, Teacher

def check():
    with app.app_context():
        t = Teacher.query.filter_by(name='Teacher 8_J').first()
        if t:
            print(f"Name: {t.name}, Subjects: {t.subjects}, GL: {t.grade_levels}")
        else:
            print("Teacher 8_J not found.")

if __name__ == "__main__":
    check()
