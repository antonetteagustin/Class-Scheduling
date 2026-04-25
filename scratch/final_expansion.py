import os
import sys
sys.path.append(os.getcwd())
from app import app, db
from models import Teacher

with app.app_context():
    # Physics 3rd expert: Teacher 9_S (19) - Ensure GL 12
    t9 = Teacher.query.get(19)
    if t9:
        if 'Physics' not in t9.subjects: t9.subjects += ', Physics'
        t9.grade_levels = '11, 12'
    
    # Language 3rd expert: Teacher 10_S (20) - Ensure GL 12
    t10 = Teacher.query.get(20)
    if t10:
        if 'Language' not in t10.subjects: t10.subjects += ', Language'
        t10.grade_levels = '11, 12'
        
    # Programming 3rd expert: Teacher 7_S (17) - FIX GL TO INCLUDE 12
    t7 = Teacher.query.get(17)
    if t7:
        if 'Programming' not in t7.subjects: t7.subjects += ', Programming'
        t7.grade_levels = '11, 12'
        
    db.session.commit()
    print("Final Expertise Expansion (3rd Experts with GL fixes) Complete.")
