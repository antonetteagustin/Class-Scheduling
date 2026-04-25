from app import app, db, Teacher, Subject

def normalize_gl(gl):
    if not gl: return gl
    gl_s = str(gl).strip()
    if gl_s.isdigit(): return f"Grade {gl_s}"
    return gl_s

with app.app_context():
    print("Starting Database Cleanup...")
    
    # Update Subjects
    subjects = Subject.query.all()
    sub_count = 0
    for s in subjects:
        old_gl = s.grade_level
        new_gl = normalize_gl(old_gl)
        if old_gl != new_gl:
            s.grade_level = new_gl
            sub_count += 1
    
    # Update Teachers
    teachers = Teacher.query.all()
    tea_count = 0
    for t in teachers:
        if t.grade_levels:
            old_gls = t.grade_levels
            new_gls = ",".join([normalize_gl(g) for g in old_gls.split(',')])
            if old_gls != new_gls:
                t.grade_levels = new_gls
                tea_count += 1
                
    db.session.commit()
    print(f"Cleanup finished.")
    print(f"Updated {sub_count} subjects.")
    print(f"Updated {tea_count} teachers.")
