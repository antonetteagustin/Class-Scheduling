from app import app
from models import db, Teacher, Schedule, ScheduleRun
from sqlalchemy import func

def verify():
    with app.app_context():
        # Get active run
        run = ScheduleRun.query.filter_by(is_active=True).first()
        if not run:
            print("No active run found.")
            return

        schedules = Schedule.query.filter_by(run_id=run.id).all()
        teachers = Teacher.query.all()
        
        violations = []
        
        for t in teachers:
            if t.name == "TBA": continue
            
            # Check each day
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                day_sch = [s for s in schedules if s.teacher_id == t.id and s.day_of_week == day]
                if not day_sch: continue
                
                # Load check
                total_mins = sum(s.subject.duration_mins for s in day_sch)
                if total_mins > t.max_hours_per_day * 60:
                    violations.append(f"LOAD VIOLATION: {t.name} on {day}: {total_mins/60}h > {t.max_hours_per_day}h")
                
                # Stay window check
                def time_to_min(t_str):
                    h, m = map(int, t_str.split(':'))
                    return h * 60 + m
                
                starts = [time_to_min(s.start_time) for s in day_sch]
                ends = [time_to_min(s.end_time) for s in day_sch]
                
                span = max(ends) - min(starts)
                if span > t.stay_window_hours * 60:
                    violations.append(f"STAY VIOLATION: {t.name} on {day}: {span/60}h > {t.stay_window_hours}h")
                    
        if not violations:
            print("Verification passed! No load or stay window violations found.")
        else:
            print(f"Found {len(violations)} violations:")
            for v in violations:
                print(f" - {v}")

if __name__ == "__main__":
    verify()
