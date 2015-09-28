import datetime
from flask import render_template, g, flash, redirect, request, url_for
from app import app
from flask.ext.login import login_user, logout_user, current_user
from forms import LoginForm, RegisterForm, QuestionForm, AnswerForm
from models import User, ROLE_USER, ROLE_ADMIN, Question, Answer
from app import lm, db


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(body=form.question.data)
        db.session.add(question)
        db.session.commit()
        flash('Question was added')
        return redirect(url_for('index'))
    questions_all = Question.query.all()
    return render_template("index.html", title='Home', form=form, questions=questions_all)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(csrf_enabled=False)
    if request.method == "POST" and form.validate():
        user = User(form.username.data, form.password.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/answers', methods=['GET', 'POST'])
def answers():
    form = AnswerForm()
    question_id = 1
    if form.validate_on_submit():
        question_id = 1
        answer = Answer(body=form.answer.data, question_id=question_id)
        db.session.add(answer)
        db.session.commit()
        flash('Answer was added')
        return redirect(url_for('index'))
    answers_all = Answer.query.filter_by(question_id=question_id)
    return render_template("answers.html", title='Answers', form=form, answers=answers_all)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
