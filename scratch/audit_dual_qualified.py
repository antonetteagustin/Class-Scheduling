import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Teacher

with app.app_context():
    # Use explicit comparisons for clarity
    teachers = Teacher.query.filter((Teacher.department == 'Both') | (Teacher.is_hybrid == True)).all()
    print(f"DEBUG: Found {len(teachers)} dual-qualified teachers.")
    for t in teachers:
        print(f"Name: {t.name} | Dept: {t.department} | Hybrid: {t.is_hybrid} | GL: {t.grade_levels}")

    # Also check if any teacher has 'Both' in their grade_levels just in case
    other = Teacher.query.filter(Teacher.grade_levels.like('%Both%')).all()
    if other:
        print(f"DEBUG: Found {len(other)} teachers with 'Both' in Grade Levels.")
        for t in other:
            print(f"Name: {t.name} | GL: {t.grade_levels}")
