import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Section
import json

def test_edit_section():
    with app.app_context():
        # Find a section to edit
        section = Section.query.first()
        if not section:
            print("No sections found to test.")
            return
            
        print(f"Testing edit for Section: {section.name} (ID: {section.id})")
        
        # Simulate a POST request to edit_section
        with app.test_request_context(
            path=f'/admin/sections/edit/{section.id}',
            method='POST',
            data={
                'name': section.name, # Keep same name
                'grade_level': section.grade_level,
                'department': section.department,
                'adviser_id': section.adviser_id or 'none',
                'room_id': section.room_id or 'none'
            },
            headers={'X-Requested-With': 'XMLHttpRequest'}
        ):
            from app import edit_section
            response = edit_section(section.id)
            if hasattr(response, 'get_data'):
                print("Response Data:", response.get_data(as_text=True))
            else:
                print("Response:", response)

if __name__ == '__main__':
    test_edit_section()
