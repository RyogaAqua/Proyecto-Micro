from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.models import db, User, Role
from flask_login import login_user, logout_user

# Blueprint de autenticación: gestiona login, registro y logout
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Inicia sesión de un usuario existente si las credenciales son válidas.
    Registra el inicio de sesión en la tabla `login`.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)

            # Registrar el inicio de sesión en la tabla `login`
            db.session.execute(
                """
                INSERT INTO login (user_id) VALUES (:user_id)
                """,
                {"user_id": user.id}
            )
            db.session.commit()

            return redirect(url_for('main.dashboard'))

        flash('Invalid credentials')

    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registra un nuevo usuario y lo almacena en la tabla `signup`.
    """    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Verificar si el nombre de usuario ya existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return render_template('register.html', form=form)

        # Verificar si el correo electrónico ya existe
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already exists. Please use a different one.')
            return render_template('register.html', form=form)

        role = Role.query.filter_by(name=form.role.data).first()

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=role
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        # Registrar el nuevo usuario en la tabla `signup`
        db.session.execute(
            """
            INSERT INTO signup (username, email, password_hash) VALUES (:username, :email, :password_hash)
            """,
            {
                "username": user.username,
                "email": user.email,
                "password_hash": user.password_hash
            }
        )
        db.session.commit()

        flash('User registered successfully.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
    """
    Cierra sesión del usuario actual y redirige al login.
    """
    logout_user()
    return redirect(url_for('auth.login'))
