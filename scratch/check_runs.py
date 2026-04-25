import os
import sys
sys.path.append(os.getcwd())
from app import app, db
from models import ScheduleRun

with app.app_context():
    count = ScheduleRun.query.count()
    print(f"Total ScheduleRuns: {count}")
    last = ScheduleRun.query.order_by(ScheduleRun.id.desc()).first()
    if last:
        print(f"Last Run: ID {last.id}, Status: {'Success' if last.conflicts == 0 else 'Failed'}, Conflicts: {last.conflicts}")
