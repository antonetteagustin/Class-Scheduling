import os
from app import app
from models import db, Teacher, Classroom, Section, Subject, Setting, Schedule, ScheduleRun, User
from werkzeug.security import generate_password_hash

def populate():
    with app.app_context():
        print("Starting Database Reset & Repopulation (Sample Input)...")
        
        # 1. Clear Data (Order matters for foreign keys)
        Schedule.query.delete()
        ScheduleRun.query.delete()
        Section.query.delete()
        Subject.query.delete()
        Teacher.query.delete()
        Classroom.query.delete()
        Setting.query.delete()
        # Keep admin user, delete others
        User.query.filter(User.role != 'admin').delete()
        db.session.commit()
        print("Database and Settings cleared.")

        # 2. Create Subjects
        # JHS Core (Approx 45-60 mins based on previous patterns)
        jhs_subs = [
            ('Filipino', 60, 4), ('English', 60, 4), ('Math', 60, 4), ('Science', 60, 4),
            ('Araling Panlipunan', 60, 3), ('TLE', 60, 4), ('Values Education', 60, 2), ('MAPEH', 60, 4)
        ]
        for name, dur, freq in jhs_subs:
            sub = Subject(name=name, department='JHS', duration_mins=dur, meetings_per_week=freq, grade_level='7,8,9,10')
            db.session.add(sub)

        # SHS Core
        shs_core = [
            ('Oral Communication', 60, 4), ('Gen. Mathematics', 60, 4), ('Statistics and Probability', 60, 4),
            ('21st Century Literature', 60, 4), ('Contemporary Philippine Arts', 60, 4), 
            ('Media and Information Literacy', 60, 4), ('Physical Education and Health', 60, 2),
            ('Personal Development', 60, 4), ('Understanding Culture, Society and Politics', 60, 4)
        ]
        for name, dur, freq in shs_core:
            sub = Subject(name=name, department='SHS', duration_mins=dur, meetings_per_week=freq, grade_level='11,12', track='All')
            db.session.add(sub)

        # SHS Specialized Items
        shs_spec = [
            # STEM
            ('Pre-Calculus', 60, 4, 'STEM', False), ('Basic Calculus', 60, 4, 'STEM', False),
            ('General Biology 1', 60, 4, 'STEM', True), ('General Physics 1', 60, 4, 'STEM', True),
            ('General Chemistry 1', 60, 4, 'STEM', True),
            # HUMSS
            ('Creative Writing', 60, 4, 'HUMSS', False), ('Introduction to World Religions', 60, 4, 'HUMSS', False),
            ('Disciplines and Ideas in Social Sciences', 60, 4, 'HUMSS', False),
            # TVL-ICT
            ('Computer Programming', 60, 4, 'TVL-ICT', True), ('Animation', 60, 4, 'TVL-ICT', True),
            ('Computer System Servicing', 60, 4, 'TVL-ICT', True), ('Empowerment Technologies', 60, 4, 'TVL-ICT', True)
        ]
        for name, dur, freq, track, lab in shs_spec:
            sub = Subject(name=name, department='SHS', duration_mins=dur, meetings_per_week=freq, grade_level='11,12', track=track, requires_lab=lab)
            db.session.add(sub)
        
        db.session.commit()
        print("Subjects created.")

        # 3. Create Classrooms
        # JHS Rooms (35 for 35 sections)
        classrooms_jhs = []
        for i in range(1, 36):
            c = Classroom(name=f"JHS Room {i}", room_type='Room', building='JHS')
            db.session.add(c)
            classrooms_jhs.append(c)
        
        # SHS Rooms (16)
        classrooms_shs = []
        for i in range(1, 17):
            c = Classroom(name=f"SHS Room {i}", room_type='Room', building='SHS')
            db.session.add(c)
            classrooms_shs.append(c)
            
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
        jhs_counts = {
            'Filipino': 8, 'English': 7, 'Math': 9, 'Science': 9, 
            'Araling Panlipunan': 5, 'TLE': 12, 'Values Education': 6, 'MAPEH': 8
        }
        
        t_idx = 1
        for sub_name, count in jhs_counts.items():
            for _ in range(count):
                t = Teacher(name=f"JHS Teacher {t_idx} ({sub_name})", department='JHS', grade_levels="7,8,9,10", subjects=sub_name, max_hours_per_day=6)
                db.session.add(t)
                teachers.append(t)
                t_idx += 1
        
        # Head Teachers (7, no teaching load)
        for i in range(1, 8):
            ht = Teacher(name=f"Head Teacher {i}", department='Both', grade_levels="7,8,9,10,11,12", subjects="Administrative", max_hours_per_day=0)
            db.session.add(ht)
            teachers.append(ht)

        # Dedicated SHS Teachers (26)
        shs_dedicated = []
        for i in range(1, 27):
            t = Teacher(name=f"SHS Teacher {i}", department='SHS', grade_levels="11,12", subjects="Oral Communication", max_hours_per_day=8) # Default subject
            db.session.add(t)
            shs_dedicated.append(t)
            teachers.append(t)

        # Implement Teacher Sharing: Select some JHS teachers to be 'Both'
        # We'll take 3 Math, 3 Science, 3 English
        share_count = 0
        for t in teachers:
            if t.department == 'JHS' and t.subjects in ['Math', 'Science', 'English'] and share_count < 9:
                t.department = 'Both'
                t.grade_levels = "7,8,9,10,11,12"
                if t.subjects == 'Math': t.subjects += ",Gen. Mathematics,Pre-Calculus"
                if t.subjects == 'Science': t.subjects += ",Gen. Chemistry,General Biology 1"
                if t.subjects == 'English': t.subjects += ",Oral Communication,21st Century Literature"
                share_count += 1

        db.session.commit()
        print(f"Teachers created (Total: {len(teachers)}).")

        # 5. Create Sections
        # JHS: G7=10, G8=9, G9=7, G10=9 (Total 35)
        jhs_secs_cfg = [('7', 10), ('8', 9), ('9', 7), ('10', 9)]
        sec_idx = 0
        for gl, count in jhs_secs_cfg:
            for i in range(1, count + 1):
                name = f"S{i}_G{gl}"
                room = classrooms_jhs[sec_idx]
                # Pick a teacher from relevant grade level for adviser
                adviser = teachers[sec_idx % len(teachers)] 
                sec = Section(name=name, department='JHS', grade_level=gl, adviser_id=adviser.id, room_id=room.id)
                db.session.add(sec)
                sec_idx += 1

        # SHS: Gr11: 2 STEM, 3 HUMSS, 3 TVL-ICT; Gr12: 2 STEM, 3 HUMSS, 3 TVL-ICT (Total 16)
        shs_profile = [
            ('11', 'STEM', 2), ('11', 'HUMSS', 3), ('11', 'TVL-ICT', 3),
            ('12', 'STEM', 2), ('12', 'HUMSS', 3), ('12', 'TVL-ICT', 3)
        ]
        shs_sec_idx = 0
        for gl, track, count in shs_profile:
            for i in range(1, count + 1):
                name = f"Section_{track}_{gl}_{i}"
                room = classrooms_shs[shs_sec_idx]
                adviser = shs_dedicated[shs_sec_idx % len(shs_dedicated)]
                sec = Section(name=name, department='SHS', grade_level=gl, track=track, adviser_id=adviser.id, room_id=room.id)
                db.session.add(sec)
                shs_sec_idx += 1

        db.session.commit()
        print(f"Sections created (Total JHS: 35, Total SHS: 16).")

        # 6. Global Settings
        settings_to_update = [
            ('school_name', 'Andres M. Luciano High School'),
            ('school_year', 'S.Y. 2024-2025'),
            ('jhs_am_start', '06:00'), ('jhs_am_end', '12:45'),
            ('jhs_pm_start', '13:00'), ('jhs_pm_end', '19:45'),
            ('shs_start', '07:00'), ('shs_end', '17:00'),
            ('jhs_am_break_start', '09:00'), ('jhs_am_break_end', '09:30'),
            ('jhs_pm_break_start', '16:00'), ('jhs_pm_break_end', '16:30'),
            ('shs_break_start', '09:30'), ('shs_break_end', '10:00'),
            ('shs_lunch_start', '12:00'), ('shs_lunch_end', '13:00'),
            ('jhs_special_enabled', 'no'),
            ('available_tracks', 'STEM,HUMSS,TVL-ICT')
        ]
        
        for k, v in settings_to_update:
            s = Setting.query.filter_by(key=k).first()
            if s: s.value = v
            else: db.session.add(Setting(key=k, value=v))
            
        # Set Grade 7 & 8 to AM shift, 9 & 10 to PM shift (Typical DepEd)
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
        
        # 7. Create User accounts for teachers and sections
        # This is already handled in app.py's confirm_import or teacher/section creation logic normally,
        # but since we are using direct DB calls, we should ensure they exist.
        for t in Teacher.query.all():
            if not User.query.filter_by(username=t.name).first():
                db.session.add(User(username=t.name, password=generate_password_hash('123456'), role='teacher', related_id=t.id))
        for s in Section.query.all():
            if not User.query.filter_by(username=s.name).first():
                db.session.add(User(username=s.name, password=generate_password_hash('123456'), role='student', related_id=s.id))
        
        db.session.commit()
        print("User accounts created.")
        
        print("\nSUCCESS: System populated with requested sample data.")

if __name__ == "__main__":
    populate()
