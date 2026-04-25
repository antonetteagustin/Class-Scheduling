from app import app, db, Teacher, Section, Classroom, Schedule, ScheduleRun
from app import prepare_schedule_grid, prepare_condensed_grid

def diag_grid_empty():
    with app.app_context():
        # Test Empty Section
        print("Testing Empty Section (Force Empty Schedules List)")
        try:
             # Pass an empty list of schedules
             prepare_schedule_grid(9999, 'section', [])
             print("  OK (Normal Grid)")
        except Exception as e:
             import traceback
             print("  FAILED (Normal Grid)")
             traceback.print_exc()

        try:
             prepare_condensed_grid(9999, 'section', [])
             print("  OK (Condensed Grid)")
        except Exception as e:
             import traceback
             print("  FAILED (Condensed Grid)")
             traceback.print_exc()

if __name__ == "__main__":
    diag_grid_empty()
