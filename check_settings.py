from app import app
from models import Setting

with app.app_context():
    settings = Setting.query.filter(Setting.key.like('jhs_%')).all()
    for s in settings:
        print(f"{s.key}: {s.value}")
