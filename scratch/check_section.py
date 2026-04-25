import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Section, Subject, Teacher

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

def check_section(section_name):
    with app.app_context():
        s = Section.query.filter_by(name=section_name).first()
        if not s:
            print(f"Section {section_name} not found")
            return
        print(f"Section: {s.name}, Grade: {s.grade_level}, Track: {s.track}")
        
        dept = s.department
        subjects = Subject.query.filter_by(department=dept).all()
        
        reqs = [sub for sub in subjects if gl_match(s.grade_level, sub.grade_level)]
        print(f"Subjects for {s.name}:")
        for sub in reqs:
            # Check eligibility rule from scheduler.py
            if sub.department == 'SHS':
                eligible = [t for t in Teacher.query.all() if (sub.name.strip() in [s_name.strip() for s_name in (t.subjects or '').split(',')] and gl_match(s.grade_level, t.grade_levels)) and (t.department in ['SHS', 'Both'] or getattr(t, 'is_hybrid', False))]
            else:
                eligible = [t for t in Teacher.query.all() if (sub.name.strip() in [s_name.strip() for s_name in (t.subjects or '').split(',')] and gl_match(s.grade_level, t.grade_levels)) and (t.department in ['JHS', 'Both'])]
            
            print(f"  {sub.name}: {len(eligible)} qualified teachers")
            if not eligible:
                print(f"    [!] NO QUALIFIED TEACHERS FOR {sub.name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_section(sys.argv[1])
    else:
        print("Usage: py check_section.py <section_name>")
