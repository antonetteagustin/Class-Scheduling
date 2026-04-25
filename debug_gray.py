from app import app, db, Section, Teacher, Subject, Classroom
import re

def gl_match(sec_gl, teacher_gls):
    if not teacher_gls or str(teacher_gls).strip() == '': return False
    s_gl = str(sec_gl).strip().upper().replace('GRADE', '').strip()
    t_gls = [g.strip().upper().replace('GRADE', '').strip() for g in str(teacher_gls).split(',')]
    for t_gl in t_gls:
        # Check for flex match: if '11' is in '11STEM' or vice versa
        if s_gl in t_gl or t_gl in s_gl:
            return True
    return False

def debug_gray():
    with app.app_context():
        sec = Section.query.filter_by(name='Gray_10').first()
        if not sec:
            print("Section Gray_10 not found.")
            return
        
        print(f"--- Debugging Section: {sec.name} (Grade {sec.grade_level}, Dept {sec.department}) ---")
        print(f"Adviser: {sec.adviser.name if sec.adviser else 'None'}")
        
        # Get subjects for this section
        all_subs = Subject.query.filter(Subject.department == sec.department).all()
        sec_subs = []
        for s in all_subs:
            grades = [g.strip() for g in str(s.grade_level).split(',')]
            gl_val = str(sec.grade_level).strip()
            if gl_val in grades or 'All' in str(s.grade_level):
                 sec_subs.append(s)
        
        print(f"\nSubjects for this section ({len(sec_subs)}):")
        teachers = Teacher.query.all()
        for s in sec_subs:
            eligible = []
            for t in teachers:
                t_subs = [sub.strip() for sub in str(t.subjects).split(',')]
                if s.name in t_subs and gl_match(sec.grade_level, t.grade_levels):
                    eligible.append(t.name)
            print(f"  - {s.name}: {s.meetings_per_week}x/week, Teachers: {eligible}")

        print(f"\nDemand Check for these teachers:")
        all_sections = Section.query.all()
        for s in sec_subs:
            for t in teachers:
                t_subs = [sub.strip() for sub in str(t.subjects).split(',')]
                if s.name in t_subs and gl_match(sec.grade_level, t.grade_levels):
                    # Count how many TOTAL sections need this teacher for this subject
                    demand = 0
                    for other_sec in all_sections:
                        # Check if other_sec has this subject
                        other_gl = str(other_sec.grade_level).strip()
                        s_grades = [g.strip() for g in str(s.grade_level).split(',')]
                        if other_gl in s_grades or 'All' in str(s.grade_level):
                            # Yes, other_sec needs this subject.
                            # Is this teacher the only/primary candidate?
                            # For simplicity, just count sections of the same grade level
                            if other_gl == str(sec.grade_level).strip():
                                demand += 1
                    print(f"  - Teacher {t.name} (Sub: {s.name}) is needed by {demand} Grade {sec.grade_level} sections.")
                    break # Only report first eligible teacher for brevity

if __name__ == "__main__":
    debug_gray()
