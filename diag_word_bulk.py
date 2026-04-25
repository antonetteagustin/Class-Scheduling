from app import app, db, Section, Teacher, Classroom, Schedule, ScheduleRun, Setting
import io
import docx

def diag_word_bulk():
    with app.app_context():
        active_run = ScheduleRun.query.filter_by(is_active=True).first()
        if not active_run:
            print("No active run.")
            return
            
        run_id = active_run.id
        schedules = Schedule.query.filter_by(run_id=run_id).all()
        entities = Section.query.all()
        
        school_name = Setting.query.filter_by(key='school_name').first()
        school_name = school_name.value if school_name else "Andres M. Luciano High School"
        school_year = Setting.query.filter_by(key='school_year').first()
        school_year = school_year.value if school_year else "2023-2024"

        print(f"Num Entities: {len(entities)}")
        
        from app import write_schedule_to_word
        doc = docx.Document()
        
        try:
            for i, entity in enumerate(entities):
                print(f"Writing {entity.name}...")
                write_schedule_to_word(doc, entity, 'section', schedules, school_name, school_year)
                if i < len(entities) - 1:
                    doc.add_page_break()
            
            output = io.BytesIO()
            doc.save(output)
            print("Successfully saved Word doc to memory.")
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    diag_word_bulk()
