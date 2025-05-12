# Proyecto-Micro
Proyecto Final
Universidad Interamericana de Puerto Rico
Recinto de Arecibo
Emmanuel Argüelles Ocasio - R00f
John Valentín Jiménez - R00628924
Comp-2052
Prof. Dastas

Proyecto Final – Administrador de Eventos

Para nuestro proyeycto final de la clase Comp-2052, hemos escogido el sistema para gestionar eventos. Este sistema permite a los usuarios acceder a diferentes tipos de funciones según su rol (Administrador, Organizador y/o Participante). Algunas de estas funciones incluyen manejar, crear o eliminar eventos que serán guardados en la base de datos enlazada al proyecto. Además, el proyecto permite iniciar y cerrar sesión mediante contraseñas protegidas con hash. El profesor otorgó a los alumnos una plantilla de la que se debía derivar el proyecto dependiendo del tema escogido. En nuestro caso, para la base de datos decidimos utilizar MySQL Workbench para crear el enlace y almacenar lo requerido. Este documento es creado con el fin de detallar el funcionamiento del proyecto. 

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
 
 
 
 
 
 
 
 
 
 
 







