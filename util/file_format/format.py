from pathlib import Path

structure_path = "util/file_format/format.txt"

structure = Path(structure_path).read_text()

def format_file(file_path: Path) -> None:
    with open(file_path, 'w') as file:
        file.write(structure)