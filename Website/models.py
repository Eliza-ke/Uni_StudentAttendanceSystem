# . is current folder
from .config import db
from flask_login import UserMixin # to make implementing a user class easier, when inherit
from sqlalchemy.sql import func # get automatic datetime

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period_name = db.Column(db.String(150))
    period_time = db.Column(db.String(150))
    attendances = db.relationship('Attendance')

class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year_name = db.Column(db.String(150))
    students = db.relationship('Student')
    attendances = db.relationship('Attendance')
    
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(150))
    leave_letter = db.Column(db.String(1000))
    status = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    period_id = db.Column(db.Integer, db.ForeignKey("period.id"))


class Student(db.Model, UserMixin): # user object
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    year = db.Column(db.Integer, db.ForeignKey('year.id'))
    batch = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    profile = db.Column(db.String(300))
    attendances = db.relationship('Attendance')
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(150))
    roleCode = db.Column(db.String(150))
    profile = db.Column(db.String(300))


