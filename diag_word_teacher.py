from app import app, db, Teacher, Schedule, ScheduleRun, Setting
import io
import docx

def diag_word_teacher():
    with app.app_context():
        teacher = Teacher.query.first()
        if not teacher:
            print("No teacher found.")
            return
            
        active_run = ScheduleRun.query.filter_by(is_active=True).first()
        run_filter = active_run.id if active_run else -1
        schedules = Schedule.query.filter_by(teacher_id=teacher.id, run_id=run_filter).all()
        
        school_name = Setting.query.filter_by(key='school_name').first()
        school_name = school_name.value if school_name else "School"
        school_year = Setting.query.filter_by(key='school_year').first()
        school_year = school_year.value if school_year else "2024"

        print(f"Testing Individual Word for Teacher: {teacher.name}")
        from app import write_schedule_to_word
        doc = docx.Document()
        try:
            write_schedule_to_word(doc, teacher, 'teacher', schedules, school_name, school_year)
            print("  OK")
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    diag_word_teacher()
