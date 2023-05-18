import flask_wtf
import wtforms
from flask_wtf.file import FileAllowed
from travel_app.models import Region, Season, Level, Category, ForWho
from travel_app import images
class LoginForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField('email')
    password = wtforms.PasswordField('password')
    name = wtforms.StringField('name')
    remember = wtforms.BooleanField('remember')
    submit = wtforms.SubmitField('submit')


class AddHike(flask_wtf.FlaskForm):
    hike_name = wtforms.StringField('name', [wtforms.validators.DataRequired()])
    length_km = wtforms.FloatField('km', [wtforms.validators.DataRequired()])
    time = wtforms.FloatField('how long')
    region = wtforms.SelectField('regions', choices=[(r.region_id, r.region_name) for r in Region.query.all()])
    level = wtforms.SelectField('level', choices=[(l.level_id, l.level_name) for l in Level.query.all()])
    season = wtforms.SelectField('season', choices=[(s.season_id, s.season_name) for s in Season.query.all()])
    category = wtforms.SelectField('category', choices=[(c.category_id, c.category_name) for c in Category.query.all()])
    people = wtforms.SelectField('for who?', choices=[(p.people_id, p.people_name) for p in ForWho.query.all()])
    water = wtforms.BooleanField('with water?')
    images = wtforms.MultipleFileField(validators=[FileAllowed(images,'Images only!')], label='upload images')
    submit = wtforms.SubmitField('submit')
