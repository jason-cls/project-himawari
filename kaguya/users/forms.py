from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from kaguya.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=3, max=20)])
    email = StringField('Email', validators=[Email()])
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password', 
        validators=[EqualTo('new_password')])
    image_file = FileField('Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken.\
                 Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:   
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is already taken.\
                 Please choose a different one.')

    def validate_new_password(self, new_password):
        if current_user.check_password(new_password.data):
            raise ValidationError('New password is the same as the existing one.\
             Please choose a different one.')


class AnimeListFilterForm(FlaskForm):
    select_list = SelectField("Select List", choices=[("All", "All"),("Watching", "Watching"), 
        ("Untacked","Untacked"), ("On Hold","On Hold"), 
        ("Plan to Watch", "Plan to Watch"),
        ("Completed","Completed"), ("Dropped", "Dropped")], validators=[DataRequired()])
    submit = SubmitField("Select")

