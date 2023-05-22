from flask import Flask
import flask_migrate
import flask_sqlalchemy
import flask_login
from flask_uploads import configure_uploads,IMAGES,UploadSet
from config import Config

flask_app = Flask(__name__)
flask_app.app_context().push()

flask_app.config.from_object(Config)

login_mngr = flask_login.LoginManager(flask_app)

db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db)

images = UploadSet('images',IMAGES)
configure_uploads(flask_app,images)

from travel_app import routes, models
