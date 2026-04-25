from app import app, db, Subject

def check():
    with app.app_context():
        subs = Subject.query.filter_by(department='JHS').all()
        for s in subs:
            print(f"Sub: {s.name}, Lab: {s.requires_lab}")

if __name__ == "__main__":
    check()
