from app import app, db, Teacher, Schedule, ScheduleRun, User
import sys

with app.app_context():
    active_runs = ScheduleRun.query.all()
    print(f"Total Schedule Runs: {len(active_runs)}")
    for run in active_runs:
        print(f"Run ID: {run.id} | Active: {run.is_active} | Created: {run.created_at}")

    active_run = ScheduleRun.query.filter_by(is_active=True).first()
    if not active_run:
        print("ERROR: No active ScheduleRun found.")
        sys.exit(1)

    # Check a sample teacher user
    teacher_user = User.query.filter_by(role='teacher').first()
    if teacher_user:
        print(f"\nSample Teacher User: {teacher_user.username}")
        print(f"Related ID: {teacher_user.related_id}")
        teacher = Teacher.query.get(teacher_user.related_id)
        if teacher:
            print(f"Teacher Record: {teacher.name} (ID: {teacher.id})")
            schedules = Schedule.query.filter_by(teacher_id=teacher.id, run_id=active_run.id).all()
            print(f"Schedules in active run: {len(schedules)}")
            for s in schedules:
                print(f"  - Subject: {s.subject_id} | Day: {s.day} | Time: {s.start_time}")
        else:
            print("ERROR: Teacher record missing for this user.")
    else:
        print("No teacher users found.")

    total_schedules = Schedule.query.filter_by(run_id=active_run.id).count()
    print(f"\nTotal schedules in active run: {total_schedules}")
