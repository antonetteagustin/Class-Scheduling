import sys
sys.path.append('.')
from app import app
from models import Subject, Setting, Section

def check():
    with app.app_context():
        jhs_subs = Subject.query.filter_by(department='JHS').all()
        settings = {s.key: s.value for s in Setting.query.all()}
        
        print(f"--- JHS Subjects ---")
        for s in jhs_subs:
            print(f"{s.name}: Frequency {s.meetings_per_week}")
            
        print(f"\n--- Special Mode Settings ---")
        print(f"JHS Enabled: {settings.get('jhs_special_enabled')}")
        print(f"JHS Days: {settings.get('jhs_special_days')}")
        print(f"Extra Subject: {settings.get('jhs_special_extra_subject')}")
        
        # Simulating Friday pool for a JHS Section
        friday = 'Friday'
        is_friday_special = settings.get('jhs_special_enabled') == 'yes' and friday in settings.get('jhs_special_days', '').split(',')
        extra_sub_name = settings.get('jhs_special_extra_subject', '').strip()
        
        # Subjects in JHS pool (filtered like scheduler.py)
        # Note: scheduler.py filters OUT the extra subject from the base reqs
        sec_subs = [s for s in jhs_subs if s.name.strip() != extra_sub_name]
        
        for d in ['Monday', 'Friday']:
            pool = []
            for s in sec_subs:
                freq = s.meetings_per_week
                is_on_day = False
                if freq >= 5: is_on_day = True
                elif freq == 4: is_on_day = (d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday'])
                elif freq == 3: is_on_day = (d in ['Monday', 'Wednesday', 'Friday'])
                elif freq == 2: is_on_day = (d in ['Tuesday', 'Thursday'])
                elif freq == 1: is_on_day = (d == 'Wednesday')
                
                if is_on_day: pool.append(s.name)
            
            # Add extra sub on special days
            added_extra = False
            if d == 'Friday' and is_friday_special:
                extra_obj = next((s for s in jhs_subs if s.name.strip() == extra_sub_name), None)
                if extra_obj:
                    pool.append(f"{extra_obj.name} (EXTRA)")
                    added_extra = True
                    
            print(f"\n{d} Subject Count: {len(pool)}")
            print(f"Subjects: {', '.join(pool)}")

if __name__ == "__main__":
    check()
