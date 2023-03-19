import os
import subprocess
import time
import sys
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2

# --- PostgreSQL Server ---

def run_postgres():
    # Check if PostgreSQL is already running
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="your_new_superuser",
            password="qwerty",
            port="5432"
        )
        print("Server is already running on port:", conn.get_dsn_parameters()["port"])
    except psycopg2.OperationalError:
        # Run the PostgreSQL server if it's not running
        print("Starting PostgreSQL server...")
        server_process = subprocess.Popen(["pg_ctl", "start", "-D", "C:\Program Files\PostgreSQL\10\data"])
        time.sleep(5)
        print("Server started.")

# --- SQLAlchemy Script ---

def create_database():
    # Database credentials
    DB_NAME = "postgres"
    DB_USER = "your_new_superuser"
    DB_PASSWORD = "qwerty"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    # Set up the connection string to the database
    DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create the engine with the specified user
    engine = create_engine(DATABASE_URI)

    # Create a session factory
    Session = sessionmaker(bind=engine)

    # Create the base class for declarative ORM
    Base = declarative_base()

    # Define the User model
    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        name = Column(String)
        description = Column(String)
        file_path = Column(String)
        code = Column(String)

        def __repr__(self):
            return f"<CodeSnippet(name='{self.name}', description='{self.description}', file_path='{self.file_path}')>"

    # Create the database tables
    Base.metadata.create_all(engine)

    # Create a session and add a new user
    session = Session()
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()

    # Query the database and print the users
    users = session.query(User).all()
    print(users)

# --- Main Execution ---

def main():
    run_postgres()
    create_database()

if __name__ == "__main__":
    main()
