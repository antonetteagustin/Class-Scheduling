import sys
import os
import time

# Set up environment
sys.path.append(os.getcwd())

try:
    from app import app, db
    from models import Section, Teacher, Subject, Classroom, Setting, Schedule, ScheduleRun
    from scheduler import generate_schedule, time_to_min, min_to_time
    
    with app.app_context():
        # Force a specific JHS section to be tested
        section = Section.query.filter_by(department='JHS', grade_level='7').first()
        if not section:
            print("No JHS section found")
            sys.exit(1)
            
        print(f"Testing break enforcement for: {section.name}")
        
        # Mock settings to ensure 09:00 break
        # We'll just read them as they should be there
        
        # Run generation for JHS only
        print("Running JHS Generation...")
        success, duration, conflicts, reason = generate_schedule(phase='jhs')
        print(f"Result: Success={success}, Conflicts={conflicts}")
        
        # Get the latest run
        run = ScheduleRun.query.order_by(ScheduleRun.id.desc()).first()
        schedules = Schedule.query.filter_by(run_id=run.id, section_id=section.id, day_of_week='Monday').all()
        
        print("\nMonday Schedule for " + section.name + ":")
        for s in sorted(schedules, key=lambda x: time_to_min(x.start_time)):
            print(f"{s.start_time} - {s.end_time}: {s.subject.name}")
            
except Exception as e:
    import traceback
    traceback.print_exc()
