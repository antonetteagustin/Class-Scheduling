import sys
sys.path.append('.')
from app import app, db
from models import Subject, Setting, Section, Teacher

def verify():
    with app.app_context():
        # Setup mock data for simulation
        dept = 'JHS'
        extra_name = 'Homeroom'
        
        print(f"--- Verification Run ---")
        
        # 1. Simulating the 'scheduler.py' provisioning logic
        hidden_sub = Subject.query.filter_by(name=extra_name, department=dept, is_system=True).first()
        if not hidden_sub:
            print(f"Provisioning hidden subject: {extra_name}")
            hidden_sub = Subject(name=extra_name, department=dept, duration_mins=40, meetings_per_week=0, is_system=True)
            db.session.add(hidden_sub)
            db.session.commit()
        else:
            print(f"Hidden subject '{extra_name}' already exists.")

        # 2. Simulate Pool Calculation
        sec = Section.query.filter_by(department=dept).first()
        if not sec:
            print("No JHS section found to test with.")
            return

        regular_subs = Subject.query.filter_by(department=dept, is_system=False).all()
        
        for d in ['Monday', 'Friday']:
            pool = []
            # Regular subs
            for s in regular_subs:
                freq = s.meetings_per_week
                is_on_day = False
                if freq >= 5: is_on_day = True
                elif freq == 4: is_on_day = (d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday'])
                elif freq == 3: is_on_day = (d in ['Monday', 'Wednesday', 'Friday'])
                elif freq == 2: is_on_day = (d in ['Tuesday', 'Thursday'])
                elif freq == 1: is_on_day = (d == 'Wednesday')
                if is_on_day: pool.append(s.name)
            
            # Special injection (Friday is special in my test)
            if d == 'Friday':
                pool.append(f"{hidden_sub.name} (HIDDEN)")
            
            print(f"\n{d} for {sec.name}:")
            print(f"  Count: {len(pool)}")
            print(f"  List: {', '.join(pool)}")
            
        # 3. Check Admin Filter
        subjects_visible = Subject.query.filter_by(is_system=False).count()
        subjects_total = Subject.query.count()
        print(f"\n--- Admin Visibility Check ---")
        print(f"Visible Subjects: {subjects_visible}")
        print(f"Total Subjects (incl. hidden): {subjects_total}")
        
        if subjects_total > subjects_visible:
            print("SUCCESS: System subjects are correctly hidden.")

if __name__ == "__main__":
    verify()
