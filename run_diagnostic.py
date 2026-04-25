import sys
import json
from app import app
from scheduler import generate_schedule
from models import db, ScheduleRun

# DIAGNOSTIC CONFIGURATION
# This script runs the scheduler in 'Halt on First Failure' mode.
# No changes to the database occur.

def run_diagnostics():
    print("INITIALIZING DIAGNOSTIC MODE...")
    print("Rule: Read-only execution, hard stop at first failure, full trace dump.")
    
    with app.app_context():
        # Capture the first diagnostic event
        diagnostic_event = {}

        def diagnostic_callback(p, msg):
            if "[DIAGNOSTIC]" in msg:
                try:
                    # The message will be a JSON string from the scheduler
                    data = json.loads(msg.replace("[DIAGNOSTIC]", "").strip())
                    diagnostic_event.update(data)
                except:
                    pass
            elif p == 5 or p == 10:
                print(f"[{p}%] {msg}")

        # Execute generation in diagnostic mode
        try:
            generate_schedule(phase='all', progress_callback=diagnostic_callback, diagnostic_mode=True)
        except Exception as e:
            if "DIAGNOSTIC_STOP" not in str(e):
                print(f"Error during diagnostics: {e}")

        if diagnostic_event:
            print("\n" + "="*50)
            print("FIRST FAILURE TRACE DUMP")
            print("="*50)
            print(f"Section ID:   {diagnostic_event.get('section_id')}")
            print(f"Section Name: {diagnostic_event.get('section_name')}")
            print(f"Day:          {diagnostic_event.get('day')}")
            print(f"Time Window:  {diagnostic_event.get('window_attempted')}")
            print(f"Classification: {diagnostic_event.get('classification')}")
            print("-" * 30)
            print("CAPACITY DETAILS:")
            print(f"Remaining Shift Capacity: {diagnostic_event.get('remaining_shift_cap')} mins")
            print(f"Required Duration:       {diagnostic_event.get('required_duration')} mins")
            print("-" * 30)
            print("TEACHER POOL STATUS:")
            print(f"Total Qualified:         {diagnostic_event.get('total_qualified')}")
            print(f"Blocked by Slots:        {diagnostic_event.get('blocked_by_slots')}")
            print(f"Blocked by Constraints:  {diagnostic_event.get('blocked_by_constraints')}")
            print("-" * 30)
            print("SEQUENCE AT FAILURE:")
            print(f"Last Success: {diagnostic_event.get('last_success')}")
            print(f"Failing Sub:  {diagnostic_event.get('failing_subject')}")
            print(f"Pending:      {diagnostic_event.get('remaining_subs')}")
            print("="*50)
            
            # ROLLBACK ANY ACCIDENTAL CHANGES
            db.session.rollback()
            print("\nDiagnostic complete. Database state preserved (Read-Only).")
        else:
            print("\nNo failures detected in this run.")

if __name__ == "__main__":
    run_diagnostics()
