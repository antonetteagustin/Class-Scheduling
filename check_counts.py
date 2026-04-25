from app import app
from models import db, Schedule, ScheduleRun

with app.app_context():
    run = ScheduleRun.query.filter_by(is_active=True).order_by(ScheduleRun.id.desc()).first()
    if run:
        count = Schedule.query.filter_by(run_id=run.id).count()
        print(f"Run ID: {run.id}")
        print(f"Conflicts: {run.conflicts}")
        print(f"Schedule Records: {count}")
    else:
        print("No active run found.")
