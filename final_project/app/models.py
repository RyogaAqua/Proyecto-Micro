from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Carga un usuario desde su ID, necesario para el sistema de sesiones de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de roles (Admin, Professor, Student, etc.)
class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relación inversa opcional (para ver usuarios asociados al rol)
    users = db.relationship('User', backref='role', lazy=True)

# Modelo de usuarios del sistema
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Asegura suficiente espacio para el hash
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relación con cursos (si es profesor)
    cursos = db.relationship('Curso', backref='profesor', lazy=True)

    def set_password(self, password):
        # Fuerza el uso de pbkdf2:sha256
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña ingresada es válida comparando con el hash.
        """
        return check_password_hash(self.password_hash, password)

# Modelo de curso asociado a un profesor
class Curso(db.Model):
    __tablename__ = 'curso'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Modelo de evento asociado a la tabla 'evento'
class Evento(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    organizador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organizador = db.relationship('User', backref='eventos')