from app import app, db, Section, Teacher, Classroom, Schedule, ScheduleRun
import io
import pandas as pd

def reproduce_excel_error():
    with app.app_context():
        # Get an active run
        active_run = ScheduleRun.query.filter_by(is_active=True).first()
        if not active_run:
            print("No active run found for reproduction.")
            return
            
        view_type = 'section'
        filter_value = 'All'
        
        run_filter = active_run.id
        schedules = Schedule.query.filter_by(run_id=run_filter).all()
        entities = Section.query.all()
        
        print(f"Run ID: {run_filter}")
        print(f"Schedules: {len(schedules)}")
        print(f"Entities: {[e.name for e in entities]}")
        
        output = io.BytesIO()
        try:
            from app import write_schedule_to_excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for entity in entities:
                    print(f"Writing {entity.name}...")
                    write_schedule_to_excel(writer, entity, view_type, schedules)
            print("Successfully written to memory.")
        except Exception as e:
            import traceback
            print("FAILED with exception:")
            traceback.print_exc()

if __name__ == "__main__":
    reproduce_excel_error()
