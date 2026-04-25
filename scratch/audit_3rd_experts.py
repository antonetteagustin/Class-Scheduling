import os
import sys
sys.path.append(os.getcwd())
from app import app, db
from models import Teacher

with app.app_context():
    for tid in [17, 19, 20]:
        t = Teacher.query.get(tid)
        print(f"[{t.id}] {t.name} -> GL: {t.grade_levels} | Subs: {t.subjects}")
