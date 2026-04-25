from app import app
from scheduler import generate_schedule
import time

def test_gen():
    with app.app_context():
        print("Triggering Schedule Generation with new sample data...")
        start = time.time()
        success, duration, conflicts, reason = generate_schedule()
        end = time.time()
        
        print(f"\nGeneration Result:")
        print(f"Success: {success}")
        print(f"Conflicts: {conflicts}")
        print(f"Duration: {duration}s")
        print(f"Total Time: {end - start:.2f}s")
        
        if success:
            print("\nPERFECT: All teachers and sections scheduled without conflicts!")
        else:
            print(f"\nWARNING: Found {conflicts} conflicts. Check logs in Admin Dashboard.")

if __name__ == "__main__":
    test_gen()
