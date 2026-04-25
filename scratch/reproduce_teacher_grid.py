from app import app, db, Teacher, Schedule, ScheduleRun, User, prepare_schedule_grid
import json

with app.app_context():
    active_run = ScheduleRun.query.filter_by(is_active=True).first()
    if not active_run:
        print("No active run")
        exit()

    # Get the first teacher user
    t_user = User.query.filter_by(role='teacher').first()
    if not t_user:
        print("No teacher user")
        exit()

    teacher = Teacher.query.get(t_user.related_id)
    schedules = Schedule.query.filter_by(teacher_id=teacher.id, run_id=active_run.id).all()
    
    print(f"Testing Teacher: {teacher.name} (ID: {teacher.id})")
    print(f"Schedules Found: {len(schedules)}")

    grid_data = prepare_schedule_grid(teacher.id, 'teacher', schedules)
    
    print("\n--- GRID DIAGNOSTICS ---")
    print(f"Days: {grid_data['days']}")
    print(f"Time Slots count: {len(grid_data['time_slots'])}")
    
    filled_cells = []
    for slot in grid_data['time_slots']:
        for day in grid_data['days']:
            sch = grid_data['grid'][slot][day]
            if sch:
                filled_cells.append(f"{slot} {day}: {sch}")
    
    print(f"Filled Cells count: {len(filled_cells)}")
    if filled_cells:
        print("Sample Filled Cells (first 5):")
        for c in filled_cells[:5]:
            print(f"  {c}")
    else:
        print("!!! ERROR: NO CELLS WERE FILLED IN THE GRID !!!")

    print("\n--- OCCUPIED DIAGNOSTICS ---")
    occ_count = sum(1 for slot in grid_data['time_slots'] for day in grid_data['days'] if grid_data['occupied'][slot][day])
    print(f"Occupied Slots count: {occ_count}")
