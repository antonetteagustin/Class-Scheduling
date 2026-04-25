from app import app
from scheduler import generate_schedule

def test_generation():
    with app.app_context():
        success, duration, conflicts, msg = generate_schedule()
        print(f"Success: {success}, Conflicts: {conflicts}, Duration: {duration}s")

if __name__ == '__main__':
    test_generation()
