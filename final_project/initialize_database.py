from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from config import Config

def ensure_database_exists():
    """
    Verifies if the database exists and creates it if it does not.
    """
    database_uri = Config.SQLALCHEMY_DATABASE_URI

    # Extract server URI and database name
    server_uri = database_uri.rsplit('/', 1)[0]  # Remove database name
    database_name = database_uri.rsplit('/', 1)[1]  # Extract database name

    # Connect to the server
    engine = create_engine(server_uri)
    try:
        with engine.connect() as connection:
            # Create the database if it does not exist
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
            print(f"✅ Database '{database_name}' verified or created.")
    except OperationalError as e:
        print(f"❌ Error connecting to the MySQL server: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    ensure_database_exists()