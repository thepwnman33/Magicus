import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TestHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"Event detected: {event}")

observer = Observer()
event_handler = TestHandler()
observer.schedule(event_handler, path='C:\\Users\\oropesa\\Documents\\Magicus', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
#this is just a commentdsfgdggggbg