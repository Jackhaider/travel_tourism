from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, NumberRange

class DestinationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description')
    image = StringField('Image URL')
    submit = SubmitField('Save')

class BookingForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    num_people = IntegerField('Number of people', validators=[DataRequired(), NumberRange(min=1)])
    date = StringField('Travel date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Book Now')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
