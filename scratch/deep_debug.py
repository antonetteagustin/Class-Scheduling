import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Section, Subject
from flask import request, jsonify

def simulate_edit_section(sec_id):
    print(f"\n--- SIMULATING EDIT SECTION (ID: {sec_id}) ---")
    with app.app_context():
        sec = Section.query.get(sec_id)
        if not sec:
            print("Section not found.")
            return

        with app.test_request_context(
            method='POST',
            data={
                'name': sec.name,
                'grade_level': sec.grade_level,
                'department': sec.department,
                'adviser_id': sec.adviser_id or 'none',
                'room_id': sec.room_id or 'none'
            },
            headers={'X-Requested-With': 'XMLHttpRequest'}
        ):
            from app import edit_section
            # We need to mock current_user since it has @login_required
            from unittest.mock import MagicMock
            import flask_login
            flask_login.current_user = MagicMock()
            flask_login.current_user.role = 'admin'
            flask_login.current_user.is_authenticated = True
            
            try:
                # Bypass @login_required by calling the underlying function if needed, 
                # or just hope the mock works with flask_login.
                # Actually, @login_required checks current_user.
                resp = edit_section(sec_id)
                if hasattr(resp, 'get_data'):
                    print("Status:", resp.status_code)
                    print("Data:", resp.get_data(as_text=True))
                else:
                    print("Response:", resp)
            except Exception as ex:
                print("CRASHED with exception:", type(ex).__name__, ":", ex)
                import traceback
                traceback.print_exc()

def simulate_edit_subject(sub_id):
    print(f"\n--- SIMULATING EDIT SUBJECT (ID: {sub_id}) ---")
    with app.app_context():
        sub = Subject.query.get(sub_id)
        if not sub:
            print("Subject not found.")
            return

        with app.test_request_context(
            method='POST',
            data={
                'name': sub.name + " Test",
                'department': sub.department,
                'duration_mins': str(sub.duration_mins),
                'meetings_per_week': str(sub.meetings_per_week),
                'grade_level': sub.grade_level or '7'
            },
            headers={'X-Requested-With': 'XMLHttpRequest'}
        ):
            from app import edit_subject
            from unittest.mock import MagicMock
            import flask_login
            flask_login.current_user = MagicMock()
            flask_login.current_user.role = 'admin'
            
            try:
                resp = edit_subject(sub_id)
                if hasattr(resp, 'get_data'):
                    print("Status:", resp.status_code)
                    print("Data:", resp.get_data(as_text=True))
                else:
                    print("Response:", resp)
            except Exception as ex:
                print("CRASHED with exception:", type(ex).__name__, ":", ex)
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    # Try ID 1 for both
    simulate_edit_section(1)
    simulate_edit_subject(1)
