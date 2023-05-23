import flask_wtf
import wtforms
from flask_wtf.file import FileAllowed
from travel_app.models import Region, Level, Category, ForWho
from travel_app import images


class LoginForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField('email')
    password = wtforms.PasswordField('password')
    name = wtforms.StringField('name')
    remember = wtforms.BooleanField('remember')
    submit = wtforms.SubmitField('submit')


class AddHikeForm(flask_wtf.FlaskForm):
    hike_name = wtforms.StringField('name', [wtforms.validators.DataRequired()])
    length_km = wtforms.FloatField('km', [wtforms.validators.DataRequired()])
    time = wtforms.FloatField('how long')
    text = wtforms.TextAreaField('hike description')
    region = wtforms.SelectField('regions', choices=[(r.region_id, r.region_name) for r in Region.query.all()])
    level = wtforms.SelectField('level', choices=[(l.level_id, l.level_name) for l in Level.query.all()])
    # season = wtforms.SelectField('season', choices=[(s.season_id, s.season_name) for s in Season.query.all()])
    summer = wtforms.BooleanField('summer')
    winter = wtforms.BooleanField('winter')
    autumn = wtforms.BooleanField('autumn')
    spring = wtforms.BooleanField('spring')
    rainy_days = wtforms.BooleanField('rainy days')
    category = wtforms.SelectField('category', choices=[(c.category_id, c.category_name) for c in Category.query.all()])
    people = wtforms.SelectField('for who?', choices=[(p.people_id, p.people_name) for p in ForWho.query.all()])
    water = wtforms.BooleanField('with water?')
    images = wtforms.MultipleFileField(validators=[FileAllowed(images, 'Images only!')], label='upload images')
    submit = wtforms.SubmitField('submit')


lengths = ['','short', 'mid-length', 'long']


class SearchForm(flask_wtf.FlaskForm):
    length_km = wtforms.SelectField('km', choices=lengths)
    time = wtforms.SelectField('how long', choices=lengths)
    hike_name = wtforms.StringField('name')
    region = wtforms.SelectField('regions', choices=[("", "")]+[(r.region_id, r.region_name) for r in Region.query.all()])
    level = wtforms.SelectField('level', choices=[("", "")]+[(l.level_id, l.level_name) for l in Level.query.all()])
    season = wtforms.SelectField('season', choices=['','summer', 'winter', 'autumn', 'spring'])
    category = wtforms.SelectField('category', choices=[("", "")]+[(c.category_id, c.category_name) for c in Category.query.all()])
    people = wtforms.SelectField('for who?', choices=[("", "")]+[(p.people_id, p.people_name) for p in ForWho.query.all()])
    water = wtforms.BooleanField('with water?')
    search = wtforms.SubmitField('search')


class AddThread(flask_wtf.FlaskForm):
    title = wtforms.StringField('title',[wtforms.validators.DataRequired()])
    text = wtforms.TextAreaField('thread text')
    hike_id = wtforms.IntegerField('hike id')
    add = wtforms.SubmitField('add')


class AddComment(flask_wtf.FlaskForm):
    comment_text = wtforms.TextAreaField('comment text')
    thread_id = wtforms.IntegerField('thread id')
    add_comment = wtforms.SubmitField('add')
