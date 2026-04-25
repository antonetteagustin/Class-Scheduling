import re

def update_app_py():
    with open('app.py', 'r') as f:
        content = f.read()

    # Define the old block (Union) and the new block (Intersection)
    # We use a regex to match the pattern across the different routes
    
    pattern = r"(elif view_type == '(teacher|classroom)':\n\s+if filter_value == 'All':\n\s+entities = \[t for t in Teacher\.query\.all\(\) if t\.name != 'TBA'\]\n\s+else:\n\s+# Presence-based filtering\n\s+target_depts = \['JHS', 'SHS'\] if filter_value == 'Both' else \[filter_value\]\n\s+active_ids = \{sch\.(teacher_id|room_id) for sch in schedules if sch\.section\.department in target_depts\}\n\s+entities = \[t for t in Teacher\.query\.filter\(Teacher\.id\.in_\(active_ids\)\)\.all\(\) if t\.name != 'TBA'\])"
    
    # Wait, the teacher/classroom pattern is slightly different (Teacher uses [t for ...], Classroom uses Classroom.query.filter...)
    
    # Let's do a simpler string replacement for each occurrence to be safe.
    
    # Teacher Block Pattern
    old_teacher = """    elif view_type == 'teacher':
        if filter_value == 'All':
            entities = [t for t in Teacher.query.all() if t.name != 'TBA']
        else:
            # Presence-based filtering
            target_depts = ['JHS', 'SHS'] if filter_value == 'Both' else [filter_value]
            active_ids = {sch.teacher_id for sch in schedules if sch.section.department in target_depts}
            entities = [t for t in Teacher.query.filter(Teacher.id.in_(active_ids)).all() if t.name != 'TBA']"""

    new_teacher = """    elif view_type == 'teacher':
        if filter_value == 'All':
            entities = [t for t in Teacher.query.all() if t.name != 'TBA']
        elif filter_value == 'Both':
            # Strict Dual-Presence (Intersection of JHS and SHS)
            jhs_ids = {sch.teacher_id for sch in schedules if sch.section.department == 'JHS'}
            shs_ids = {sch.teacher_id for sch in schedules if sch.section.department == 'SHS'}
            active_ids = jhs_ids.intersection(shs_ids)
            entities = [t for t in Teacher.query.filter(Teacher.id.in_(active_ids)).all() if t.name != 'TBA']
        else:
            active_ids = {sch.teacher_id for sch in schedules if sch.section.department == filter_value}
            entities = [t for t in Teacher.query.filter(Teacher.id.in_(active_ids)).all() if t.name != 'TBA']"""

    # Classroom Block Pattern
    old_classroom = """    elif view_type == 'classroom':
        if filter_value == 'All':
            entities = Classroom.query.all()
        else:
            # Presence-based filtering
            target_depts = ['JHS', 'SHS'] if filter_value == 'Both' else [filter_value]
            active_ids = {sch.room_id for sch in schedules if sch.section.department in target_depts}
            entities = Classroom.query.filter(Classroom.id.in_(active_ids)).all()"""

    new_classroom = """    elif view_type == 'classroom':
        if filter_value == 'All':
            entities = Classroom.query.all()
        elif filter_value == 'Both':
            # Strict Dual-Presence (Intersection of JHS and SHS)
            jhs_ids = {sch.room_id for sch in schedules if sch.section.department == 'JHS'}
            shs_ids = {sch.room_id for sch in schedules if sch.section.department == 'SHS'}
            active_ids = jhs_ids.intersection(shs_ids)
            entities = Classroom.query.filter(Classroom.id.in_(active_ids)).all()
        else:
            active_ids = {sch.room_id for sch in schedules if sch.section.department == filter_value}
            entities = Classroom.query.filter(Classroom.id.in_(active_ids)).all()"""

    content = content.replace(old_teacher, new_teacher)
    content = content.replace(old_classroom, new_classroom)

    with open('app.py', 'w') as f:
        f.write(content)
    print("app.py updated successfully.")

if __name__ == "__main__":
    update_app_py()
