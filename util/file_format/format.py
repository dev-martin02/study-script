from pathlib import Path
from util.ai import AIAgent

structure_path = "util/file_format/format.txt"

structure = Path(structure_path).read_text()

def format_file(file_path: Path) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(structure)

def agent_format_file(file_path: Path) -> None:
    print(f"\n[AI] Starting formatting: {file_path.name}...")
    try:
        # Read with UTF-8 to handle special characters
        content = file_path.read_text(encoding='utf-8')
        
        formatted_content = AIAgent().generate_content(
            instruction=f"You are an expert organizing notes, please format the like this {structure}. Make sure the questions are at the end of the file and the notes are at the top of the file using bullets points",
            contents=content,
        )
        
        # Write back with UTF-8
        file_path.write_text(formatted_content, encoding='utf-8')
        print(f"✅ Success: {file_path.name} has been formatted.")
        
    except Exception as e:
        print(f"❌ Error formatting {file_path.name}: {str(e)}")
        print("Moving on...")
