from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    review = TextAreaField('Your review', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Empty form for button actions
class EmptyForm(FlaskForm):
    submit = SubmitField('')
