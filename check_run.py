from app import app, db, ScheduleRun

def check():
    with app.app_context():
        r = ScheduleRun.query.order_by(ScheduleRun.id.desc()).first()
        if r:
            print(f"Conflicts: {r.conflicts}")
            print(f"Log: {r.conflict_log}")
        else:
            print("No run found.")

if __name__ == "__main__":
    check()
