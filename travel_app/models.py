from travel_app import db
import flask_login


class User(flask_login.UserMixin, db.Model):
    user_id = db.Column()
