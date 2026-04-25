from app import app
from models import ScheduleRun

def read_logs():
    with app.app_context():
        run = ScheduleRun.query.order_by(ScheduleRun.id.desc()).first()
        if run:
            print(f"Run ID: {run.id}")
            print(f"Conflicts: {run.conflicts}")
            print("\nLOG ENTRIES:")
            logs = run.conflict_log.split(' | ')
            for l in logs[:20]: # Show first 20
                print(f"- {l}")
        else:
            print("No runs found.")

if __name__ == "__main__":
    read_logs()
