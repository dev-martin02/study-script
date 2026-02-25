import json
from pathlib import Path
from util.ai import AIAgent

def answer_questions(questions: list) -> str:
    print('waiting for the answer...')
    return AIAgent().generate_content(
        instruction="You are an expert, please respond to all this questions in a concise and to the point manner",
        contents=str(questions),
    )

def intelligent_sorting(folders: list, content: str) -> str:
    folder_names = ', '.join(folders)
    return AIAgent().generate_content(
        instruction=f"You are an expert organizing content, please go thru the content of the file and based on the folders names: {folder_names}, determine which folder is the best fit for the content and respond with only the name of the folder without any explanation, if the content is not related to any of the folders respond with a suggestion of a new folder name that is relevant to the content and the property 'create_one' put it as true ONLY IF YOU ARE MAKING A SUGGESTION,     please return json and follow this format : " + """{
                "folder_name": "String",
                "create_one": "Boolean" 
            }""",
        contents=content,
        response_format={
            'type': 'json_object',
        }
    )

def move_file_to_folder(file_path: Path, sorting_result: str, base_path: str | Path) -> Path:
    """
    Moves a file to a folder based on the output from intelligent_sorting.
    Creates a new folder if needed.
    
    Args:
        file_path: Path to the file to move
        sorting_result: JSON string output from intelligent_sorting function
    
    Returns:
        Path to the moved file
    """
    # Parse the JSON result
    result = json.loads(sorting_result)
    folder_name = result['folder_name']
    create_one = result['create_one']
    
    # Determine the target folder path
    target_folder = Path(base_path) / folder_name
    
    # Create the folder if needed
    if create_one or not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {target_folder}")
    
    # Move the file to the target folder
    target_path = target_folder / file_path.name
    
    # Only move if target is different from source
    if target_path != file_path:
        file_path.rename(target_path)
        print(f"Moved {file_path.name} to {target_folder}")
    else:
        print(f"File {file_path.name} is already in {target_folder}")
        target_path = file_path
    
    return target_path

# Get all the main content title & Questions
def inspect_file(file_path: Path) -> dict:
    full_content = ""

    with open(file_path, 'r', encoding='utf-8') as file:
        # Get the title of the file
        file_title = file.readline()
        content = file.read()
        full_content += file_title + content
        questions = []

        # Get the questions of the file 
        questions_start = full_content.find('Questions')
        if questions_start != -1:
            # Get everything after "Questions"
            questions_section = full_content[questions_start:]
            
            # Split into lines and filter out empty lines and === lines
            questions = [
                line.strip() 
                for line in questions_section.split('\n')
                if line.strip() and not line.strip().startswith('=') and 'Questions' not in line
            ]

    # Clean the title and extra spaces
    clean_title = file_title.replace("Title:", "").strip()

    # Get the parent directory of the file
    parent_dir = file_path.parent

    if parent_dir.name != clean_title and file_path.name != "questions.txt":
        # Create a new folder in the same directory as the original file
        new_folder = parent_dir / clean_title  # the "/" concatenates the path
        new_folder.mkdir(parents=True, exist_ok=True) 

        if(len(questions) > 0):  
            answers = answer_questions(questions)
            # Rename the file to the new folder name
            new_file_name = Path(f"{new_folder}/{clean_title}.txt")
            # Create the new file in the new folder
            question_file = Path(f"{new_folder}/questions.txt")
            # Rename the file to the new folder name
            file_path.rename(new_file_name)

            first_question_start = full_content.find(questions[0])
            new_content = full_content[:first_question_start]

            # Questions file
            with open(question_file, 'w', encoding='utf-8') as file:
                file.write(answers)

            # Main file
            with open(new_file_name, 'w', encoding='utf-8') as file:
                file.write(new_content)