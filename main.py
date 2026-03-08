import platform
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from util.file_format.format import agent_format_file, format_file
from util.inspect.index import intelligent_sorting, move_file_to_folder

if platform.system() == "Windows":
    main_parent_path = Path.home() / "OneDrive" / "Desktop" / "study-hub"
else:
    main_parent_path = Path.home() / "Desktop" / "study-hub"

inspection_queue_name = "inspection-in-queue"
main_parent_path.mkdir(parents=True, exist_ok=True)

def get_all_folders() -> list[str]:
    return [
        item.name
        for item in main_parent_path.iterdir()
        if item.is_dir() and item.name != inspection_queue_name
    ]


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
                elif (
                    current_event == "modified"
                    and current_file.parent == main_parent_path
                    and current_file not in added_files_paths
                    and current_file.stat().st_size > 0
                ):
                    print(f"Tracking modified file: {current_file.name}")
                    added_files_paths.add(current_file)
                else:
                    format_file(current_file)

        if added_files_paths:
            inspection_queue_folder.mkdir(parents=True, exist_ok=True)
            for file in added_files_paths:
                file.rename(inspection_queue_folder / file.name)
            added_files_paths.clear()

        if inspection_queue_folder.exists():
            for file in inspection_queue_folder.iterdir():
                if not file.is_file():
                    continue

                try:
                    agent_format_file(file)
                    print(f"Finished formatting file: {file.name}")
                    print(f"Intelligently sorting file: {file.name}")

                    file_content = file.read_text(encoding="utf-8")
                    sorting_result = intelligent_sorting(get_all_folders(), file_content)
                    print(f"Sorting result for {file.name}: {sorting_result}")

                    if sorting_result:
                        print(f"Moving file: {file.name} to folder based on sorting result")
                        move_file_to_folder(file, sorting_result, main_parent_path)
                        print(f"Finished processing file: {file.name}")
                except Exception as exc:
                    print(f"Error occurred while formatting file {file.name}: {exc}")

        time.sleep(1)
finally:
    observer.stop()
    observer.join()