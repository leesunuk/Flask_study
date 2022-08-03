from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired(), Length(4, 30)])
    password1 = PasswordField('password', validators=[DataRequired(), Length(4, 30)])
    password2 = PasswordField("'password again", validators=[DataRequired()])
    
class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    
class PostForm(FlaskForm):
    title = StringField('tittle', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])