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

# Add Quiz Route
@app.route('/add_quiz/<chapter_id>/<name>', methods=['GET', 'POST'])
def add_quiz(chapter_id, name):
    if request.method == 'POST':
        quiz_name = request.form.get('quiz_name')
        quiz_date = request.form.get('quiz_date')  # Adding quiz_date
        duration = request.form.get('duration')  # Adding duration
        remarks = request.form.get('remarks')  # Adding remarks
        
        # Convert the duration to time format
        duration = datetime.strptime(duration, '%H:%M').time()
        
        new_quiz = Quiz(
            chapter_id=chapter_id,
            quiz_name=quiz_name,
            quiz_date=datetime.strptime(quiz_date, '%Y-%m-%d').date(),  # Convert string to date
            duration=duration,
            remarks=remarks
        )
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))

    return render_template('add_quiz.html', name=name, chapter_id=chapter_id)

# Edit Quiz Route
@app.route('/edit_quiz/<id>/<name>', methods=['GET', 'POST'])
def edit_quiz(id, name):
    quiz = Quiz.query.get(id)
    if request.method == 'POST':
        quiz.quiz_name = request.form.get('quiz_name')
        quiz.quiz_desc = request.form.get('quiz_description')
        quiz.quiz_date = request.form.get('quiz_date')  # Handle quiz_date
        quiz.duration = request.form.get('duration')  # Handle duration
        quiz.remarks = request.form.get('remarks')  # Handle remarks
        
        # Convert the duration to time format
        quiz.duration = datetime.strptime(quiz.duration, '%H:%M').time()
        
        # Convert quiz_date to date format
        quiz.quiz_date = datetime.strptime(quiz.quiz_date, '%Y-%m-%d').date()
        
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    
    return render_template('edit_quiz.html', name=name, quiz=quiz)

# Delete Quiz Route
@app.route('/delete_quiz/<id>/<name>', methods=['GET', 'POST'])
def delete_quiz(id, name):
    quiz = Quiz.query.get(id)
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
    else:
        flash('Quiz not found!', 'error')
    return redirect(url_for('admin_dashboard', name=name))

#admin quiz dashboard
@app.route('/admin_quiz_dashboard/<name>', methods=['GET', 'POST'])
def admin_quiz_dashboard(name):
    quizzes = Quiz.query.all()
    return render_template('admin_quiz_dashboard.html', name=name, quizzes=quizzes)

@app.route('/add_question/<int:quiz_id>/<name>', methods=['GET', 'POST'])
def add_question(quiz_id, name):
    quiz = Quiz.query.get_or_404(quiz_id)  # Fetch the quiz object by quiz_id

    if request.method == 'POST':
        question_text = request.form['question']
        opt1 = request.form['opt1']
        opt2 = request.form['opt2']
        opt3 = request.form['opt3']
        opt4 = request.form['opt4']
        correct_option = request.form['correct_option']

        # Create a new question and associate it with the quiz
        question = Question(
            quiz_id=quiz.id,
            question=question_text,
            opt1=opt1,
            opt2=opt2,
            opt3=opt3,
            opt4=opt4,
            correct_option=correct_option
        )

        db.session.add(question)
        db.session.commit()

        flash('Question added successfully!', 'success')

        # Check which button was clicked
        if 'add_more' in request.form:
            return redirect(url_for('add_question', quiz_id=quiz_id, name=name))
        else:
            return redirect(url_for('admin_quiz_dashboard', name=name))

    return render_template('add_ques.html', quiz=quiz, name=name)

@app.route('/quiz_questions/<int:quiz_id>/<name>', methods=['GET'])
def quiz_questions(quiz_id, name):
    # Fetch all questions associated with the quiz
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    return render_template('quiz_questions.html', quiz=quiz, questions=questions, name=name)


@app.route('/delete_question/<int:question_id>/<int:quiz_id>/<name>', methods=['GET'])
def delete_question(question_id, quiz_id, name):
    # Fetch the question by ID
    question = Question.query.get_or_404(question_id)
    
    # Delete the question
    db.session.delete(question)
    db.session.commit()

    flash('Question deleted successfully!', 'success')

    return redirect(url_for('quiz_questions', quiz_id=quiz_id, name=name))

@app.route('/edit_question/<int:question_id>/<name>', methods=['GET', 'POST'])
def edit_question(question_id, name):
    question = Question.query.get_or_404(question_id)  

    # Handle form submission to update the question
    if request.method == 'POST':
        question_text = request.form['question']
        opt1 = request.form['opt1']
        opt2 = request.form['opt2']
        opt3 = request.form['opt3']
        opt4 = request.form['opt4']
        correct_option = request.form['correct_option']

        # Update the question details
        question.question = question_text
        question.opt1 = opt1
        question.opt2 = opt2
        question.opt3 = opt3
        question.opt4 = opt4
        question.correct_option = correct_option

        db.session.commit()

        flash('Question updated successfully!', 'success')
        return redirect(url_for('quiz_questions', quiz_id=question.quiz_id, name=name))

    return render_template('edit_ques.html', question=question, name=name)







#user fadboard
@app.route('/user_dashboard/<name>', methods=['GET', 'POST'])
def user_dashboard(name):
    quizzes = Quiz.query.all()
    user = User.query.filter_by(username=name).first()
    today = datetime.today().date()
    return render_template('user_dashboard.html', name=name, quizzes=quizzes, today=today)

#view quiz
@app.route('/view_quiz_details/<int:quiz_id>/<name>', methods=['GET', 'POST'])
def view_quiz(quiz_id, name):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('view_quiz_details.html', name=name, quiz=quiz)

#start quiz
@app.route('/start_quizuser/<int:quiz_id>/<name>', methods=['GET', 'POST'])
def start_quizuser(quiz_id, name):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return render_template('start_quizuser.html', name=name, quiz=quiz, questions=questions)

# Submit Quiz
@app.route('/submit_quiz/<int:quiz_id>/<name>', methods=['POST'])
def submit_quiz(quiz_id, name):
    # Fetch the quiz using quiz_id
    quiz = Quiz.query.filter_by(id=quiz_id).first()  # Correcting this to fetch quiz object
    user = User.query.filter_by(username=name).first()

    if quiz and user:
        total_score = 0
        for question in quiz.questions:  # Accessing questions related to the quiz
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer == question.correct_option:  # Checking correct answer
                total_score += 1

        # Save the score to the database
        newscore = Score(
            quiz_id=quiz_id,  # Corrected to quiz_id
            user_id=user.id,  # Assuming user ID is correctly fetched
            time_taken=datetime.now(),
            total_score=total_score  # Corrected variable name from 'score' to 'total_score'
        )
        db.session.add(newscore)
        db.session.commit()
        user_scores = db.session.query(Score, Quiz).join(Quiz).filter(Score.user_id == user.id).all()


        # Render the score page after submitting
    return render_template('user_score.html', name=name, user_scores=user_scores)

#searching 
def search_subject(search_txt):
    subjects = Subject.query.filter(Subject.subj_name.ilike(f"%{search_txt}%")).all()
    return subjects

def search_chapter(search_txt):
    chapters = Chapter.query.filter(Chapter.chapter_name.ilike(f"%{search_txt}%")).all()
    subjects = [chapter.subjects for chapter in chapters]
    return subjects

def search_quiz_name_or_subject(search_term):
    if search_term:
        # Search quizzes based on subject name or quiz name
        return Quiz.query.join(Chapter).join(Subject).filter(
            (Subject.subj_name.ilike(f'%{search_term}%')) | 
            (Quiz.quiz_name.ilike(f'%{search_term}%'))
        ).all()
    return []



@app.route('/adminsearch/<name>', methods=['GET', 'POST'])
def search(name):
    if request.method == 'POST':
        search_txt = request.form.get('search_txt')
        by_subject = search_subject(search_txt)
        by_chapter = search_chapter(search_txt)
        

        if by_subject:
            return render_template('admin_dashboard.html', name=name, subjects=by_subject)
        elif by_chapter:
            return render_template('admin_dashboard.html', name=name, subjects=by_chapter)
    return redirect(url_for('admin_dashboard', name=name))

from datetime import datetime

@app.route('/usersearch/<name>', methods=['GET', 'POST'])
def usersearch(name):
    if request.method == 'POST':
        search_txt = request.form.get('search_txt')

        if search_txt: 
            quizzes = search_quiz_name_or_subject(search_txt)
            
            today = datetime.now().date()
            
            return render_template('user_dashboard.html', name=name, quizzes=quizzes, today=today)
    return redirect(url_for('user_dashboard', name=name))



#user score
@app.route('/scores/<name>', methods=['GET', 'POST'])
def scores(name):
    user = User.query.filter_by(username=name).first()  
    if not user:
        return redirect(url_for('home'))  

    user_scores = (
        db.session.query(Score, Quiz)  # Query Score and Quiz models
        .join(Quiz, Score.quiz_id == Quiz.id)  # Join with Quiz based on quiz_id
        .filter(Score.user_id == user.id)  # Filter scores by user_id
        .order_by(Score.time_taken.desc())  # Order by time_taken in descending order
        .all()  # Execute the query and fetch all results
    )

    return render_template('score.html', name=name, user_scores=user_scores)  # Render the scores page with the fetched scores

