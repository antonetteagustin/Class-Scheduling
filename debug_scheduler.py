import traceback
from app import app
from scheduler import generate_schedule

with app.app_context():
    try:
        print("Starting schedule generation...")
        result = generate_schedule()
        print("Generation finished.")
        print("Result:", result)
    except Exception as e:
        print("\n!!! SCHEDULER ERROR CAUGHT !!!\n")
        traceback.print_exc()
