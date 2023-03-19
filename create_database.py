# Import the necessary modules
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define the base model
Base = declarative_base()

# Define the CodeSnippet model
class CodeSnippet(Base):
    __tablename__ = 'code_snippets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    file_path = Column(String)
    code = Column(String)

# Create the database engine and the code_snippets table
engine = create_engine('postgresql://user:password@localhost/mydatabase')
Base.metadata.create_all(engine)
