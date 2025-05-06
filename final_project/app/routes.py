from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import CursoForm, ChangePasswordForm
from app.models import db, Curso, User

# Blueprint principal que maneja el dashboard, gestión de cursos y cambio de contraseña
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página de inicio pública (home).
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario autenticado cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Verifica que la contraseña actual sea correcta
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')  # 🔁 Traducido
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra los cursos si no es estudiante.
    """
    if current_user.role.name == 'Student': # Change this for your project
        cursos = Curso.query.all()
    else:
        cursos = Curso.query.filter_by(profesor_id=current_user.id).all()

    return render_template('dashboard.html', cursos=cursos)

@main.route('/cursos', methods=['GET', 'POST'])
@login_required
def cursos():
    """
    Permite crear un nuevo curso. Solo disponible para profesores o admins.
    """
    form = CursoForm()
    if form.validate_on_submit():
        curso = Curso(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            profesor_id=current_user.id
        )
        db.session.add(curso)
        db.session.commit()
        flash("Course created successfully.")  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('curso_form.html', form=form)

@main.route('/cursos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_curso(id):
    """
    Permite editar un curso existente. Solo si es admin o el profesor dueño.
    """
    curso = Curso.query.get_or_404(id)

    # Validación de permisos
    if current_user.role.name not in ['Admin', 'Professor'] or (
        curso.profesor_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to edit this course.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    form = CursoForm(obj=curso)

    if form.validate_on_submit():
        curso.titulo = form.titulo.data
        curso.descripcion = form.descripcion.data
        db.session.commit()
        flash("Course updated successfully.")  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    return render_template('curso_form.html', form=form, editar=True)

@main.route('/cursos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_curso(id):
    """
    Elimina un curso si el usuario es admin o su profesor creador.
    """
    curso = Curso.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Professor'] or (
        curso.profesor_id != current_user.id and current_user.role.name != 'Admin'):
        flash('You do not have permission to delete this course.')  # 🔁 Traducido
        return redirect(url_for('main.dashboard'))

    db.session.delete(curso)
    db.session.commit()
    flash("Course deleted successfully.")  # 🔁 Traducido
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)
