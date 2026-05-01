from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    if admin:
        print(f"Admin user exists: {admin.username}")
    else:
        new_admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(new_admin)
        db.session.commit()
        print("Created admin user: admin / admin123")
