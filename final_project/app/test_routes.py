from flask import Blueprint, request, jsonify
from app.models import db, Curso

# Blueprint solo con endpoints de prueba para cursos
main = Blueprint('main', __name__)

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/cursos', methods=['GET'])
def listar_cursos():
    """
    Retorna una lista de cursos (JSON).
    """
    cursos = Curso.query.all()

    data = [
        {'id': curso.id, 'titulo': curso.titulo, 'descripcion': curso.descripcion, 'profesor_id': curso.profesor_id}
        for curso in cursos
    ]
    return jsonify(data), 200


@main.route('/cursos/<int:id>', methods=['GET'])
def listar_un_curso(id):
    """
    Retorna un solo curso por su ID (JSON).
    """
    curso = Curso.query.get_or_404(id)

    data = {
        'id': curso.id,
        'titulo': curso.titulo,
        'descripcion': curso.descripcion,
        'profesor_id': curso.profesor_id
    }

    return jsonify(data), 200


@main.route('/cursos', methods=['POST'])
def crear_curso():
    """
    Crea un curso sin validación.
    Espera JSON con 'titulo', 'descripcion' y 'profesor_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    curso = Curso(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        profesor_id=data.get('profesor_id')  # sin validación de usuario
    )

    db.session.add(curso)
    db.session.commit()

    return jsonify({'message': 'Curso creado', 'id': curso.id, 'profesor_id': curso.profesor_id}), 201

@main.route('/cursos/<int:id>', methods=['PUT'])
def actualizar_curso(id):
    """
    Actualiza un curso sin validación de usuario o permisos.
    """
    curso = Curso.query.get_or_404(id)
    data = request.get_json()

    curso.titulo = data.get('titulo', curso.titulo)
    curso.descripcion = data.get('descripcion', curso.descripcion)
    curso.profesor_id = data.get('profesor_id', curso.profesor_id)

    db.session.commit()

    return jsonify({'message': 'Curso actualizado', 'id': curso.id}), 200

@main.route('/cursos/<int:id>', methods=['DELETE'])
def eliminar_curso(id):
    """
    Elimina un curso sin validación de permisos.
    """
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()

    return jsonify({'message': 'Curso eliminado', 'id': curso.id}), 200
