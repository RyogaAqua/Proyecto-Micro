from app import create_app
from app.models import db

# Crea la instancia de la aplicación Flask utilizando la factoría
app = create_app()

# Inicializa la base de datos
with app.app_context():
    try:
        db.create_all()
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Ejecuta el servidor Flask en modo desarrollo
    # host='0.0.0.0' permite que sea accesible desde otras máquinas en la red local
    # En producción, desactiva debug o usa un servidor como Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
