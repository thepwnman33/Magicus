# Import the necessary modules
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CodeSnippet

# Create a database engine and a session factory
engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)

# Define a custom event handler for the file system watcher
class CodeFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the event was triggered by a code file
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        # Get the file path and read the code from the file
        file_path = event.src_path
        with open(file_path, 'r') as f:
            code = f.read()

        # Create a session and update the corresponding entry in the database
        session = Session()
        code_snippet = session.query(CodeSnippet).filter_by(file_path=file_path).first()
        if code_snippet is not None:
            code_snippet.code = code
            session.commit()

# Create a file system observer and attach the event handler
observer = Observer()
event_handler = CodeFileHandler()
observer.schedule(event_handler, path='.', recursive=True)
observer.start()

# Wait indefinitely for file system events
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
