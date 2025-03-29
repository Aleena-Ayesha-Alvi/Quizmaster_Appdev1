from flask_sqlalchemy import SQLAlchemy
from datetime import time, datetime, date

db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Integer, default=1)  # roles: 0 for Admin, 1 for User
    name = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)  # Fix: DateTime type
    college_name = db.Column(db.String(80), nullable=False)
    mobile_no = db.Column(db.String(10), nullable=False)
    
    # Relations
    scores = db.relationship("Score", backref="user", lazy=True, cascade="all,delete")

# Subject model
class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    subj_name = db.Column(db.String(80), nullable=False)
    subj_desc = db.Column(db.String(200))
    
    # Relations
    chapters = db.relationship("Chapter", backref="subjects", lazy=True, cascade="all,delete")

# Chapter model
class Chapter(db.Model):
    __tablename__ = "chapters"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)  # Fixed FK
    chapter_name = db.Column(db.String(80), nullable=False)
    chapt_desc = db.Column(db.String(200))
    
    # Relations
    quizzes = db.relationship("Quiz", backref="chapters", lazy=True, cascade="all,delete")

# Quiz model
class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)  # Fixed FK
    quiz_name = db.Column(db.String(80), nullable=False)
    quiz_date = db.Column(db.Date, nullable=False)  # Fixed Date Type
    duration = db.Column(db.Time, nullable=False)  # Fixed Duration Type
    remarks = db.Column(db.String(200), nullable=False)
    
    # Relations
    questions = db.relationship("Question", backref="quizzes", lazy=True, cascade="all,delete")
    scores = db.relationship("Score", backref="quizzes", lazy=True, cascade="all,delete")

# Question model
class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)  # Fixed FK
    question = db.Column(db.String(255), nullable=False)
    opt1 = db.Column(db.String(255), nullable=False)
    opt2 = db.Column(db.String(255), nullable=False)
    opt3 = db.Column(db.String(255), nullable=False)
    opt4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(255), nullable=False)  # Changed to Integer

# Score model
class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)  # Fixed FK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Fixed FK
    time_taken = db.Column(db.DateTime, nullable=False)
    total_score = db.Column(db.Float, nullable=False)
