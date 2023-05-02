from flask import Flask
import flask_migrate
import flask_sqlalchemy
from config import Config

flask_app = Flask(__name__)

flask_app.config.from_object(Config)

db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db)

from travel_app import routes,models
