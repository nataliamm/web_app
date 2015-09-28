from flask import flash
from flask.ext.wtf import Form
from wtforms import StringField, TextField, PasswordField
from models import User


class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            flash('Unknown user')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    username = StringField('username')
    password = PasswordField('new password')
    email = TextField('email address')


class QuestionForm(Form):
    question = StringField('question')


class AnswerForm(Form):
    answer = StringField('answer')
