from app import app, db, Subject, Teacher, Classroom
import json

with app.test_client() as client:
    with app.app_context():
        # Login is required, so we need to bypass or mock it
        # Easiest way is to just call the route logic directly or use test_request_context
        from flask_login import login_user
        from models import User
        user = User.query.filter_by(role='admin').first()
        
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        sess['_fresh'] = True
    
    # Attempt to reproduce the English edit
    res = client.post('/admin/subjects/edit/1', data={
        'name': 'English - Fixed',
        'department': 'JHS',
        'duration_mins': '60',
        'meetings_per_week': '5',
        'grade_level': '7',
        'requires_lab': '0'
    })
    
    print(f"Status: {res.status_code}")
    print(res.get_data(as_text=True))
