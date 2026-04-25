from app import app, db, Teacher, Subject

def gl_match(sec_gl, teacher_gls):
    if not teacher_gls or str(teacher_gls).strip() == '': return False
    s_gl = str(sec_gl).strip().upper().replace('GRADE', '').strip()
    t_gls = [g.strip().upper().replace('GRADE', '').strip() for g in str(teacher_gls).split(',')]
    for t_gl in t_gls:
        if s_gl in t_gl or t_gl in s_gl: return True
    return False

def check_english():
    with app.app_context():
        teachers = Teacher.query.all()
        for gl in ['8', '10']:
            eligible = []
            for t in teachers:
                if 'English' in [s.strip() for s in str(t.subjects).split(',')]:
                    if gl_match(gl, t.grade_levels):
                        eligible.append(t.name)
            print(f"English Grade {gl} candidates: {eligible}")

if __name__ == "__main__":
    check_english()
