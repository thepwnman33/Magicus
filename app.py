import uvicorn 
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from create_database import add_code_file, update_code_file, Session, CodeFile

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic models
class CodeFileIn(BaseModel):
    name: str
    path: str
    content: str

class CodeFileOut(BaseModel):
    id: int
    name: str
    path: str
    content: str

# Define API endpoints
@app.post("/api/codefiles/", response_model=CodeFileOut)
def create_code_file(code_file: CodeFileIn, db: Session = Session()):
    db_code_file = db.query(CodeFile).filter_by(name=code_file.name, path=code_file.path).first()
    if db_code_file:
        raise HTTPException(status_code=400, detail="Code file already exists")
    add_code_file(code_file.name, code_file.path, code_file.content)
    db_code_file = db.query(CodeFile).filter_by(name=code_file.name, path=code_file.path).first()
    return db_code_file

@app.put("/api/codefiles/", response_model=CodeFileOut)
def update_code_file(code_file: CodeFileIn, db: Session = Session()):
    db_code_file = db.query(CodeFile).filter_by(name=code_file.name, path=code_file.path).first()
    if not db_code_file:
        raise HTTPException(status_code=404, detail="Code file not found")
    update_code_file(code_file.name, code_file.path, code_file.content)
    db_code_file = db.query(CodeFile).filter_by(name=code_file.name, path=code_file.path).first()
    return db_code_file

@app.get("/api/codefiles/", response_model=List[CodeFileOut])
def read_code_files(db: Session = Session()):
    code_files = db.query(CodeFile).all()
    return code_files
