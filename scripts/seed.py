from app import app, db, User

with app.app_context():
    user = User(username='nurse1', password_hash='hash123')
    db.session.add(user)
    db.session.commit()
    print("User added:", user)
