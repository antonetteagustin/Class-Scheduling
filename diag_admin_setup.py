import os
from app import app, db, Setting, Section, Teacher, Classroom, Schedule, ScheduleRun, User
from flask import url_for

with app.app_context():
    print("Simulating Admin Setup Route...")
    try:
        settings = {s.key: s.value for s in Setting.query.all()}
        sections = Section.query.all()
        teachers = Teacher.query.all()
        classrooms = Classroom.query.all()
        
        active_run = ScheduleRun.query.filter_by(is_active=True).first()
        schedules = Schedule.query.filter_by(run_id=active_run.id).all() if active_run else []
        runs = ScheduleRun.query.order_by(ScheduleRun.id.desc()).all()
        
        print(f"Data counts: {len(sections)} sections, {len(teachers)} teachers, {len(classrooms)} classrooms")
        
        # Test prepare_schedule_grid
        from app import prepare_schedule_grid
        for s in sections:
             prepare_schedule_grid(s.id, 'section', schedules)
        for t in teachers:
             prepare_schedule_grid(t.id, 'teacher', schedules)
        for r in classrooms:
             prepare_schedule_grid(r.id, 'room', schedules)
             
        print("Backend logic completed successfully.")
        
    except Exception as e:
        import traceback
        print("ERROR:")
        traceback.print_exc()
