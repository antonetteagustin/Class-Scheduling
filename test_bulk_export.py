import unittest
from app import app, db, User, ScheduleRun, Setting
from flask import url_for

class TestBulkExport(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Create user
            user = User(username='admin', password='password', role='admin')
            db.session.add(user)
            # Create active run
            run = ScheduleRun(is_active=True, conflicts=0)
            db.session.add(run)
            # Create setting
            s1 = Setting(key='school_name', value='Test School')
            s2 = Setting(key='school_year', value='2024-2025')
            db.session.add(s1)
            db.session.add(s2)
            db.session.commit()
            self.user_id = user.id

    def login(self):
        return self.client.post('/login', data=dict(
            username='admin',
            password='password'
        ), follow_redirects=True)

    def test_excel_bulk_no_active_run(self):
        self.login()
        with app.app_context():
            run = ScheduleRun.query.filter_by(is_active=True).first()
            run.is_active = False
            db.session.commit()
        
        response = self.client.get('/export_excel_bulk/section/All', follow_redirects=True)
        self.assertIn(b"No active schedule found", response.data)

    def test_excel_bulk_success_empty(self):
        # Even if empty assignments, it should now flash a message instead of returning empty file
        self.login()
        response = self.client.get('/export_excel_bulk/section/All', follow_redirects=True)
        self.assertIn(b"The active schedule run contains no assignments", response.data)

if __name__ == '__main__':
    unittest.main()
