from app import app, db, Setting, Section, Subject
from scheduler import generate_schedule, time_to_min

def test_gen():
    with app.app_context():
        print("--- Testing Schedule Generation (Refined Homeroom & Consistency) ---")
        
        def progress_cb(p, m):
            if "Attempt" in m and p % 10 == 0:
                 print(f"[{p}%] {m}")
            elif "Complete" in m:
                 print(f"[{p}%] {m}")
            
        success, duration, conflicts, reason = generate_schedule(progress_callback=progress_cb)
        
        print(f"\nResult: Success={success}, Duration={duration}, Conflicts={conflicts}")
        
        # Check Homeroom position and subsequent subject
        from models import Schedule, ScheduleRun
        latest_run = ScheduleRun.query.order_by(ScheduleRun.id.desc()).first()
        if not latest_run:
            print("No schedule run found.")
            return

        # Check a few sections
        sections_to_check = Section.query.limit(3).all()
        for sec in sections_to_check:
            print(f"\nChecking Section: {sec.name}")
            # Monday Order (Regular)
            mon = Schedule.query.filter_by(section_id=sec.id, day_of_week='Monday', run_id=latest_run.id).order_by(Schedule.start_time).all()
            mon_sub_names = [m.subject.name for m in mon]
            print(f"  Monday: {mon_sub_names}")
            
            # Friday Order (Special)
            fri = Schedule.query.filter_by(section_id=sec.id, day_of_week='Friday', run_id=latest_run.id).order_by(Schedule.start_time).all()
            fri_sub_names = [f.subject.name for f in fri]
            print(f"  Friday: {fri_sub_names}")
            
            if mon_sub_names and fri_sub_names:
                # Friday should start with Homeroom, then follow Monday's order
                if fri_sub_names[0] == 'Homeroom':
                    # Check if fri_sub_names[1:] is a subset of mon_sub_names in order
                    # (Subset because some Mon subjects might not be on Fri)
                    mon_clean = [n for n in mon_sub_names if n in fri_sub_names]
                    fri_clean = [n for n in fri_sub_names if n != 'Homeroom']
                    if mon_clean == fri_clean:
                        print(f"  SUCCESS: Friday order follows Monday's order after Homeroom.")
                    else:
                        print(f"  FAILED: Friday order mismatch. Expected {mon_clean}, got {fri_clean}")
                else:
                    print(f"  FAILED: Homeroom is NOT at start of Friday. Got {fri_sub_names[0]}")

if __name__ == "__main__":
    test_gen()
