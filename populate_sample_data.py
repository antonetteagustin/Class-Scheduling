import os
from app import app
from models import db, Teacher, Classroom, Section, Subject, Setting, Schedule, ScheduleRun, User
from werkzeug.security import generate_password_hash

def populate():
    with app.app_context():
        print("Starting Database Reset & Repopulation...")
        
        # 1. Clear Data (Order matters for foreign keys)
        Schedule.query.delete()
        ScheduleRun.query.delete()
        Section.query.delete()
        Subject.query.delete()
        Teacher.query.delete()
        Classroom.query.delete()
        Setting.query.delete()
        User.query.filter(User.role != 'admin').delete()
        db.session.commit()
        print("Database and Settings cleared.")

        # 2. Create Subjects
        # JHS Core (8 subjects * 45 mins + 30m break = 6.5 hours)
        jhs_subs = [
            ('Filipino', 45, 4), ('English', 45, 4), ('Math', 45, 4), ('Science', 45, 4),
            ('Araling Panlipunan', 45, 3), ('TLE', 45, 4), ('EsP', 45, 2), ('MAPEH', 45, 4)
        ]
        subjects = []
        for name, dur, freq in jhs_subs:
            sub = Subject(name=name, department='JHS', duration_mins=dur, meetings_per_week=freq, grade_level='7,8,9,10')
            db.session.add(sub)
            subjects.append(sub)

        # SHS Core & Applied
        shs_core = [
            ('Oral Communication', 60, 4), ('Gen. Mathematics', 60, 4), ('Earth & Life Science', 60, 4),
            ('21st Century Lit', 60, 4), ('Physical Education', 60, 2), ('Research in Daily Life', 60, 4)
        ]
        for name, dur, freq in shs_core:
            sub = Subject(name=name, department='SHS', duration_mins=dur, meetings_per_week=freq, grade_level='11,12', track='All')
            db.session.add(sub)
            subjects.append(sub)

        # SHS Specialized
        shs_spec = [
            ('Pre-Calculus', 60, 4, 'STEM', False), ('General Chemistry', 60, 4, 'STEM', True),
            ('Creative Writing', 60, 4, 'HUMSS', False), ('Introduction to World Religions', 60, 4, 'HUMSS', False),
            ('Computer Programming', 60, 4, 'TVL-ICT', True), ('ICT Specialization', 60, 4, 'TVL-ICT', True)
        ]
        for name, dur, freq, track, lab in shs_spec:
            sub = Subject(name=name, department='SHS', duration_mins=dur, meetings_per_week=freq, grade_level='11,12', track=track, requires_lab=lab)
            db.session.add(sub)
            subjects.append(sub)
        
        db.session.commit()
        print("Subjects created.")

        # 3. Create Classrooms
        # JHS Buildings (35 rooms for 35 sections - 1:1 ratio for simplicity and success)
        classrooms = []
        for i in range(1, 36):
            c = Classroom(name=f"JHS Room {i}", room_type='Room', building='JHS')
            db.session.add(c)
            classrooms.append(c)
        
        # SHS Buildings (16 rooms)
        for i in range(1, 17):
            c = Classroom(name=f"SHS Room {i}", room_type='Room', building='SHS')
            db.session.add(c)
            classrooms.append(c)
            
        # Labs
        labs = [
            Classroom(name="Biochem Lab", room_type='Laboratory', building='SHS'),
            Classroom(name="Physics Lab", room_type='Laboratory', building='SHS'),
            Classroom(name="Computer Lab", room_type='Laboratory', building='SHS')
        ]
        for l in labs: db.session.add(l)
        
        db.session.commit()
        print("Classrooms and Labs created.")

        # 4. Create Teachers
        teachers = []
        # JHS: Filipino (8), English (7), Math (9), Science (9), AP (5), TLE (12), EsP (6), MAPEH (8)
        jhs_counts = {
            'Filipino': 8, 'English': 7, 'Math': 9, 'Science': 9, 
            'Araling Panlipunan': 5, 'TLE': 12, 'EsP': 6, 'MAPEH': 8
        }
        
        idx = 1
        for sub_name, count in jhs_counts.items():
            for _ in range(count):
                # Using 8 hours to give the scheduler more breathing room
                t = Teacher(name=f"Teacher {idx} ({sub_name})", department='JHS', grade_levels="7,8,9,10", subjects=sub_name, max_hours_per_day=8)
                db.session.add(t)
                teachers.append(t)
                idx += 1
        
        # Head Teachers (7, no load)
        for i in range(1, 8):
            ht = Teacher(name=f"Head Teacher {i}", department='Both', grade_levels="7,8,9,10,11,12", subjects="Administrative", max_hours_per_day=0)
            db.session.add(ht)
            teachers.append(ht)

        # Cross-Dept (Apply to teachers from Science/Math/English)
        cross_count = 0
        jhs_teachers = [t for t in teachers if t.department == 'JHS']
        for t in jhs_teachers:
            if t.subjects in ['Science', 'Math', 'English'] and cross_count < 10:
                t.department = 'Both'
                t.grade_levels = "7,8,9,10,11,12"
                if 'Science' in t.subjects: t.subjects += ",General Chemistry,Earth & Life Science"
                if 'Math' in t.subjects: t.subjects += ",Gen. Mathematics,Pre-Calculus"
                if 'English' in t.subjects: t.subjects += ",Oral Communication,21st Century Lit"
                cross_count += 1

        # Dedicated SHS Teachers
        for i in range(idx, idx + 16): 
            t = Teacher(name=f"SHS Specialist {i}", department='SHS', grade_levels="11,12", subjects="Research in Daily Life,Empowerment Tech,ICT Specialization,Creative Writing,Computer Programming", max_hours_per_day=8)
            db.session.add(t)
            teachers.append(t)
            
        db.session.commit()
        print(f"Teachers created (Total: {len(teachers)}).")

        # 5. Create Sections
        # JHS: G7=10, G8=9, G9=7, G10=9
        jhs_secs_cfg = [('7', 10), ('8', 9), ('9', 7), ('10', 9)]
        sections = []
        sec_idx = 0
        for gl, count in jhs_secs_cfg:
            for i in range(1, count + 1):
                name = f"S{i}_G{gl}"
                room_id = classrooms[sec_idx % 35].id 
                adviser_id = teachers[sec_idx % len(teachers)].id
                sec = Section(name=name, department='JHS', grade_level=gl, adviser_id=adviser_id, room_id=room_id)
                db.session.add(sec)
                sections.append(sec)
                sec_idx += 1

        # SHS: 16 sections
        shs_profile = [
            ('11', 'STEM', 2), ('11', 'HUMSS', 3), ('11', 'TVL-ICT', 3),
            ('12', 'STEM', 2), ('12', 'HUMSS', 3), ('12', 'TVL-ICT', 3)
        ]
        shs_sec_idx = 0
        for gl, track, count in shs_profile:
            for i in range(1, count + 1):
                name = f"Section_{track}_{gl}_{i}"
                adviser_id = teachers[(shs_sec_idx + 63) % len(teachers)].id
                room_id = classrooms[35 + (shs_sec_idx % 16)].id
                sec = Section(name=name, department='SHS', grade_level=gl, track=track, adviser_id=adviser_id, room_id=room_id)
                db.session.add(sec)
                sections.append(sec)
                shs_sec_idx += 1

        db.session.commit()
        print(f"Sections created (Total: {len(sections)}).")

        # 6. Global Settings
        settings_to_update = [
            ('school_year', 'S.Y. 2024-2025'),
            ('jhs_am_start', '06:00'), ('jhs_am_end', '12:45'),
            ('jhs_pm_start', '13:00'), ('jhs_pm_end', '19:45'),
            ('shs_start', '07:00'), ('shs_end', '17:00'),
            ('jhs_am_break_start', '09:00'), ('jhs_am_break_end', '09:30'),
            ('jhs_pm_break_start', '16:00'), ('jhs_pm_break_end', '16:30'),
            ('shs_break_start', '09:30'), ('shs_break_end', '10:00'),
            ('shs_lunch_start', '12:00'), ('shs_lunch_end', '13:00'),
            ('jhs_special_enabled', 'no') # Disable Friday Homeroom for initial success
        ]
        
        for k, v in settings_to_update:
            s = Setting.query.filter_by(key=k).first()
            if s: s.value = v
            else: db.session.add(Setting(key=k, value=v))
            
        for gl in ['7', '8']: 
            s = Setting.query.filter_by(key=f'jhs_am_grade_{gl}').first()
            if s: s.value = 'active'
            else: db.session.add(Setting(key=f'jhs_am_grade_{gl}', value='active'))
        
        for gl in ['9', '10']:
            s = Setting.query.filter_by(key=f'jhs_am_grade_{gl}').first()
            if s: s.value = 'inactive'
            else: db.session.add(Setting(key=f'jhs_am_grade_{gl}', value='inactive'))
        
        db.session.commit()
        print("Settings updated.")
        
        print("\nSUCCESS: System repopulated with high-fidelity sample data.")

if __name__ == "__main__":
    populate()
