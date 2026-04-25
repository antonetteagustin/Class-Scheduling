from app import app
from flask import url_for

with app.app_context():
    try:
        u1 = url_for('export_excel_bulk', view_type='section', filter_value='All')
        u2 = url_for('export_word_bulk', view_type='teacher', filter_value='Both')
        u3 = url_for('export_pdf_bulk', view_type='classroom', filter_value='JHS')
        print(f"EXCEL: {u1}")
        print(f"WORD:  {u2}")
        print(f"PDF:   {u3}")
    except Exception as e:
        print(f"ERROR: {e}")
