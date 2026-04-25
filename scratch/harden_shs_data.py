import os
import sys
sys.path.append(os.getcwd())
from app import app, db
from models import Teacher, Subject

def harden_data():
    with app.app_context():
        print("=== DATA HARDENING: SUBJECT REGISTRATION ===")
        # Register FILDIS and Religion
        new_subs = [
            {'name': 'FILDIS', 'dept': 'SHS', 'gl': '12', 'dur': 40},
            {'name': 'Religion', 'dept': 'SHS', 'gl': '12', 'dur': 40}
        ]
        for s_info in new_subs:
            existing = Subject.query.filter_by(name=s_info['name'], department=s_info['dept']).first()
            if not existing:
                sub = Subject(
                    name=s_info['name'],
                    department=s_info['dept'],
                    grade_level=s_info['gl'],
                    duration_mins=s_info['dur'],
                    meetings_per_week=5,
                    track='None' # Core
                )
                db.session.add(sub)
                print(f"Added Subject: {s_info['name']}")
            else:
                print(f"Subject {s_info['name']} already exists.")

        # Update KOMPAN to cover both 11 and 12 if needed (Optional, but good for coverage)
        kompan = Subject.query.filter_by(name='KOMPAN', department='SHS').first()
        if kompan:
            kompan.grade_level = '11,12'
            print("Updated KOMPAN to cover Grade 11,12")

        print("\n=== DATA HARDENING: TEACHER ELIGIBILITY EXPANSION ===")
        # [14] Teacher 4_S (Physics), [15] Teacher 5_S (Language), [16] Teacher 6_S (Programming), [18] Teacher 8_S (EALS)
        target_ids = [14, 15, 16, 18]
        for t_id in target_ids:
            t = Teacher.query.get(t_id)
            if t:
                # Add '12' to grade_levels if not already there
                gls = [g.strip() for g in (t.grade_levels or '').split(',') if g.strip()]
                if '12' not in gls:
                    gls.append('12')
                    t.grade_levels = ','.join(gls)
                    print(f"Expanded {t.name} to Grade 12")
            else:
                print(f"Warning: Teacher ID {t_id} not found.")

        db.session.commit()
        print("\nDATA HARDENING COMPLETE.")

if __name__ == "__main__":
    harden_data()
