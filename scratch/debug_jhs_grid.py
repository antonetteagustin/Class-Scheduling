import sys
import os

# Set up dummy environment if needed, but here we can just try to import app
sys.path.append(os.getcwd())

try:
    from app import app, db, prepare_schedule_grid
    from models import Section, Schedule
    
    with app.app_context():
        # Find a JHS AM section
        section = Section.query.filter_by(department='JHS', grade_level='7').first()
        if not section:
            print("No JHS Grade 7 section found")
            sys.exit(1)
        
        print(f"Testing section: {section.name} ({section.department} {section.grade_level})")
        
        schedules = Schedule.query.filter_by(run_id=Schedule.query.order_by(Schedule.id.desc()).first().run_id if Schedule.query.first() else None).all()
        
        grid_data = prepare_schedule_grid(section.id, 'section', schedules)
        
        print(f"Days: {grid_data['days']}")
        
        # Check Monday, around 09:00
        for slot in grid_data['time_slots']:
            if '09:00' <= slot <= '09:30':
                val = grid_data['grid'][slot]['Monday']
                occ = grid_data['occupied'][slot]['Monday']
                span = grid_data['spans'][slot]['Monday']
                print(f"{slot}: {val} (Occ: {occ}, Span: {span})")

except Exception as e:
    import traceback
    traceback.print_exc()
