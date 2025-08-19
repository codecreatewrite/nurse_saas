from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # For timestamps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nurse.db'  # DB file name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Saves resources
app.config['SECRET_KEY'] = 'supersecretkey123'  # Change to something random/secure later (use secrets module: import secrets; secrets.token_hex(16))
db = SQLAlchemy(app)

# User model (for nurses, with login)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    condition_notes = db.Column(db.Text)
    assigned_nurse_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Patient {self.name}>'

# Vital model (for vitals tracker)
class Vital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    heart_rate = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(20))  # e.g., '120/80'
    temperature = db.Column(db.Float)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Vital for Patient {self.patient_id} at {self.timestamp}>'

# Task model (for nurse tasks)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # e.g., 'pending', 'done'
    assigned_nurse_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task "{self.description}" for Patient {self.patient_id}>'

# MedAdmin model (for eMAR)
class MedAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    med_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    given_time = db.Column(db.DateTime)
    nurse_initials = db.Column(db.String(10))
    status = db.Column(db.String(20), default='scheduled')  # 'given', 'refused', 'not_given'
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<MedAdmin {self.med_name} for Patient {self.patient_id}>'

# Create all tables (run once or when models change)
with app.app_context():
    db.create_all()

# Your existing hello route for testing
@app.route('/')
def hello():
    return "Hello, Nurse App! DB is set up."

if __name__ == '__main__':
    app.run(debug=True)
