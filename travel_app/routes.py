import datetime

import sqlalchemy
import werkzeug.utils

import travel_app
import flask
import flask_login
from werkzeug.security import check_password_hash, generate_password_hash
from travel_app import login_mngr, models, forms, flask_app, db, images
from travel_app.models import Region, Hike, Level, Category, Picture, ForWho, Thread, Comment, User


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
        return flask.redirect('/hikes')

    return flask.render_template('login.html', form=form)


@flask_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()

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


@flask_app.route('/hikes', methods=['GET', 'POST'])
def show_hikes():
    form = forms.SearchForm()
    thread_form = forms.AddThread()
    comment_form = forms.AddComment()
    hikes = db.session.query(Hike.hike_name, Hike.hike_id,
                             Hike.length_km,
                             Hike.time,
                             Region.region_name,
                             Level.level_name,
                             Hike.summer, Hike.spring, Hike.winter, Hike.autumn, Hike.rainy_days,
                             Hike.text,
                             Category.category_name,
                             ForWho.people_name,
                             Hike.water).join(Region, Hike.region == Region.region_id) \
        .join(Level, Hike.level == Level.level_id) \
        .join(Category, Hike.category == Category.category_id) \
        .join(ForWho, Hike.for_who == ForWho.people_id) \
        .all()
    return flask.render_template('hikes.html', hikes=hikes, form=form, thread_form=thread_form,
                                 comment_form=comment_form)


@flask_app.route('/search', methods=['GET', 'POST'])
def search_hike():
    form = forms.SearchForm()
    # search form
    if form.validate_on_submit():
        region = form.region.data
        level = form.level.data
        season = 'Hike.' + form.season.data
        category = form.category.data
        forwho = form.people.data
        water = form.water.data
        hours_description = form.time.data
        km_description = form.length_km.data
        name = form.hike_name.data
        hikes = db.session.query(Hike.hike_name, Hike.hike_id,
                                 Hike.length_km,
                                 Hike.time,
                                 Region.region_name,
                                 Level.level_name,
                                 Hike.summer, Hike.winter, Hike.autumn, Hike.spring, Hike.rainy_days,
                                 Hike.text,
                                 Category.category_name,
                                 ForWho.people_name,
                                 Hike.water)
        if region != '':
            hikes = hikes.filter_by(region=region)
        if level != '':
            hikes = hikes.filter_by(level=level)
        if category != '':
            hikes = hikes.filter_by(category=category)
        if forwho != '':
            hikes = hikes.filter_by(for_who=forwho)
        if hours_description != '':
            hikes = hikes.filter_by(hours_description=hours_description)
        if km_description != '':
            hikes = hikes.filter_by(km_description=km_description)
        if season != 'Hike.':
            hikes = hikes.filter(eval(season) == True)
        if name != '':
            hikes = hikes.filter(sqlalchemy.func.lower(Hike.hike_name).contains(name))
        hikes = hikes.filter_by(water=water) \
            .join(Region, Hike.region == Region.region_id) \
            .join(Level, Hike.level == Level.level_id) \
            .join(Category, Hike.category == Category.category_id) \
            .join(ForWho, Hike.for_who == ForWho.people_id).all()
        return flask.render_template('hikes.html', hikes=hikes, form=form)


@flask_app.route('/add_hike', methods=['GET', 'POST'])
def add_hike():
    form = forms.AddHikeForm()
    if form.validate_on_submit():
        if form.length_km.data <= 2:
            km_description = 'short'
        elif 3 <= form.length_km.data <= 8:
            km_description = 'mid-length'
        else:
            km_description = 'long'
        if form.time.data <= 2:
            hours_description = 'short'
        elif 3 <= form.time.data <= 8:
            hours_description = 'mid-length'
        else:
            hours_description = 'long'
        new_hike = models.Hike(hike_name=form.hike_name.data, length_km=form.length_km.data, time=form.time.data,
                               region=form.region.data, level=form.level.data, summer=form.summer.data,
                               winter=form.winter.data, km_description=km_description,
                               hours_description=hours_description,
                               autumn=form.autumn.data, spring=form.spring.data, rainy_days=form.rainy_days.data,
                               category=form.category.data, for_who=form.people.data, water=form.water.data,
                               text=form.text.data)
        db.session.add(new_hike)
        db.session.commit()
        current_id = models.Hike.query.filter_by(hike_name=new_hike.hike_name).first().hike_id
        if form.images.data[0].filename != '':
            for file in form.images.data:
                try:
                    filename = images.save(file)
                    new_image = models.Picture(url='../static/images/' + filename, hike_id=current_id)
                    db.session.add(new_image)
                except:
                    flask.flash('not allowed format!')
                    return flask.redirect('/add_hike')
        db.session.commit()
        return 'successfully added!'
    return flask.render_template('add_hike.html', form=form)


@flask_app.route('/hike<hike_id>', methods=['GET', 'POST'])
def show_hike(hike_id):
    add_Thread = forms.AddThread()
    add_comment = forms.AddComment()
    hike = db.session.query(Hike.hike_id, Hike.hike_name, Hike.length_km, Hike.time, Region.region_name,
                            Level.level_name, Hike.summer, Hike.winter, Hike.autumn, Hike.spring, Hike.rainy_days,
                            Category.category_name, ForWho.people_name, Hike.water).filter_by(hike_id=hike_id).join(
        Region, Hike.region == Region.region_id).join(Level, Hike.level == Level.level_id).join(Category,
                                                                                                Hike.category == Category.category_id).join(
        ForWho, Hike.for_who == ForWho.people_id).first()
    pictures = Picture.query.filter_by(hike_id=hike.hike_id)
    threads = db.session.query(Thread.thread_id, Thread.title, Thread.thread_text, Thread.datetime,
                               User.name).filter_by(hike_id=hike_id).join(User, Thread.user_id == User.user_id).all()
    comments = db.session.query(Comment.comment_text, User.name, Comment.datetime, Comment.thread_id).join(User,
                                                                                                           Comment.user_id == User.user_id).all()
    if add_Thread.validate_on_submit():
        new_thread = Thread(title=add_Thread.title.data, thread_text=add_Thread.text.data,
                            user_id=flask_login.current_user.user_id, hike_id=add_Thread.hike_id.data,
                            datetime=datetime.datetime.now())
        db.session.add(new_thread)
        db.session.commit()
        return flask.redirect('/hike' + hike_id + '#' + str(new_thread.thread_id))

    if add_comment.validate_on_submit():
        new_comment = Comment(comment_text=add_comment.comment_text.data, datetime=datetime.datetime.now(),
                              thread_id=add_comment.thread_id.data, user_id=flask_login.current_user.user_id)
        db.session.add(new_comment)
        db.session.commit()
        return flask.redirect('/hike' + hike_id + '#' + str(add_comment.thread_id.data))
    return flask.render_template('hike.html', hike=hike, pictures=pictures, threads=threads, comments=comments,
                                 add_thread=add_Thread, add_comment=add_comment)
