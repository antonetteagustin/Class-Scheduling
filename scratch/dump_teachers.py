import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Teacher

with app.app_context():
    teachers = Teacher.query.all()
    with open('scratch/all_teachers.txt', 'w') as f:
        for t in teachers:
            f.write(f"ID: {t.id} | Name: {t.name} | Dept: {t.department} | Hybrid: {t.is_hybrid} | GL: {t.grade_levels} | Subs: {t.subjects}\n")
    print(f"Dumped {len(teachers)} teachers to scratch/all_teachers.txt")
