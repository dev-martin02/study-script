from dataclasses import dataclass
import platform
import time
from pathlib import Path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from util.ai import intelligent_sorting
from util.file_format.format import agent_format_file, format_file
from util.file_interaction.index import relocate_file

if platform.system() == "Windows":
    main_parent_path = Path.home() / "OneDrive" / "Desktop" / "study-hub"
else:
    main_parent_path = Path.home() / "Desktop" / "study-hub"

inspection_queue_name = "inspection-in-queue"
# Create main parent folder if it doesn't exist and subfolders
main_parent_path.mkdir(parents=True, exist_ok=True)

for folder_name in ["Inbox", "Content", "Problems"]:
    (main_parent_path / folder_name).mkdir(parents=True, exist_ok=True)

# Inbox structure
for subfolder in ["Structuring", "Naming", "in-queue"]:
    (main_parent_path / "Inbox" / subfolder).mkdir(parents=True, exist_ok=True)

def get_all_folders(path: Path) -> list[str]:
    return [
        item.name
        for item in path.iterdir()
        if item.is_dir() and item.name != inspection_queue_name
    ]

@dataclass
class File_handler:
    current_path: Path
    new_location_folder: Path

class MyEventHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.modified_file: Path | None = None
        self.event_type: str | None = None

    def on_any_event(self, event: FileSystemEvent) -> None:
        current_file = Path(event.src_path)
        if current_file != self.modified_file or event.event_type != self.event_type:
            self.modified_file = current_file
            self.event_type = event.event_type

event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, str(main_parent_path), recursive=True)
observer.start()

def check_folder_content(folder_name: str): 
    folder_path = main_parent_path / folder_name
    number_of_files = len(list(folder_path.glob("*.*")))
    return number_of_files
try:
    added_files_paths: set[Path] = set()
    inspection_queue_folder = main_parent_path / inspection_queue_name

    while True:
        if event_handler.modified_file and event_handler.event_type:
            current_file = event_handler.modified_file
            current_event = event_handler.event_type
            event_handler.modified_file = None
            event_handler.event_type = None

            if current_file.suffix == ".txt" and current_file.exists():
                if current_event == "created":
                    format_file(current_file)

        if check_folder_content('Inbox') > 0:
                print("Moving files to in-queue")
                for file in (main_parent_path / "Inbox").iterdir():
                    if file.is_file() and file.suffix == ".txt":
                        file_handler = File_handler(
                            current_path=file,
                            new_location_folder=main_parent_path / "Inbox" / "in-queue" / file.name
                        )
                        relocate_file(file_handler)

        # files in-que should be moved to structuring
        # Check for all the files in the in-queue folder and move them to the structuring folder one by one
        for file in (main_parent_path / "Inbox" / "in-queue").iterdir():
            if file.is_file() and file.suffix == ".txt":
                # send the file to the agent to be structured
                agent_format_file(file)
                file_handler = File_handler(
                    current_path=file,
                    new_location_folder=main_parent_path / "Inbox" / "Structuring" / file.name
                )
                relocate_file(file_handler)


        # Check for all the files in the structuring folder and move them to the content folder one by one
        for file in (main_parent_path / "Inbox" / "Structuring").iterdir():
            if file.is_file() and file.suffix == ".txt":
                # send the file to the agent to be structured
                sorting_result = intelligent_sorting(get_all_folders(main_parent_path / "Content"), file.read_text(encoding="utf-8"))
                if sorting_result:
                    file_handler = File_handler(
                        current_path=file,
                        new_location_folder=main_parent_path / "Content"
                    )
                    relocate_file(file_handler, sorting_result)
                else:
                    file_handler = File_handler(
                        current_path=file,
                        new_location_folder=main_parent_path / "Problems"/file.name
                    )
                    relocate_file(file_handler)
        time.sleep(1)
finally:
    observer.stop()
    observer.join()