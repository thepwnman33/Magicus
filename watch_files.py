print("Starting the file watcher...")
import os
import time
import git
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CodeSnippet
import subprocess

DB_NAME = "mydatabase"
DB_USER = "your_new_user"
DB_PASSWORD = "qwerty"
DB_HOST = "localhost"
DB_PORT = "5432"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)

def git_commit(file_path, message):
    try:
        print(f"Running git add {file_path}")
        subprocess.run(["git", "add", file_path], check=True)
        print(f"Running git commit -m '{message}'")
        subprocess.run(["git", "commit", "-m", message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while committing {file_path}: {e}")

from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler

class CodeFileHandler(PatternMatchingEventHandler):
    patterns = ["*.py"]
    def on_modified(self, event):
        print(f"Handling on_modified event for {event.src_path}")
        print(f"File modified: {event.src_path}")
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        print("Processing modified Python file")

        file_path = event.src_path
        repo = git.Repo(search_parent_directories=True)
        relative_file_path = os.path.relpath(file_path, repo.working_tree_dir)
        try:
            latest_commit = repo.git.log('-1', relative_file_path)
        except git.exc.GitCommandError:
            latest_commit = repo.head.commit.hexsha

        session = Session()
        code_snippet = session.query(CodeSnippet).filter_by(file_path=file_path).first()

        if code_snippet is not None:
            with open(file_path, 'r') as f:
                code = f.read()

            print(f"Before updating code snippet: {code_snippet.__dict__}")

            code_snippet.code = code
            code_snippet.latest_commit = latest_commit
            session.commit()

            print(f"After updating code snippet: {code_snippet.__dict__}")
            print(f"Updated code snippet: {file_path}")
            git_commit(file_path, f"Update {file_path}")
        else:
            print("File not found in the database")

    def on_created(self, event):
        print(f"Handling on_created event for {event.src_path}")
        file_path = None
        if not event.is_directory and event.src_path.endswith(".py"):
            file_path = event.src_path
            print(f"File created: {file_path}")
            print("Processing created Python file")

            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return

            # The rest of the on_created function code...
            repo = git.Repo(search_parent_directories=True)
            relative_file_path = os.path.relpath(file_path, repo.working_tree_dir)
            try:
                latest_commit = repo.git.log('-1', relative_file_path)
            except git.exc.GitCommandError:
                latest_commit = repo.head.commit.hexsha

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

                print(f"Added code snippet: {code_snippet.__dict__}")

                # Stage the new file
                repo.git.add(file_path)

                # Commit the new file
                commit_message = f"Add new Python file: {file_path}"
                repo.git.commit('-m', commit_message)

                # Push the changes to the remote repository
                repo.git.push()

            else:
                print("File already exists in the database")

    def on_deleted(self, event):
        print(f"Handling on_deleted event for {event.src_path}")
        print(f"File deleted: {event.src_path}")
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        print("Processing deleted Python file")

        file_path = event.src_path
        session = Session()
        code_snippet = session.query(CodeSnippet).filter_by(file_path=file_path).first()

        if code_snippet is not None:
            session.delete(code_snippet)
            session.commit()
            print(f"Deleted code snippet: {file_path}")
            git_commit(file_path, f"Delete {file_path}")
        else:
            print("File not found in the database")


observer = PollingObserver()
event_handler = CodeFileHandler()
observer.schedule(event_handler, path='C:\\Users\\oropesa\\Documents\\Magicus', recursive=True)
print(f"Watching path: C:\\Users\\oropesa\\Documents\\Magicus")
print("Starting the observer...")
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
