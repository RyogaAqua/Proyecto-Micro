from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.forms import CursoForm, ChangePasswordForm, EventForm
from app.models import db, Curso, User, Role, Evento
import logging
from datetime import datetime

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
            flash('Current password is incorrect.')
            return render_template('cambiar_password.html', form=form)

        # Actualiza la contraseña y guarda
        current_user.set_password(form.new_password.data)
        try:
            db.session.commit()
            flash('✅ Password updated successfully.')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating password: {str(e)}', 'danger')

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra todos los eventos.
    """
    eventos = Evento.query.all()
    return render_template('events.html', eventos=eventos, current_user=current_user)

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("You do not have permission to view this page.")
        return redirect(url_for('main.dashboard'))

    # Obtener instancias completas de usuarios con sus roles (no usar .add_columns)
    usuarios = User.query.join(User.role).all()

    return render_template('usuarios.html', usuarios=usuarios)

@main.route('/eventos', methods=['GET'])
def listar_eventos():
    """
    Retorna una lista de todos los eventos.
    """
    eventos = Evento.query.all()
    data = [
        {
            'id': evento.id,
            'nombre': evento.nombre,
            'ubicacion': evento.ubicacion,
            'fecha_inicio': evento.fecha_inicio,
            'fecha_fin': evento.fecha_fin,
            'descripcion': evento.descripcion
        }
        for evento in eventos
    ]
    return jsonify(data), 200

@main.route('/eventos/<int:id>', methods=['GET'])
def obtener_evento(id):
    """
    Retorna un evento específico por su ID.
    """
    evento = Evento.query.get_or_404(id)
    data = {
        'id': evento.id,
        'nombre': evento.nombre,
        'ubicacion': evento.ubicacion,
        'fecha_inicio': evento.fecha_inicio,
        'fecha_fin': evento.fecha_fin,
        'descripcion': evento.descripcion
    }
    return jsonify(data), 200

@main.route('/eventos', methods=['POST'])
def crear_evento():
    """
    Crea un nuevo evento.
    Espera un JSON con 'nombre', 'ubicacion', 'fecha_inicio', 'fecha_fin', y opcionalmente 'descripcion'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    evento = Evento(
        nombre=data.get('nombre'),
        ubicacion=data.get('ubicacion'),
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        descripcion=data.get('descripcion')
    )

    db.session.add(evento)
    db.session.commit()

    return jsonify({'message': 'Evento creado', 'id': evento.id}), 201

@main.route('/eventos/<int:id>', methods=['PUT'])
def actualizar_evento(id):
    """
    Actualiza un evento existente.
    """
    evento = Evento.query.get_or_404(id)
    data = request.get_json()

    evento.nombre = data.get('nombre', evento.nombre)
    evento.ubicacion = data.get('ubicacion', evento.ubicacion)
    evento.fecha_inicio = data.get('fecha_inicio', evento.fecha_inicio)
    evento.fecha_fin = data.get('fecha_fin', evento.fecha_fin)
    evento.descripcion = data.get('descripcion', evento.descripcion)

    db.session.commit()

    return jsonify({'message': 'Evento actualizado', 'id': evento.id}), 200

@main.route('/eventos/<int:id>', methods=['POST', 'DELETE'])
@login_required
def eliminar_evento(id):
    """
    Permite eliminar un evento dependiendo del rol del usuario.
    """
    evento = Evento.query.get_or_404(id)

    # Verificar permisos
    if current_user.role.name == 'Usuario':
        flash('You do not have permission to delete events.', 'danger')
        return redirect(url_for('main.dashboard'))

    if current_user.role.name == 'Organizador' and evento.organizador_id != current_user.id:
        flash('You do not have permission to delete this event.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(evento)
    db.session.commit()

    flash('Event deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/eventos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_evento_web():
    """
    Renderiza un formulario para crear un nuevo evento desde la interfaz web.
    """
    logging.basicConfig(level=logging.DEBUG)
    form = EventForm()

    if form.validate_on_submit():
        try:
            logging.info("Attempting to create a new event.")
            logging.debug(f"Form data received: {form.data}")
            logging.debug(f"Current user ID: {current_user.id}")

            # Log the exact data being sent to the database
            logging.debug(f"Event details: nombre={form.nombre.data}, ubicacion={form.ubicacion.data}, fecha_inicio={form.fecha_inicio.data}, fecha_fin={form.fecha_fin.data}, descripcion={form.descripcion.data}, organizador_id={current_user.id}")

            # Validar formato de fechas
            if not isinstance(form.fecha_inicio.data, datetime) or not isinstance(form.fecha_fin.data, datetime):
                flash('Invalid date format. Please use YYYY-MM-DD HH:MM:SS.')
                logging.error("Invalid date format detected.")
                return render_template('event_dates.html', form=form)

            # Convertir el formato de fecha ingresado al formato esperado por la base de datos
            fecha_inicio = form.fecha_inicio.data.strftime('%Y-%m-%d %H:%M:%S')
            fecha_fin = form.fecha_fin.data.strftime('%Y-%m-%d %H:%M:%S')

            evento = Evento(
                nombre=form.nombre.data,
                ubicacion=form.ubicacion.data,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                descripcion=form.descripcion.data,
                organizador_id=current_user.id
            )
            db.session.add(evento)
            db.session.commit()

            logging.info("Event successfully created and saved to the database.")
            flash('Event created successfully!')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating event: {str(e)}")
            flash(f'Error creating event: {str(e)}')
    else:
        logging.warning("Form validation failed. User input might be incorrect.")
        logging.debug(f"Form errors: {form.errors}")
        flash('Form validation failed. Please check your input.')

    return render_template('event_dates.html', form=form)

@main.route('/eventos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    """
    Permite editar un evento dependiendo del rol del usuario.
    """
    evento = Evento.query.get_or_404(id)

    # Verificar permisos
    if current_user.role.name == 'Organizador' and evento.organizador_id != current_user.id:
        flash('You do not have permission to edit this event.', 'danger')
        return redirect(url_for('main.dashboard'))

    if current_user.role.name == 'Usuario':
        flash('You do not have permission to edit events.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = EventForm(obj=evento)

    if form.validate_on_submit():
        # Convertir el formato de fecha ingresado al formato esperado por la base de datos
        fecha_inicio = form.fecha_inicio.data.strftime('%Y-%m-%d %H:%M:%S')
        fecha_fin = form.fecha_fin.data.strftime('%Y-%m-%d %H:%M:%S')

        evento.nombre = form.nombre.data
        evento.ubicacion = form.ubicacion.data
        evento.fecha_inicio = fecha_inicio
        evento.fecha_fin = fecha_fin
        evento.descripcion = form.descripcion.data

        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('event_dates.html', form=form, editar=True)

@main.route('/event_dates', methods=['GET', 'POST'])
def event_dates():
    """
    Renderiza la página de fechas de eventos con un formulario.
    """
    form = EventForm()

    if form.validate_on_submit():
        # Aquí puedes manejar la lógica para guardar el evento
        flash('Event form submitted successfully.')
        return redirect(url_for('main.event_dates'))

    return render_template('event_dates.html', form=form)

@main.route('/event_create', methods=['GET', 'POST'])
@login_required
def event_create():
    """
    Renderiza un formulario para crear un nuevo evento desde la interfaz web.
    """
    form = EventForm()

    if form.validate_on_submit():
        try:
            # Convertir el formato de fecha ingresado al formato esperado por la base de datos
            fecha_inicio = form.fecha_inicio.data.strftime('%Y-%m-%d %H:%M:%S')
            fecha_fin = form.fecha_fin.data.strftime('%Y-%m-%d %H:%M:%S')

            evento = Evento(
                nombre=form.nombre.data,
                ubicacion=form.ubicacion.data,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                descripcion=form.descripcion.data,
                organizador_id=current_user.id
            )
            db.session.add(evento)
            db.session.commit()

            flash('Event created successfully!')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}')

    return render_template('event_dates.html', form=form)

@main.route('/events')
@login_required
def events():
    """
    Muestra la lista de eventos usando la plantilla events.html.
    """
    eventos = Evento.query.all()
    return render_template('events.html', eventos=eventos, current_user=current_user)