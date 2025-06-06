from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.fields import DateTimeField

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Role',
        choices=[('Admin', 'Admin'), ('Organizador', 'Organizador'), ('Participante', 'Participante')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar un evento
class EventForm(FlaskForm):
    nombre = StringField('Event Name', validators=[DataRequired(), Length(max=150)])
    ubicacion = StringField('Location', validators=[DataRequired(), Length(max=200)])
    fecha_inicio = DateTimeField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    fecha_fin = DateTimeField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    descripcion = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Create Event')