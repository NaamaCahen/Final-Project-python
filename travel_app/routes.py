import travel_app
import flask
import flask_login
from werkzeug.security import check_password_hash, generate_password_hash
from travel_app import login_mngr, models, forms, flask_app, db


@login_mngr.user_loader
def load_user(userid):
    userid = int(userid)
    return models.User.query.get(userid)


@flask_app.route('/')
def home():
    return flask.render_template('index.html')


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect('/')
    form = forms.LoginForm()

    if form.validate_on_submit():
        # Retrieve the user with the email
        user = models.User.query.filter_by(email=form.email.data).first()

        if user is None or not check_password_hash(user.password, form.password.data):
            flask.flash('invalid email or password')
            return flask.redirect('/login')

        flask_login.login_user(user, remember=form.remember.data)
        return flask.redirect('/')

    return flask.render_template('login.html',form=form)


@flask_app.route('/signup', methods=['GET','POST'])
def signup():
    form = forms.LoginForm()

    if form.validate_on_submit():
        # if it returns a user , the email already exists
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            flask.flash('Email address already exists')
            return flask.redirect('/signup')

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = models.User(email=form.email.data, name=form.name.data, password=generate_password_hash(form.password.data, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return flask.redirect('login')

    return flask.render_template('signup.html',form=form)


@flask_app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect('/')
