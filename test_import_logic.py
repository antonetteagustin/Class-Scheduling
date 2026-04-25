def standardize_gl(gl_val):
    gl = str(gl_val or '7').strip()
    if gl.isdigit():
        gl = f"Grade {gl}"
    if "JHS" in gl.upper() and "ALL" in gl.upper(): gl = "All JHS"
    if "SHS" in gl.upper() and "ALL" in gl.upper(): gl = "All SHS"
    return gl

test_cases = [
    ("7", "Grade 7"),
    ("11", "Grade 11"),
    ("Grade 7", "Grade 7"),
    ("all jhs", "All JHS"),
    ("All SHS", "All SHS"),
    (7, "Grade 7"),
    (None, "Grade 7")
]

for val, expected in test_cases:
    result = standardize_gl(val)
    print(f"Input: {val!r} -> Result: {result!r} | {'PASS' if result == expected else 'FAIL'}")
