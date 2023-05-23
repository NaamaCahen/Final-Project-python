from travel_app import db
import flask_login


class User(flask_login.UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(64))
    threads = db.relationship('Thread', backref='users', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', lazy='dynamic')

    def get_id(self):
        return (self.user_id)


class Hike(db.Model):
    __tablename__ = 'hikes'
    hike_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hike_name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text)
    length_km = db.Column(db.Float, nullable=False)
    time = db.Column(db.Float, nullable=False)
    km_description = db.Column(db.String(32))
    hours_description = db.Column(db.String(32))
    region = db.Column(db.Integer, db.ForeignKey('regions.region_id'))
    level = db.Column(db.Integer, db.ForeignKey('levels.level_id'))
    season = db.Column(db.Integer, db.ForeignKey('seasons.season_id'))
    summer = db.Column(db.Boolean)
    winter = db.Column(db.Boolean)
    autumn = db.Column(db.Boolean)
    spring = db.Column(db.Boolean)
    rainy_days = db.Column(db.Boolean)
    category = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    for_who = db.Column(db.Integer, db.ForeignKey('people.people_id'))
    water = db.Column(db.Boolean)
    pictures = db.relationship('Picture', backref='hikes', lazy='dynamic')
    threads = db.relationship('Thread', backref='hikes', lazy='dynamic')


class Region(db.Model):
    __tablename__ = 'regions'
    region_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    region_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='regions', lazy='dynamic')


class Level(db.Model):
    __tablename__ = 'levels'
    level_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    level_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='levels', lazy='dynamic')


class Season(db.Model):
    __tablename__ = 'seasons'
    season_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    season_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='seasons', lazy='dynamic')


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='categories', lazy='dynamic')


class ForWho(db.Model):
    __tablename__ = 'people'
    people_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    people_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='people', lazy='dynamic')


class Picture(db.Model):
    __tablename__ = 'pictures'
    picture_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(128), nullable=False)
    hike_id = db.Column(db.Integer, db.ForeignKey('hikes.hike_id'))


class Thread(db.Model):
    __tablename__ = 'threads'
    thread_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    thread_text = db.Column(db.Text)
    hike_id = db.Column(db.Integer, db.ForeignKey('hikes.hike_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    datetime = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='threads', lazy='dynamic')

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_text = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.thread_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
