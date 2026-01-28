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

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.src_path != self.modified_file or event.event_type != self.event_type:
            self.modified_file = Path(event.src_path)
            self.event_type = event.event_type


event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, file_path, recursive=True)
observer.start()

try:

    # Inspect all the files that weren't modified in the last 5 minutes
    files_to_inspect = []
    for files in Path(file_path).iterdir():
        if files.stat().st_mtime + 300 < datetime.now().timestamp():
            files_to_inspect.append(files)

    for file in files_to_inspect:
        print(f"Inspecting file: {file.name}")
        inspect_file(file)

    while True:
        if event_handler.event_type == 'created' and  event_handler.modified_file.suffix == '.txt' and event_handler.modified_file.name != 'questions.txt':
            print(f"Formatting file: {event_handler.modified_file.name}")
            format_file(event_handler.modified_file)
        time.sleep(1)
finally:
    observer.stop()
    observer.join()