# Proyecto-Micro
Proyecto Final
Universidad Interamericana de Puerto Rico
Recinto de Arecibo
Emmanuel Argüelles Ocasio - R00f
John Valentín Jiménez - R00628924
Comp-2052
Prof. Dastas

Proyecto Final – Administrador de Eventos

Para nuestro proyecto final de la clase Comp-2052, hemos escogido el sistema para gestionar eventos. Este sistema permite a los usuarios acceder a diferentes tipos de funciones según su rol (Administrador, Organizador y/o Participante). Algunas de estas funciones incluyen manejar, crear o eliminar eventos que serán guardados en la base de datos enlazada al proyecto. Además, el proyecto permite iniciar y cerrar sesión mediante contraseñas protegidas con hash. El profesor otorgó a los alumnos una plantilla de la que se debía derivar el proyecto dependiendo del tema escogido. En nuestro caso, para la base de datos decidimos utilizar MySQL Workbench para crear el enlace y almacenar lo requerido. Este documento es creado con el fin de resaltar los detalles importantes sobre el funcionamiento del proyecto. 

Primero, creamos la base de datos en MySQL Workbench:
 
•	Aquí ingresamos el nombre de la base de datos, el host, puerto y el password de root que utilizaremos más adelante.
 
•	Luego, creamos un file SQL en el que implementaremos el esquema correspondiente de los que ofreció el profesor en el archivo del proyecto.
 

•	Seleccionamos Data Export para que la base de datos creada aparezca disponible.

•	Utilizamos una extensión SQL para VS Code e ingresamos las credenciales creadas para la base de datos en MySQL Workbench.

•	En el documento config.py, debemos asegurarnos que la línea 'mysql+pymysql://root:789456@localhost/administrador_evento contenga el nombre correcto de la base de datos y la contraseña correcta de root. 
•	La correcta configuración de la anterior permitirá que create_demo_users.py pueda crear los usuarios en la base de datos con los datos ingresados en el archivo Python. 
 
 
auth_routes.py:
 

•	En el documento auth_routes.py., tenemos la función:
user = User.query.filter_by(email=form.email.data).first()
if user and user.check_password(form.password.data):
    login_user(user)  # Establece sesión
    # Registra en tabla login:
    db.session.execute("INSERT INTO login (user_id) VALUES (:user_id)", {"user_id": user.id})

Esta se encarga de verificar las credenciales proporcionadas por el usuario para su inicio de sesión. Este es el main de nuestro Dashboard, de no tener un usuario creado, podemos seleccionar register y se nos redirigirá a register.html. 

•	Tenemos la función:
user = User(username=..., email=..., role=role)
user.set_password(password)  # Almacena hash seguro
db.session.add(user)
# Registra en tabla signup:
db.session.execute("INSERT INTO signup (...) VALUES (...)")

Esta se encarga del registro, verifica que las credenciales ingresadas por el usuario no sean iguales a alguna de las credenciales de un usuario ya creado. De estar disponibles, crea el usuario nuevo con su rol y credenciales. Una vez creadas las credenciales nuevas, podremos seleccionar iniciar sesión y se nos redirigirá a login.html.

•	Finalmente, tenemos la función de logout, que cerrera la sesión del usuario y lo redirige a login.html
@auth.route('/logout')
 def logout():
 """
 Cierra sesión del usuario actual y redirige al login.
 """ 
logout_user() 
return redirect(url_for('auth.login'))

routes.py:
 
 •	En route.py, la linea:
@main.route('/')
def index():
    return render_template('index.html')
Esta nos dirige a una home básica que no requiere autenticación de usuario para acceder a la misma. 
•	Línea para cambio de contraseña
@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.')
            return render_template('cambiar_password.html', form=form)
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Password updated successfully.')
        return redirect(url_for('main.dashboard'))

Esta linea permite al usuario usar el form de change password para crear una contraseña nueva, la actualiza con set_password() y redirige al dashboard.html

•	Ruta de Dashboard.html
@main.route('/dashboard')
@login_required
def dashboard():
    eventos = Evento.query.all()
    return render_template('dashboard.html', eventos=eventos, current_user=current_user)

•	Se crea la API de eventos:
@main.route('/eventos', methods=['GET'])
def listar_eventos():
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

•	La función para crear eventos requiere de login por parte del usuario. En esta se le pedirá al usuario detalles del evento como fecha, ubicación y hora:
@main.route('/eventos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_evento_web():
    form = EventForm()
    
    if form.validate_on_submit():
        try:
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

•	La funcion para eliminar eventos solo estará disponible para administrador y organizador.
@main.route('/eventos/<int:id>', methods=['POST', 'DELETE'])
@login_required
def eliminar_evento(id):
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




 
 
 
 
 
 
 
 
 
 







