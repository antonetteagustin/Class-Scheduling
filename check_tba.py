from app import app, db, Teacher

def check():
    with app.app_context():
        t = Teacher.query.filter_by(name='TBA').first()
        if t:
            print(f"Name: {t.name}, MaxHours: {t.max_hours_per_day}")
        else:
            print("TBA teacher not found.")

if __name__ == "__main__":
    check()
