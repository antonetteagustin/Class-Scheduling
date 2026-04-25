import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Subject

with app.app_context():
    subjects = Subject.query.all()
    with open('scratch/all_subjects.txt', 'w') as f:
        for s in subjects:
            f.write(f"ID: {s.id} | Name: {s.name} | Dept: {s.department} | GL: {s.grade_level} | Track: {s.track}\n")
    print(f"Dumped {len(subjects)} subjects to scratch/all_subjects.txt")
