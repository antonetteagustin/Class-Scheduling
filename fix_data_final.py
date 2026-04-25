from app import app, db, Teacher, Subject

def norm_list(gl_str):
    if not gl_str: return gl_str
    parts = [p.strip() for p in gl_str.split(',')]
    new_parts = []
    for p in parts:
        if p.isdigit(): new_parts.append(f"Grade {p}")
        else: new_parts.append(p)
    return ", ".join(new_parts)

with app.app_context():
    print("Starting Final Data Fix...")
    
    # Update Subjects
    subjects = Subject.query.all()
    sub_count = 0
    for s in subjects:
        old_gl = s.grade_level
        new_gl = norm_list(old_gl)
        if old_gl != new_gl:
            s.grade_level = new_gl
            sub_count += 1
    
    # Update Teachers
    teachers = Teacher.query.all()
    tea_count = 0
    for t in teachers:
        old_gls = t.grade_levels
        new_gls = norm_list(old_gls)
        if old_gls != new_gls:
            t.grade_levels = new_gls
            tea_count += 1
                
    db.session.commit()
    print(f"Fix finished. Updated {sub_count} subjects and {tea_count} teachers.")
