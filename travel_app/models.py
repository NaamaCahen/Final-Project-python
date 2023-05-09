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
