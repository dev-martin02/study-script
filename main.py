import time
from pathlib import Path
from datetime import datetime
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from util.file_format.format import format_file
from util.inspect.index import inspect_file

file_path = "C:/Users/Martin/Desktop/study"

class MyEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.modified_file = None
        self.event_type = None
        self.last_modified_time = 0

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.src_path != self.modified_file or event.event_type != self.last_event_type:
            self.modified_file = Path(event.src_path)
            self.event_type = event.event_type
            self.last_modified_time = datetime.fromtimestamp(self.modified_file.stat().st_mtime).timestamp() 
            # self.file_path = Path(self.last_modified_file)


event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, file_path, recursive=True)
observer.start()

try:
    while True:
        if event_handler.event_type == 'created' and  event_handler.modified_file.suffix == '.txt' and event_handler.modified_file.name != 'questions.txt':
            print(f"Formatting file: {event_handler.modified_file.name}")
            format_file(event_handler.modified_file)
        print(event_handler.modified_file)
        if event_handler.event_type == 'modified' and event_handler.modified_file.suffix == '.txt':
            if event_handler.last_modified_time + 300 < datetime.now().timestamp() and event_handler.last_modified_time != 0:
                print("File was not modified in the last 5 minutes") 
                inspect_file(event_handler.modified_file)
                event_handler.event_type = 'done'
            else:
                continue
        time.sleep(1)
finally:
    observer.stop()
    observer.join()