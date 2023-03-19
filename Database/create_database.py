import os
import subprocess
import time
import sys
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# --- PostgreSQL Server ---

def run_postgres():
    # Check if PostgreSQL is already running
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="your_new_user",
            password="qwerty",
            port="5432"
        )
        print("Server is already running on port:", conn.get_dsn_parameters()["port"])
    except psycopg2.OperationalError:
        # Run the PostgreSQL server if it's not running
        print("Starting PostgreSQL server...")
        server_process = subprocess.Popen(["pg_ctl", "start", "-D", "C:\Program Files\PostgreSQL\10\bin"])
        time.sleep(5)
        print("Server started.")

# --- SQLAlchemy Script ---

def create_new_database():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="your_new_user",
        password="qwerty",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE mydatabase;")
    cursor.close()
    conn.close()

def create_database():
    # Database credentials    
    DB_NAME = "mydatabase"
    DB_USER = "your_new_user"
    DB_PASSWORD = "qwerty"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    # Set up the connection string to the database
    DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?user={DB_USER}"

    # Create the engine with the specified user
    engine = create_engine(DATABASE_URI)

    # Create a session factory
    Session = sessionmaker(bind=engine)

    # Define the CodeSnippet model
    Base = declarative_base()

    class CodeSnippet(Base):
        __tablename__ = "code_snippets"

        id = Column(Integer, primary_key=True)
        name = Column(String)
        description = Column(String)
        file_path = Column(String)
        code = Column(String)

        def __repr__(self):
            return f"<CodeSnippet(name='{self.name}', description='{self.description}', file_path='{self.file_path}')>"

    # Create the database tables
    Base.metadata.create_all(engine)

# --- Main Execution ---

def main():
    run_postgres()
    create_new_database()  # Call this function before creating the SQLAlchemy engine
    create_database()

if __name__ == "__main__":
    main()
