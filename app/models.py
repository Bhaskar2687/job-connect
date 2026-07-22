from app import db, login_manager
from datetime import date
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    company_name = db.Column(db.String(100))   # <-- ADD THIS

    usertype = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    jobs = db.relationship('Jobs', backref='job_applier', lazy=True)
    applications = db.relationship('Application', backref='application_submiter', lazy=True)
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.usertype}', '{self.email}')"
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)

    experience = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    job_type = db.Column(db.String(50), nullable=False)

    apply_link = db.Column(db.String(500), nullable=False)

    industry = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    applications = db.relationship(
        'Application',
        backref='application_jober',
        lazy=True
    )

    def __repr__(self):
        return f"Jobs('{self.id}','{self.title}', '{self.industry}', '{self.date_posted}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    review = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Review('{self.username}', '{self.review}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=date.today())
    degree = db.Column(db.String(20), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    cv = db.Column(db.String(100), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    def __repr__(self):
        return (
            f"Application('{self.id}', '{self.gender}', "
            f"'{self.degree}', '{self.industry}')"
        )

from datetime import datetime

class CareerList(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id'),
        nullable=False
    )

    date_added = db.Column(
        db.DateTime,
        default=date.today
    )

    __table_args__ = (
        db.UniqueConstraint('user_id', 'job_id', name='unique_saved_job'),
    )

    user = db.relationship('User', backref='career_list')
    job = db.relationship('Jobs', backref='career_users')
