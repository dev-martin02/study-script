import time
import platform
from pathlib import Path
from datetime import datetime
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from util.file_format.format import format_file, agent_format_file
from util.inspect.index import inspect_file

# Dynamically get the user's Desktop path regardless of OS
if platform.system() == "Windows":
    file_path = Path.home() / "OneDrive" / "Desktop" / "study-hub"
else:
    file_path = Path.home() / "Desktop" / "study-hub"

file_path.mkdir(parents=True, exist_ok=True) 
file_path = str(file_path)

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
    # files_to_inspect = []
    # for files in Path(file_path).iterdir():
    #     if files.stat().st_mtime + 300 < datetime.now().timestamp():
    #         files_to_inspect.append(files)

    # for file in files_to_inspect:
    #     print(f"Inspecting file: {file.name}")
    #     inspect_file(file)
    new_files_paths = set()
    file_path_obj = Path(file_path)

    while True:
        if event_handler.modified_file and event_handler.modified_file.parent == file_path_obj: 
            if event_handler.event_type == "modified" and event_handler.modified_file not in new_files_paths:
                print(f"Tracking new file: {event_handler.modified_file.name}")
                new_files_paths.add(event_handler.modified_file)
        if(new_files_paths):
            in_queu_folder = Path(file_path) / "inspection-in-queue"
            in_queu_folder.mkdir(parents=True, exist_ok=True) 
            for file in new_files_paths:
                file.rename(in_queu_folder / file.name)
            new_files_paths.clear()
        if event_handler.event_type == 'created' and event_handler.modified_file.suffix == '.txt' and event_handler.modified_file.name != 'questions.txt':
            print(f"Formatting file: {event_handler.modified_file.name}")
            format_file(event_handler.modified_file)
        # If inspection-in-queue folder has a fille then call thje agent to inspect it
        in_queu_folder = Path(file_path) / "inspection-in-queue"
        if in_queu_folder.exists():
            for file in in_queu_folder.iterdir():
                if file.is_file():
                    print(f"Agent formatting file: {file.name}")
                    agent_format_file(file)
        time.sleep(1)

    
finally:
    observer.stop()
    observer.join()