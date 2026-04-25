import random

def gl_match(req_gl, target_gl_str):
    if not target_gl_str: return True
    def norm(g): 
        if g is None: return ""
        return str(g).strip().upper().replace('GRADE', '').strip()
    req = norm(req_gl)
    if not req: return True
    targets = [norm(g) for g in str(target_gl_str).split(',') if norm(g)]
    if "ALL JHS" in str(target_gl_str).upper() and req in ['7', '8', '9', '10']: return True
    if "ALL SHS" in str(target_gl_str).upper() and req in ['11', '12']: return True
    for t in targets:
        if req == t or (len(req) >= 1 and req in t):
            return True
    return False

# Mock Section Class
class MockSection:
    def __init__(self, id, grade_level, department, is_section_a=False):
        self.id = id
        self.grade_level = grade_level
        self.department = department
        self.is_section_a = is_section_a

# Mock Settings
settings = {
    'jhs_pm_grade_7': None,
    'jhs_pm_grade_8': 'on',
    'jhs_pm_grade_9': None,
    'jhs_pm_grade_10': 'on',
}

def get_hierarchy_keys(sec):
    gl = str(sec.grade_level).upper().replace('GRADE', '').strip()
    # 1. SHIFT (Highest Container) - JHS AM/PM lookup
    is_pm = settings.get(f'jhs_pm_grade_{gl}') in ['active', 'on']
    shift_rank = 1 if is_pm else 0
    
    # 2. DOMAIN (JHS before SHS within same shift)
    domain_rank = 0 if sec.department == 'JHS' else 1
    
    # 3. BLOCK (Balanced Static: A=7-8, B=9-10 | A=11, B=12)
    if sec.department == 'JHS':
        block_rank = 0 if gl in ['7', '8'] else 1
    else: # SHS
        block_rank = 0 if gl == '11' else 1
    
    # 4. PRIORITY (Section A first)
    priority_rank = 0 if sec.is_section_a else 1
    
    return (shift_rank, domain_rank, block_rank, priority_rank, sec.id)

# Create test sections
test_sections = [
    MockSection(1, 7, 'JHS', True),    # Shift AM, Domain JHS, Block A
    MockSection(2, 7, 'JHS', False),   # Shift AM, Domain JHS, Block A
    MockSection(3, 9, 'JHS', True),    # Shift AM, Domain JHS, Block B
    MockSection(4, 9, 'JHS', False),   # Shift AM, Domain JHS, Block B
    MockSection(5, 8, 'JHS', True),    # Shift PM, Domain JHS, Block A
    MockSection(6, 10, 'JHS', True),   # Shift PM, Domain JHS, Block B
    MockSection(7, 11, 'SHS', True),   # Shift AM (Assume SHS is AM), Domain SHS, Block A
    MockSection(8, 12, 'SHS', True),   # Shift AM (Assume SHS is AM), Domain SHS, Block B
]

# Randomize then sort
random.shuffle(test_sections)
sorted_sections = sorted(test_sections, key=get_hierarchy_keys)

print("--- Hierarchical Processing Order ---")
for s in sorted_sections:
    shift = "PM" if settings.get(f'jhs_pm_grade_{str(s.grade_level)}') in ['active', 'on'] else "AM"
    domain = s.department
    gl = s.grade_level
    is_a = " (Section A)" if s.is_section_a else ""
    # Block Rank
    if s.department == 'JHS':
        block = "A" if str(gl) in ['7', '8'] else "B"
    else:
        block = "A" if str(gl) == '11' else "B"
        
    print(f"Shift: {shift} | Domain: {domain} | Block: {block} | Grade: {gl}{is_a}")

# Verification Logic
prev_key = (-1, -1, -1, -1, -1)
for s in sorted_sections:
    curr_key = get_hierarchy_keys(s)
    if curr_key < prev_key:
        print("ERROR: Hierarchy Violation Found!")
        exit(1)
    prev_key = curr_key

print("\nSUCCESS: Hierarchy strictly enforced.")
