import os
import sys
sys.path.append(os.getcwd())
from app import app, db
from models import Teacher, Subject

with app.app_context():
    print("=== SHS TEACHER CAPACITY AUDIT ===")
    shs_teachers = Teacher.query.filter(Teacher.department.in_(['SHS', 'Both'])).all()
    for t in shs_teachers:
        print(f"[{t.id}] {t.name}")
        print(f"  Subjects: {t.subjects}")
        print(f"  Levels: {t.grade_levels}")
        print("-" * 20)
        
    print("\n=== SHS SUBJECTS REQUIRING COVERAGE ===")
    # These are the ones we identified earlier
    core_subs = ['Physics', 'Language', 'Programming']
    for s_name in core_subs:
        eligible = Teacher.query.filter(Teacher.subjects.like(f'%{s_name}%')).all()
        print(f"{s_name}: Currently {len(eligible)} teachers")
