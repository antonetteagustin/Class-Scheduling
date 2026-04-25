import sys
import os
sys.path.append(os.getcwd())
from app import app, db
from models import Setting

with app.app_context():
    settings = {s.key: s.value for s in Setting.query.all()}
    keys = sorted(settings.keys())
    for k in keys:
        print(f"{k}: {settings[k]}")
