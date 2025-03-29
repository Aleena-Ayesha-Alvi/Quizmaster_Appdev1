#App Routes

from flask import Flask,render_template,request,redirect,url_for,flash,session
from .models import *
from flask import current_app as app
from datetime import datetime

#many controller and routes here

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('user_name')
        pwd = request.form.get('password')
        usr = User.query.filter_by(username=uname, password=pwd).first()

        if usr:
            if usr.role == 0:  # Admin
                return redirect(url_for('admin_dashboard', name=uname))
            elif usr.role == 1:  # Regular User
                return redirect(url_for('user_dashboard', name=uname))
        return render_template('login.html', err_msg="Invalid User Credentials")

    return render_template('login.html', err_msg="")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form.get('user_name')
        pwd = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')
        college_name = request.form.get('college_name')
        mobile_no = request.form.get('mobile_no')

        # Convert date input to Python date format
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()

        # Check if user already exists
        usr = User.query.filter_by(username=uname).first()
        if usr:
            return render_template('signup.html', err_msg="User Already Exists")

        # Create new user
        new_usr = User(username=uname, password=pwd, name=full_name, qualification=qualification, 
                       date_of_birth=dob_date, college_name=college_name, mobile_no=mobile_no)
        db.session.add(new_usr)
        db.session.commit()

        return render_template('login.html', err_msg="Registration Successful, Please Login")

    return render_template('signup.html', err_msg="")

@app.route('/admin_dashboard/<name>', methods=['GET', 'POST'])
def admin_dashboard(name):
    if request.method == 'POST':
        # Handle form submission for adding subjects, chapters, quizzes, etc.
        pass
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', name=name, subjects=subjects)

@app.route('/user_dashboard/<name>', methods=['GET', 'POST'])
def user_dashboard(name):
    if request.method == 'POST':
        # Handle form submission for taking quizzes, etc.
        pass
    subjects = Subject.query.all()
    return render_template('user_dashboard.html', name=name, subjects=subjects)


# Add Subject Route
@app.route('/add_subjects/<name>', methods=['GET', 'POST'])
def add_subjects(name):
    if request.method == 'POST':
        subj_name = request.form.get('subject_name')
        subj_desc = request.form.get('subject_description')
        new_subject = Subject(subj_name=subj_name, subj_desc=subj_desc)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))

    return render_template('add_subjects.html', name=name)

# Add Chapter Route
@app.route('/add_chapters/<subject_id>/<name>', methods=['GET', 'POST'])
def add_chapters(subject_id, name):
    if request.method == 'POST':
        chapter_name = request.form.get('chapter_name')
        chapt_desc = request.form.get('chapter_description')
        new_chapter = Chapter(subject_id=subject_id, chapter_name=chapter_name, chapt_desc=chapt_desc)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))

    return render_template('add_chapters.html', name=name, subject_id=subject_id)

# Edit Subject Route
@app.route('/edit_subject/<id>/<name>', methods=['GET', 'POST'])
def edit_subject(id, name):
    subject = Subject.query.get(id)
    if request.method == 'POST':
        subject.subj_name = request.form.get('subject_name')
        subject.subj_desc = request.form.get('subject_description')
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    
    return render_template('edit_subject.html', name=name, subject=subject)

# Delete Subject Route
@app.route('/delete_subject/<id>/<name>', methods=['GET', 'POST'])
def delete_subject(id, name):
    subject = Subject.query.get(id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
    return redirect(url_for('admin_dashboard', name=name))

# Edit Chapter Route
@app.route('/edit_chapter/<id>/<name>', methods=['GET', 'POST'])
def edit_chapter(id, name):
    chapter = Chapter.query.get(id)
    if request.method == 'POST':
        chapter.chapter_name = request.form.get('chapter_name')
        chapter.chapt_desc = request.form.get('chapter_description')
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    
    return render_template('edit_chapter.html', name=name, chapter=chapter)

# Delete Chapter Route
@app.route('/delete_chapter/<id>/<name>', methods=['GET', 'POST'])
def delete_chapter(id, name):
    chapter = Chapter.query.get(id)
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
    return redirect(url_for('admin_dashboard', name=name))
