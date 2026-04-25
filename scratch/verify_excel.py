import pandas as pd
import os
import json

# Create a sample excel file
data = {
    'Teacher Name': ['John Doe', 'Jane Smith'],
    'Dept': ['JHS', 'SHS'],
    'Max Hours': [6, 8],
    'Grades': ['7,8', '11,12'],
    'Is Master?': ['No', 'Yes'],
    'Preferred Days': ['Mon-Fri', 'MWF'],
    'Subjects': ['Math, Science', 'Physics']
}

df = pd.DataFrame(data)
test_file = 'test_import.xlsx'
df.to_excel(test_file, index=False)

print(f"Created {test_file}")

# Simulate smart mapping config from app.py
smart_mappings = {
    'teachers': {
        'name': ['name', 'full name', 'teacher name', 'teacher', 'instructor'],
        'department': ['department', 'dept', 'level'],
        'max_hours_per_day': ['max hours', 'max hours per day', 'hours', 'limit'],
        'grade_levels': ['grade levels', 'grades', 'handled grades'],
        'is_master': ['master teacher', 'master', 'is master', 'master?'],
        'preferred_days': ['preferred days', 'days', 'schedule preference'],
        'subjects': ['subjects', 'assigned subjects']
    }
}

def get_field_match(header, module_map):
    if pd.isna(header): return None
    header = str(header).lower().replace(' ', '').replace('_', '').replace('-', '').strip()
    for field, aliases in module_map.items():
        f_clean = field.lower().replace(' ', '').replace('_', '').replace('-', '')
        if header == f_clean:
            return field
        for alias in aliases:
            a_clean = alias.lower().replace(' ', '').replace('_', '').replace('-', '')
            if header == a_clean:
                return field
    return None

try:
    # Test reading the file
    df_read = pd.read_excel(test_file, engine='openpyxl')
    print("Successfully read Excel file using openpyxl.")
    
    module_map = smart_mappings['teachers']
    col_to_field = {}
    for col in df_read.columns:
        matched_field = get_field_match(col, module_map)
        if matched_field:
            col_to_field[col] = matched_field
            print(f"Mapped header '{col}' -> '{matched_field}'")
        else:
            print(f"Failed to map header '{col}'")

    final_data = []
    for _, row in df_read.iterrows():
        mapped_row = {field: row[col] for col, field in col_to_field.items() if not pd.isna(row[col])}
        final_data.append(mapped_row)

    print("\nParsed Data Sample:")
    print(json.dumps(final_data, indent=2))

    # Clean up
    os.remove(test_file)
    print(f"\nRemoved {test_file}")

except Exception as e:
    print(f"Error: {e}")
