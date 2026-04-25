import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Section, Subject, Teacher

with app.app_context():
    s = Section.query.filter_by(name='Orange_8').first()
    if not s:
        print("Section Orange_8 not found")
        sys.exit()
    print(f'Section: {s.name}, Adviser: {s.adviser.name if s.adviser else "None"}')
    
    # Get subjects required for this section based on department and grade level
    # Logic from scheduler.py
    dept = s.department
    subjects = Subject.query.filter_by(department=dept).all()
    
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

    reqs = [sub for sub in subjects if gl_match(s.grade_level, sub.grade_level)]
    print('Subjects in regular pool:')
    for sub in reqs:
        print(f'  {sub.name} (Meetings/Week: {sub.meetings_per_week}, Duration: {sub.duration_mins}m)')
