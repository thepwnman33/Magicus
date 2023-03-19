import os
import time
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CodeSnippet

DB_NAME = "mydatabase"
DB_USER = "your_new_user"
DB_PASSWORD = "qwerty"
DB_HOST = "localhost"
DB_PORT = "5432"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)

class CodeFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        file_path = event.src_path
        repo = git.Repo(search_parent_directories=True)
        latest_commit = repo.git.log('-1', file_path)
        session = Session()
        code_snippet = session.query(CodeSnippet).filter_by(file_path=file_path).first()
        if code_snippet is not None and code_snippet.latest_commit == latest_commit:
            return

        with open(file_path, 'r') as f:
            code = f.read()

        if code_snippet is not None:
            code_snippet.code = code
            code_snippet.latest_commit = latest_commit
            session.commit()
            print(f"Updated code snippet: {file_path}")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        file_path = event.src_path
        repo = git.Repo(search_parent_directories=True)
        latest_commit = repo.git.log('-1', file_path)
        session = Session()
        code_snippet = session.query(CodeSnippet).filter_by(file_path=file_path).first()

        if code_snippet is None:
            with open(file_path, 'r') as f:
                code = f.read()

            name = os.path.basename(file_path)
            description = name

            code_snippet = CodeSnippet(name=name, description=description, file_path=file_path, code=code, latest_commit=latest_commit)
            session.add(code_snippet)
            session.commit()
            print(f"Added new code snippet: {file_path}")

observer = Observer()
event_handler = CodeFileHandler()
observer.schedule(event_handler, path='C:/Users/oropesa/Documents/Magicus', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
