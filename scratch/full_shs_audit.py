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

def full_audit():
    with app.app_context():
        print("=== SHS SUBJECT AUDIT ===")
        shs_subs = Subject.query.filter_by(department='SHS').all()
        teachers = Teacher.query.all()
        
        for sub in shs_subs:
            print(f"Subject: {sub.name} (GL: {sub.grade_level})")
            # Potential teachers by expertise
            qualified = [t for t in teachers if sub.name.strip() in [s.strip() for s in (t.subjects or '').split(',')]]
            print(f"  - Total with expertise: {len(qualified)}")
            
            # Check per Grade Level
            for gl in ['11', '12']:
                eligible = [t for t in qualified if (gl_match(gl, t.grade_levels) or t.department == 'Both' or t.is_hybrid)]
                if not eligible:
                    print(f"    [!] NO ELIGIBLE TEACHER FOR GRADE {gl}")
                else:
                    print(f"    - Grade {gl}: {len(eligible)} teachers ({', '.join([t.name for t in eligible])})")
        
        print("\n=== UNMAPPED TEACHER EXPERTISE ===")
        sub_names = [s.name.strip() for s in Subject.query.all()]
        for t in teachers:
            if t.department in ['SHS', 'Both']:
                t_subs = [s.strip() for s in (t.subjects or '').split(',') if s.strip()]
                orphan = [s for s in t_subs if s not in sub_names]
                if orphan:
                    print(f"Teacher {t.name} specializes in {orphan} - NOT IN SUBJECT TABLE")

if __name__ == "__main__":
    full_audit()
