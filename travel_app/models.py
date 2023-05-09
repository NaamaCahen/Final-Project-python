from travel_app import db
import flask_login


class User(flask_login.UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(64))

    def get_id(self):
        return (self.user_id)


class Hike(db.Model):
    __tablename__ = 'hikes'
    hike_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hike_name = db.Column(db.String(100), nullable=False)
    length_km = db.Column(db.Float, nullable=False)
    time = db.Column(db.Float, nullable=False)
    region = db.Column(db.Integer, db.ForeignKey('region.region_id'))
    level = db.Column(db.Integer, db.ForeignKey('level.level_id'))
    season = db.Column(db.Integer, db.ForeignKey('season.season_id'))
    category = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    for_who = db.Column(db.Integer, db.ForeignKey('people.people_id'))
    water = db.Column(db.Boolean)
    pictures = db.relationship('Picture', backref='hike', lazy='dynamic')


class Region(db.Model):
    __tablename__ = 'regions'
    region_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    region_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='region', lazy='dynamic')


class Level(db.Model):
    __tablename__ = 'levels'
    level_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    level_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='level', lazy='dynamic')


class Season(db.Model):
    __tablename__ = 'seasons'
    season_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    season_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='season', lazy='dynamic')


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='category', lazy='dynamic')


class ForWho(db.Model):
    __tablename__ = 'people'
    people_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    people_name = db.Column(db.String(32), nullable=False)
    hikes = db.relationship('Hike', backref='people', lazy='dynamic')


class Picture(db.Model):
    __tablename__ = 'pictures'
    picture_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(128), nullable=False)
    hike_id = db.Column(db.Integer, db.ForeignKey('hike.hike_id'))
