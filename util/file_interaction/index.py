import json
from pathlib import Path
from util.ai import AIAgent
    
def answer_questions(questions: list[str]) -> str:
    return AIAgent().generate_content(
        instruction="You are an expert, please respond to all this questions in a concise and to the point manner",
        contents=str(questions),
    )

def relocate_file(file_obj: dict, sorting_result: str | None = None) -> Path:
    if sorting_result:
        result = json.loads(sorting_result)
        folder_name = result["folder_name"]
        create_one = result["create_one"]
        print(sorting_result)
        new_folder = file_obj.new_location_folder/ folder_name
        if create_one:
            new_folder.mkdir(parents=True, exist_ok=True)
            file_obj.current_path.rename(new_folder / file_obj.current_path.name)
        else:
            # new_location_folder is a directory (e.g. Content); move file into it
            file_obj.current_path.rename(new_folder / file_obj.current_path.name)
    else:
        file_obj.new_location_folder.parent.mkdir(parents=True, exist_ok=True)
        file_obj.current_path.rename(file_obj.new_location_folder)

def inspect_file(file_path: Path) -> None:
    full_content = ""

    with open(file_path, "r", encoding="utf-8") as file:
        file_title = file.readline()
        content = file.read()
        full_content += file_title + content
        questions = []

        questions_start = full_content.find("Questions")
        if questions_start != -1:
            questions_section = full_content[questions_start:]
            questions = [
                line.strip()
                for line in questions_section.split("\n")
                if line.strip()
                and not line.strip().startswith("=")
                and "Questions" not in line
            ]

    clean_title = file_title.replace("Title:", "").strip()
    parent_dir = file_path.parent

    if parent_dir.name != clean_title and file_path.name != "questions.txt":
        new_folder = parent_dir / clean_title
        new_folder.mkdir(parents=True, exist_ok=True)

        if len(questions) > 0:
            answers = answer_questions(questions)
            new_file_name = Path(f"{new_folder}/{clean_title}.txt")
            question_file = Path(f"{new_folder}/questions.txt")
            file_path.rename(new_file_name)

            first_question_start = full_content.find(questions[0])
            new_content = full_content[:first_question_start]

            with open(question_file, "w", encoding="utf-8") as file:
                file.write(answers)

            with open(new_file_name, "w", encoding="utf-8") as file:
                file.write(new_content)