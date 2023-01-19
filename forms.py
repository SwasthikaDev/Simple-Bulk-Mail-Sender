from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators, FileField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.Length(min=8)])


class TemplateEditorForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[
                        validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[
                             validators.DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     validators.DataRequired()])


class FileUploadForm(FlaskForm):
    file = FileField('Upload File')
    submit = SubmitField('Upload')


class EditUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Save")
