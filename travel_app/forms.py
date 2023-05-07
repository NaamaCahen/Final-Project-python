import flask_wtf
import wtforms


class LoginForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField('email')
    password = wtforms.PasswordField('password')
    name = wtforms.StringField('name')
    remember = wtforms.BooleanField('remember')
    submit = wtforms.SubmitField('submit')
