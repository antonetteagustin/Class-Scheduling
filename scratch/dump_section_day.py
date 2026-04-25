import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Section, Subject, Teacher, Setting

def gl_match(req_gl, target_gl_str):
    if not target_gl_str: return True
    def norm(g): 
        if g is None: return ""
        return str(g).strip().upper().replace('GRADE', '').strip()
    req = norm(req_gl)
    if not req: return True
    targets = [norm(g) for g in str(target_gl_str).split(',') if norm(g)]
    if "ALL JHS" in str(target_gl_str).upper() and req in ['7', '8', '9', '10']: return True
    if "ALL SHS" in str(target_gl_str).upper() and req in ['11', '12']: return True
    for t in targets:
        if req == t or (len(req) >= 1 and req in t):
            return True
    return False

def dump_section_day(section_name, day):
    with app.app_context():
        sec = Section.query.filter_by(name=section_name).first()
        if not sec:
            print(f"Section {section_name} not found")
            return
            
        print(f"Auditing Requirements for {sec.name} on {day}...")
        
        # Get subjects for this section's grade level
        all_subs = Subject.query.filter_by(department=sec.department).all()
        sec_subs = [s for s in all_subs if gl_match(sec.grade_level, s.grade_level)]
        
        # Filter for day using the logic from scheduler.py
        daily_pool = []
        for s in sec_subs:
            freq = s.meetings_per_week
            is_on_day = False
            if freq >= 5: is_on_day = True
            elif freq == 4: is_on_day = (day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday'])
            elif freq == 3: is_on_day = (day in ['Monday', 'Wednesday', 'Friday'])
            elif freq == 2: is_on_day = (day in ['Tuesday', 'Thursday'])
            elif freq == 1: is_on_day = (day == 'Wednesday')
            
            if is_on_day: daily_pool.append(s)
            
        # Add Special Extra Subject if applicable
        settings = {s.key: s.value for s in Setting.query.all()}
        spec_enabled = settings.get('special_mode', 'off') == 'on'
        spec_days = settings.get('special_mode_days', '').split(',')
        is_special_day = spec_enabled and day in spec_days
        
        if is_special_day:
            extra_sub_name = settings.get(f'{sec.department.lower()}_special_extra', 'None')
            if extra_sub_name != 'None':
                extra_obj = Subject.query.filter_by(name=extra_sub_name, department=sec.department).first()
                if extra_obj:
                    daily_pool.append(extra_obj)

        print(f"Total Subjects for {day}: {len(daily_pool)}")
        for sub in daily_pool:
            # Check eligibility
            if sub.department == 'SHS':
                eligible = [t for t in Teacher.query.all() if (sub.name.strip() in [s_n.strip() for s_name in (t.subjects or '').split(',')] and (gl_match(sec.grade_level, t.grade_levels) or t.department == 'Both' or t.is_hybrid))]
            else:
                eligible = [t for t in Teacher.query.all() if (sub.name.strip() in [s_n.strip() for s_name in (t.subjects or '').split(',')] and (gl_match(sec.grade_level, t.grade_levels) or t.department == 'Both'))]
            
            print(f"  - {sub.name}: {len(eligible)} qualified teachers")
            if not eligible:
                print(f"    [!] MISSING TEACHER")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        dump_section_day(sys.argv[1], sys.argv[2])
    else:
        print("Usage: py dump_section_day.py <section_name> <day>")
