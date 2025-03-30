#App Routes

from flask import Flask,render_template,request,redirect,url_for,flash,session
from .models import *
from flask import current_app as app
from datetime import datetime


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user_name')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        date_of_birth = request.form.get('dob')
        college_name = request.form.get('college_name')
        mobile_no = request.form.get('mobile_no')

        # Convert date input to Python date format
        date_of_birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('signup.html', err_msg="User Already Exists")

        # Create new user
        new_user = User(username=username, password=password, name=full_name, qualification=qualification, date_of_birth=date_of_birth_date, college_name=college_name, mobile_no=mobile_no)
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html', err_msg="Registration complete! Now, log in and start exploring")

    return render_template('signup.html', err_msg="")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter_by(username=uname, password=password).first()

        if user:
            if user.role == 0:  # Admin
                return redirect(url_for('admin_dashboard', name=uname))
            elif user.role == 1:  # Regular User
                return redirect(url_for('user_dashboard', name=uname))
        return render_template('login.html', err_msg="Invalid User Name or Password")

    return render_template('login.html', err_msg="")


@app.route('/admin_dashboard/<name>', methods=['GET', 'POST'])
def admin_dashboard(name):
    subjects = Subject.query.all()
    return render_template('admin_dashboard.html', name=name, subjects=subjects)



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
