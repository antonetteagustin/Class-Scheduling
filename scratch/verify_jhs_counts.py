from app import app
from models import db, Subject, Section, Setting, Schedule, ScheduleRun

def check():
    with app.app_context():
        # Check counts
        jhs_subs = Subject.query.filter_by(department='JHS').all()
        jhs_sections = Section.query.filter_by(department='JHS').all()
        settings = {s.key: s.value for s in Setting.query.all()}
        
        print(f"JHS Subjects: {len(jhs_subs)}")
        for s in jhs_subs:
            print(f"  - {s.name} (Freq: {s.meetings_per_week})")
            
        print(f"JHS Sections: {len(jhs_sections)}")
        
        # Check active run
        active_run = ScheduleRun.query.filter_by(is_active=True).order_by(ScheduleRun.id.desc()).first()
        if not active_run:
            print("No active schedule run found.")
            return
            
        print(f"Verifying Run ID: {active_run.id} (SY: {active_run.school_year})")
        
        for sec in jhs_sections:
            print(f"\nSection: {sec.name}")
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                count = Schedule.query.filter_by(run_id=active_run.id, section_id=sec.id, day_of_week=day).count()
                print(f"  {day}: {count} subjects")

if __name__ == "__main__":
    check()
