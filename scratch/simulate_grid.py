import re

def time_to_min(t_str):
    h, m = map(int, t_str.split(':'))
    return h * 60 + m

def min_to_time(m):
    return f"{m//60:02d}:{m%60:02d}"

settings_dict = {
    'jhs_am_grade_7': 'on',
    'jhs_am_start': '06:00',
    'jhs_am_end': '12:30',
    'jhs_am_break_start': '09:00',
    'jhs_am_break_end': '09:30',
    'active_days': 'Monday,Tuesday,Wednesday,Thursday,Friday'
}

days = settings_dict['active_days'].split(',')

def get_shift_bounds(dept, grade_level):
    if dept == 'SHS':
        return settings_dict.get('shs_start', '07:00'), settings_dict.get('shs_end', '17:00')
    else:
        gl = str(grade_level).upper().replace('GRADE', '').strip()
        is_am = settings_dict.get(f'jhs_am_grade_{gl}') in ['active', 'on']
        is_pm = settings_dict.get(f'jhs_pm_grade_{gl}') in ['active', 'on']
        if is_pm and not is_am:
            return settings_dict.get('jhs_pm_start', '12:00'), settings_dict.get('jhs_pm_end', '18:00')
        else:
            return settings_dict.get('jhs_am_start', '06:00'), settings_dict.get('jhs_am_end', '12:00')

# Simulation for Grade 7 Section
st, en = get_shift_bounds('JHS', '7')
abs_min_m = time_to_min(st)
abs_max_m = time_to_min(en)

min_m = (abs_min_m // 5) * 5
max_m = ((abs_max_m + 5) // 5) * 5
time_slots = [min_to_time(m) for m in range(min_m, max_m, 5)]

# Mock current breaks logic
shift = 'AM' # Simplified
prefix = 'jhs_am'
break_times = [(settings_dict.get(f'{prefix}_break_start', '09:00'), settings_dict.get(f'{prefix}_break_end', '09:30'))]

day_breaks = {d: set() for d in days}
for d in days:
    current_breaks = break_times # Simplified
    for b_start, b_end in current_breaks:
        bs_m = time_to_min(b_start)
        be_m = time_to_min(b_end)
        for m in range(bs_m, be_m, 5):
            day_breaks[d].add(min_to_time(m))

grid = {slot: {day: None for day in days} for slot in time_slots}
occupied = {slot: {day: False for day in days} for slot in time_slots}

# Mark breaks
for slot in time_slots:
    for day in days:
        if slot in day_breaks[day]:
            if grid[slot][day] is None and not occupied[slot][day]:
                l_s = settings_dict.get('shs_lunch_start', '12:00')
                is_lunch = (slot == l_s)
                grid[slot][day] = 'LUNCH' if is_lunch else 'BREAK'

# Export sample
for slot in time_slots:
    if '09:00' <= slot <= '09:30':
        print(f"{slot}: {grid[slot]['Monday']}")
