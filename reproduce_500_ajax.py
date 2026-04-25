from app import app, db, Subject, Teacher, Classroom
import json

with app.test_client() as client:
    with app.app_context():
        from models import User
        user = User.query.filter_by(role='admin').first()
        
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        sess['_fresh'] = True
    
    # Attempt with AJAX header
    res = client.post('/admin/subjects/edit/1', data={
        'name': 'English - Fixed 2',
        'department': 'JHS',
        'duration_mins': '60',
        'meetings_per_week': '5',
        'grade_level': '7',
        'requires_lab': '0'
    }, headers={'X-Requested-With': 'XMLHttpRequest'})
    
    print(f"Status: {res.status_code}")
    print(res.get_data(as_text=True))
