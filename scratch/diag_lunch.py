import os
import sys

# Add the project directory to sys.path
sys.path.append(os.getcwd())

from app import app, Setting, Section, ScheduleRun, Schedule, Teacher, Classroom
from datetime import datetime

with app.app_context():
    print("--- Settings Diagnostic ---")
    settings = Setting.query.all()
    for s in settings:
        if 'shs' in s.key or 'lunch' in s.key or 'break' in s.key:
            print(f"{s.key}: '{s.value}'")
    
    print("\n--- Active Run Diagnostic ---")
    active_run = ScheduleRun.query.filter_by(is_active=True).first()
    if active_run:
        print(f"Active Run ID: {active_run.id}, Created At: {active_run.created_at}")
        
        # Check for any schedules overlapping 12:00-13:00 for SHS
        shs_sections = Section.query.filter_by(department='SHS').all()
        for sec in shs_sections:
            over_schedules = Schedule.query.filter_by(run_id=active_run.id, section_id=sec.id).all()
            for sch in over_schedules:
                # Check for 12:00 overlap
                # Simple check: does start_time <= '12:00' and end_time > '12:00'?
                if sch.start_time <= '12:00' and sch.end_time > '12:00':
                    print(f"CONFLICT: Section {sec.name} has Class {sch.subject.name} starting at {sch.start_time} (Overlaps Lunch)")
    else:
        print("No active schedule run found.")
