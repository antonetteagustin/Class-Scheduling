from app import app
from scheduler import generate_schedule
from models import db, ScheduleRun

def run():
    with app.app_context():
        # Clear existing runs
        ScheduleRun.query.delete()
        db.session.commit()
        
        print("Starting Generation...")
        def progress(p, msg):
            print(f"[{p}%] {msg}")
            
        generate_schedule(phase='all', progress_callback=progress)
        
        # Check results
        run = ScheduleRun.query.first()
        if run:
            print(f"\nGeneration Finished. Status: {run.status}")
            print(f"Conflict Log:\n{run.conflict_log}")
        else:
            print("No run created.")

if __name__ == "__main__":
    run()
