from app import app, db, Teacher, Subject

def norm_list(s_str):
    if not s_str: return s_str
    parts = [p.strip() for p in s_str.split(',')]
    return ", ".join(parts)

with app.app_context():
    print("Starting Final Data Fix (Tracks)...")
    
    # Update Subjects
    subjects = Subject.query.all()
    sub_count = 0
    for s in subjects:
        # Normalize Grade Level
        # (Assuming it was already done, but let's re-run for safety)
        
        # Normalize Track
        old_track = s.track
        new_track = norm_list(old_track)
        if old_track != new_track:
            s.track = new_track
            sub_count += 1
                
    db.session.commit()
    print(f"Fix finished. Updated tracks for {sub_count} subjects.")
