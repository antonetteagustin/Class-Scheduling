from app import app, db, Teacher, Section, Classroom, Schedule, ScheduleRun
from app import prepare_schedule_grid, prepare_condensed_grid

def diag_grid():
    with app.app_context():
        active_run = ScheduleRun.query.filter_by(is_active=True).first()
        if not active_run:
            print("No active run.")
            return
        
        run_id = active_run.id
        schedules = Schedule.query.filter_by(run_id=run_id).all()
        
        # Test Teacher
        teacher = Teacher.query.first()
        if teacher:
             print(f"Testing Teacher: {teacher.name}")
             try:
                 prepare_schedule_grid(teacher.id, 'teacher', schedules)
                 print("  OK")
             except Exception as e:
                 import traceback
                 traceback.print_exc()

        # Test Section
        section = Section.query.first()
        if section:
             print(f"Testing Section: {section.name} (Dept: {section.department})")
             try:
                 if section.department == 'SHS':
                     prepare_condensed_grid(section.id, 'section', schedules)
                 else:
                     prepare_schedule_grid(section.id, 'section', schedules)
                 print("  OK")
             except Exception as e:
                 import traceback
                 traceback.print_exc()

if __name__ == "__main__":
    diag_grid()
