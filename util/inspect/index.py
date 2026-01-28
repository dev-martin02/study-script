import dotenv
from openai import OpenAI
from pathlib import Path

dotenv.load_dotenv()
client = OpenAI()

class openaiAgent:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-5-nano"

    def generate_content(self, instruction: str, contents: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            reasoning={"effort": "low"},
            input=contents,
            instructions=instruction,

        )
        return response.output_text


def answer_questions(questions: list) -> str:
    print('waiting for the answer...')
    return openaiAgent().generate_content(
        instruction="You are an expert, please respond to all this questions in a concise and to the point manner",
        contents=str(questions),
    )

# Get all the main content title & Questions
def inspect_file(file_path: Path) -> dict:
    full_content = ""

    with open(file_path, 'r') as file:
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
            with open(question_file, 'w') as file:
                file.write(answers)

            # Main file
            with open(new_file_name, 'w') as file:
                file.write(new_content)