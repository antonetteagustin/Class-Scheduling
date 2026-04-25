from app import app, db, Setting, Schedule
with app.app_context():
    active_days = Setting.query.filter_by(key='active_days').first()
    print(f"Active Days Setting: {active_days.value if active_days else 'None (defaulting to Full Names)'}")
    
    sample_sch = Schedule.query.first()
    if sample_sch:
        print(f"Sample Schedule Day: {sample_sch.day_of_week}")
    else:
        print("No schedules found.")
