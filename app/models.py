import datetime
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column('password', db.String(10))
    email = db.Column(db.String(120), index=True)
    authenticated = db.Column(db.Boolean, default=False)
    questions = db.relationship('Question', backref='author', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.datetime.now()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return '<Question %r>' % (self.body)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __init__(self, body, question_id):
        self.body = body
        self.question_id = question_id

    def __repr__(self):
        return '<Answer %r>' % (self.body)
