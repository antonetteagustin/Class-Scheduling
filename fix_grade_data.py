from app import app, db, Teacher, Section, Subject
import re

def clean_gl(gl_str):
    if not gl_str:
        return gl_str
    # Split by comma, clean each part, join back
    parts = gl_str.split(',')
    cleaned_parts = []
    for p in parts:
        # Remove any "Grade ", "Gr ", "G " prefix (case-insensitive)
        c = re.sub(r'^(Grade|Gr|G)\s*', '', p.strip(), flags=re.IGNORECASE)
        cleaned_parts.append(c)
    return ','.join(cleaned_parts)

with app.app_context():
    print("Starting database cleanup of grade level formats...")
    
    # 1. Teachers
    teachers = Teacher.query.all()
    t_count = 0
    for t in teachers:
        old = t.grade_levels
        new = clean_gl(old)
        if old != new:
            t.grade_levels = new
            t_count += 1
    
    # 2. Sections
    sections = Section.query.all()
    sec_count = 0
    for s in sections:
        old = s.grade_level
        new = clean_gl(old)
        if old != new:
            s.grade_level = new
            sec_count += 1
            
    # 3. Subjects
    subjects = Subject.query.all()
    sub_count = 0
    for sub in subjects:
        old = sub.grade_level
        new = clean_gl(old)
        if old != new:
            sub.grade_level = new
            sub_count += 1
            
    db.session.commit()
    print(f"Cleanup finished!")
    print(f"Updated {t_count} Teachers")
    print(f"Updated {sec_count} Sections")
    print(f"Updated {sub_count} Subjects")
