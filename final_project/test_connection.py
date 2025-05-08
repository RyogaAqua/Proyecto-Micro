from app import create_app, db

def test_connection():
    """
    Test the connection to the database by attempting to connect and query the database.
    """
    app = create_app()

    with app.app_context():
        try:
            # Attempt to connect to the database
            db.session.execute('SELECT 1')
            print("✅ Connection to the database was successful.")
        except Exception as e:
            print(f"❌ Failed to connect to the database: {e}")

if __name__ == "__main__":
    test_connection()