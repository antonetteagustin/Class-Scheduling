import sys
import os
import time
sys.path.append(os.getcwd())

from app import app, db
from scheduler import generate_schedule
from models import ScheduleRun, Section, Subject, Teacher

def print_separator():
    print("="*60)

def run_single_test(name, shuffle=False):
    print(f"\n[TEST: {name}]")
    start = time.time()
    success, duration, conflicts, reason = generate_schedule(phase='all', shuffle_sections=shuffle)
    end = time.time()
    
    # Fetch the run that was just created
    run = ScheduleRun.query.order_by(ScheduleRun.id.desc()).first()
    
    print(f"  Duration: {duration:.2f}s (Real: {end-start:.2f}s)")
    print(f"  Success: {success}")
    print(f"  Conflicts: {conflicts}")
    if conflicts > 0:
        print(f"  Conflict Log: {run.conflict_log[:200]}...")
    
    return {
        'success': success,
        'conflicts': conflicts,
        'log': run.conflict_log if run else ""
    }

def analyze_conflicts(results):
    all_logs = " | ".join([r['log'] for r in results if r['log']])
    if not all_logs:
        print("No conflicts to analyze.")
        return

    print("\n[LOG ANALYSIS SUMMARY]")
    conflicts_list = all_logs.split(" | ")
    
    # Basic Frequency
    freq = {}
    for c in conflicts_list:
        if not c.strip(): continue
        # Format is usually "SectionName on Day: Infeasible (N subs)"
        parts = c.split(":")
        if len(parts) > 0:
            key = parts[0].strip() # Section Name on Day
            freq[key] = freq.get(key, 0) + 1
            
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    print("Top Bottlenecks (Section & Day):")
    for key, count in sorted_freq[:10]:
        print(f"  - {key}: {count} occurrences")

def main():
    with app.app_context():
        # Clear previous runs to start fresh
        print("Clearing old ScheduleRuns...")
        ScheduleRun.query.delete()
        db.session.commit()
        
        print_separator()
        print("VALIDATION PHASE: BASELINE GENERATION")
        print_separator()
        baseline = run_single_test("Baseline (Deterministic)", shuffle=False)
        
        print_separator()
        print("VALIDATION PHASE: STRESS TEST (5 RANDOMIZED RUNS)")
        print_separator()
        stress_results = []
        for i in range(1, 6):
            res = run_single_test(f"Stress Run #{i}", shuffle=True)
            stress_results.append(res)
            
        print_separator()
        print("FINAL SUMMARY")
        print_separator()
        all_results = [baseline] + stress_results
        total_conflicts = sum(r['conflicts'] for r in all_results)
        success_rate = sum(1 for r in all_results if r['success']) / len(all_results) * 100
        
        print(f"Total Runs: {len(all_results)}")
        print(f"Full Success Rate: {success_rate:.1f}%")
        print(f"Total Conflict Count Across Runs: {total_conflicts}")
        
        analyze_conflicts(all_results)

if __name__ == "__main__":
    main()
