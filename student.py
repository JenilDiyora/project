from unicodedata import name
from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/student_database'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

class studata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact_add = db.Column(db.String(50))
    stud_email = db.Column(db.String(50), unique=True)
    stud_pass = db.Column(db.Integer)
    tran_id = db.relationship('transa', backref='studata', lazy=True)
    schedules_id = db.relationship(
        'schedules', cascade='all, delete', backref='studata', lazy=True)
    
class courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    course_desc = db.Column(db.String(100))
    school_yr = db.Column(db.Integer)
    subject_id = db.relationship(
        'subject', cascade='all, delete', backref='courses', lazy=True)
    schedules_id = db.relationship(
        'schedules', cascade='all, delete', backref='courses', lazy=True)
    
class instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    contact_add = db.Column(db.String(50))
    ins_email = db.Column(db.String(50), unique=True)
    ins_pass = db.Column(db.Integer)
    schedules_id = db.relationship(
         'schedules', cascade='all, delete', backref='instructor', lazy=True)    


class transa(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    trans_name = db.Column(db.String(50))
    trans_date = db.Column(db.DateTime,default=datetime.now)
    std_id = db.Column(db.Integer, db.ForeignKey('studata.id'))
    
    
class subject(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    schedules_id = db.relationship(
        'schedules', cascade='all, delete', backref='subject', lazy=True)

class schedules(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    time_start = db.Column(db.Integer)
    time_end = db.Column(db.Integer)
    day = db.Column(db.DateTime, default=datetime.now)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    std_id = db.Column(db.Integer, db.ForeignKey('studata.id'))
    
