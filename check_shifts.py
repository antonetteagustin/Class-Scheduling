from app import app, db, Setting, Section

def check():
    with app.app_context():
        settings = {s.key: s.value for s in Setting.query.all()}
        print("--- Shift Mapping ---")
        for gl in ['7', '8', '9', '10']:
            am = settings.get(f'jhs_am_grade_{gl}')
            pm = settings.get(f'jhs_pm_grade_{gl}')
            print(f"Grade {gl}: AM={am}, PM={pm}")
        
        print("\n--- Sections per Shift ---")
        secs = Section.query.all()
        for s in secs:
            # Determine shift
            shift = "AM"
            if settings.get(f'jhs_pm_grade_{s.grade_level}') in ['active', 'on']:
                shift = "PM"
            # SHS check
            if s.department == 'SHS':
                shift = "SHS (usually AM/Combined)"
            print(f"Sec: {s.name} (Grade {s.grade_level}) -> {shift}")

if __name__ == "__main__":
    check()
