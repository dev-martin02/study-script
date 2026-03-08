import json
from pathlib import Path
from util.ai import AIAgent

def answer_questions(questions: list[str]) -> str:
    print("Waiting for the answer...")
    return AIAgent().generate_content(
        instruction="You are an expert, please respond to all this questions in a concise and to the point manner",
        contents=str(questions),
    )

def intelligent_sorting(folders: list[str], content: str) -> str:
    folder_names = ", ".join(folders)
    instruction = (
        "You are an expert organizing content. Review the file content and choose the best folder "
        f"from this list: {folder_names}. "
        "If none fits, suggest a new folder name and set create_one to true. "
        "Return JSON only in this format: "
        '{"folder_name": "String", "create_one": "Boolean"}'
    )

    return AIAgent().generate_content(
        instruction=instruction,
        contents=content,
        response_format={"type": "json_object"},
    )

def move_file_to_folder(file_path: Path, sorting_result: str, base_path: str | Path) -> Path:
    """Moves a file to a folder based on the JSON output from intelligent_sorting."""
    result = json.loads(sorting_result)
    folder_name = result["folder_name"]
    create_one = result["create_one"]

    target_folder = Path(base_path) / folder_name
    if create_one or not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {target_folder}")

    target_path = target_folder / file_path.name
    if target_path != file_path:
        file_path.rename(target_path)
        print(f"Moved {file_path.name} to {target_folder}")
    else:
        print(f"File {file_path.name} is already in {target_folder}")
        target_path = file_path

    return target_path

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