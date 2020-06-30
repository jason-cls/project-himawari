from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    review = TextAreaField('Your review', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Empty form for button actions
class EmptyForm(FlaskForm):
    submit = SubmitField('')


class EpisodeForm(FlaskForm):
    eps_count = IntegerField()
