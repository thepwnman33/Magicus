from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    file_path = Column(String)
    code = Column(String)
    latest_commit = Column(String)
