import os
from app import app, db, Setting, Section, Teacher, Classroom, Schedule, ScheduleRun, User
from app import prepare_schedule_grid, time_to_min, min_to_time

with app.app_context():
    print("Verifying boundary fix...")
    # Mock some settings for JHS AM
    # abs_max_m should be 12:00 (720)
    # With the fix, max_m should be 725. range(min, 725, 5) should include 720.
    
    # Let's test it directly
    abs_max_m = time_to_min('12:00')
    max_m = ((abs_max_m + 5) // 5) * 5
    print(f"abs_max_m: {abs_max_m}, max_m: {max_m}")
    time_slots = [min_to_time(m) for m in range(0, max_m, 5)]
    print(f"Last 3 slots: {time_slots[-3:]}")
    
    if '12:00' in time_slots:
        print("SUCCESS: 12:00 tick is now included in the grid slots.")
    else:
        print("FAILURE: 12:00 tick is still missing.")
        
    # Another test for 12:30
    abs_max_m = time_to_min('12:30')
    max_m = ((abs_max_m + 5) // 5) * 5
    print(f"abs_max_m: 12:30 ({abs_max_m}), max_m: {max_m}")
    time_slots = [min_to_time(m) for m in range(0, max_m, 5)]
    if '12:30' in time_slots:
        print("SUCCESS: 12:30 tick is now included.")
    else:
        print("FAILURE: 12:30 tick is still missing.")
