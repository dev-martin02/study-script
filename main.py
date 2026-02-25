import time
import platform
from pathlib import Path
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from util.file_format.format import format_file, agent_format_file
from util.inspect.index import intelligent_sorting, move_file_to_folder

# Dynamically get the user's Desktop path regardless of OS
if platform.system() == "Windows":
    main_parent_path = Path.home() / "OneDrive" / "Desktop" / "study-hub"
else:
    main_parent_path = Path.home() / "Desktop" / "study-hub"

main_parent_path.mkdir(parents=True, exist_ok=True) 
main_parent_path = str(main_parent_path)

# Check for all the folders in the main_parent_path
def get_all_folders() -> list:
    folders = []
    # avoid the inspection queue folder and only get the folders in the main_parent_path
    for item in Path(main_parent_path).iterdir():
        if item.is_dir():
            if item.name != "inspection-in-queue": 
              folders.append(item.name)
    return folders
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
observer.schedule(event_handler, main_parent_path, recursive=True)
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
    added_files_paths = set()
    file_path_obj = Path(main_parent_path)

    while True:
        if event_handler.event_type == 'created' and event_handler.modified_file.suffix == '.txt' and event_handler.modified_file.name != 'questions.txt':
            print(f"Formatting file: {event_handler.modified_file.name}")
            format_file(event_handler.modified_file)

        if event_handler.modified_file and event_handler.modified_file.parent == file_path_obj: 
            if event_handler.event_type == "modified" and event_handler.modified_file not in added_files_paths:
                print(f"Tracking new file: {event_handler.modified_file.name}")
                added_files_paths.add(event_handler.modified_file)

        if(added_files_paths):
            # Create a folder called inspection-in-queue and move all the files in the set to that folder
            inspection_queue_folder = Path(main_parent_path) / "inspection-in-queue"
            inspection_queue_folder.mkdir(parents=True, exist_ok=True) 
            for file in added_files_paths:
                file.rename(inspection_queue_folder / file.name)
            added_files_paths.discard(file)
            
        # If inspection-in-queue folder has a fille then call the agent to inspect it
        # There is a problem here, once the file is "done" it researt the loop and then throws an error because the file is not in the inspection-in-queue anymore, need to find a way to only call the agent once per file
        inspection_queue_folder = Path(main_parent_path) / "inspection-in-queue"
        if inspection_queue_folder.exists():
            for file in inspection_queue_folder.iterdir():
                if file.is_file():
                    try:
                        agent_format_file(file)
                        print (f"Finished formatting file: {file.name}")
                        print(f"Intelligently sorting file: {file.name}")

                        # Read file content and ensure file is closed before moving
                        file_content = file.read_text(encoding='utf-8')
                        sorting_result = intelligent_sorting(get_all_folders(), file_content)
                        print(f"Sorting result for {file.name}: {sorting_result}")

                        if(sorting_result):
                            print(f"Moving file: {file.name} to folder based on sorting result")
                            move_file_to_folder(file, sorting_result, main_parent_path)
                            print(f"Finished processing file: {file.name}")

                    except Exception as e:
                        print(f"Error occurred while formatting file {file.name}: {e}")
        time.sleep(1)
finally:
    observer.stop()
    observer.join()