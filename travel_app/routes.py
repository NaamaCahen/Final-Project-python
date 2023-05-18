import werkzeug.utils

import travel_app
import flask
import flask_login
from werkzeug.security import check_password_hash, generate_password_hash
from travel_app import login_mngr, models, forms, flask_app, db, images
from travel_app.models import Region, Hike, Season, Level, Category, Picture, ForWho


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

    return flask.render_template('login.html', form=form)


@flask_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.LoginForm()

    if form.validate_on_submit():
        # if it returns a user , the email already exists
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            flask.flash('Email address already exists')
            return flask.redirect('/signup')

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = models.User(email=form.email.data, name=form.name.data,
                               password=generate_password_hash(form.password.data, method='scrypt'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return flask.redirect('login')

    return flask.render_template('signup.html', form=form)


@flask_app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect('/')


@flask_app.route('/hikes')
def show_hikes():
    hikes = db.session.query(Hike.hike_name,
                             Hike.length_km,
                             Hike.time,
                             Region.region_name,
                             Level.level_name,
                             Season.season_name,
                             Category.category_name,
                             ForWho.people_name,
                             Hike.water).join(Region, Hike.region == Region.region_id) \
                                        .join(Level, Hike.level == Level.level_id)\
                                        .join(Season, Hike.season == Season.season_id)\
                                        .join(Category, Hike.category == Category.category_id)\
                                        .join(ForWho, Hike.for_who == ForWho.people_id).all()

    return flask.render_template('hikes.html', hikes=hikes)


@flask_app.route('/add_hike', methods=['GET', 'POST'])
def add_hike():
    form = forms.AddHike()
    # regions= [(c.category_id, c.category_name) for c in Category.query.all()]
    if form.validate_on_submit():
        new_hike = models.Hike(hike_name=form.hike_name.data, length_km=form.length_km.data, time=form.time.data,
                               region=form.region.data, level=form.level.data, season=form.season.data,
                               category=form.category.data, for_who=form.people.data, water=form.water.data)
        db.session.add(new_hike)
        db.session.commit()
        current_id = models.Hike.query.filter_by(hike_name=new_hike.hike_name).first().hike_id
        if form.images.data[0].filename != '':
            for file in form.images.data:
                filename = images.save(file)
                new_image = models.Picture(url='../static/images/' + filename, hike_id=current_id)
                db.session.add(new_image)
        db.session.commit()
        return 'successfully added!'
    return flask.render_template('add_hike.html', form=form)
