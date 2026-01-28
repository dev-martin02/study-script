# 📚 Study Script

An automated study notes assistant that watches your study folder, formats new notes with a consistent structure, and uses AI to answer your questions.

## What It Does

1. **Auto-formats new notes** — When you create a new `.txt` file in your study folder, it automatically applies a structured template with sections for Title, Subject, Date, Notes, and Questions.

2. **AI-powered Q&A** — After 5 minutes of inactivity on a file, the script extracts all the questions from the "Questions" section and sends them to (currently) OpenAI's GPT model for answers.

3. **Organizes your files** — Automatically creates a folder based on the note's title, moves the file there, and saves AI answers in a separate `questions.txt` file.

## File Structure Template

New files are formatted with:

```
Title:
Subject: 
Date:

====================
        Notes
====================

(your notes here)

====================
      Questions
====================

(your questions here)
```

## Setup

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd study-script
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Update the `file_path` variable in `main.py` to point to your study folder:
   ```python
   file_path = "C:/Users/YourUsername/Desktop/study"
   ```

## Usage

Run the script:

```bash
uv run main.py
```

The script will now watch your study folder. When you:

1. **Create a new `.txt` file** → It gets auto-formatted with the study template
2. **Write your notes and questions** → Just fill in the template
3. **Stop editing for 5 minutes** → AI answers your questions and organizes the files

## Project Structure

```
study-script/
├── main.py                      # File watcher and main loop
├── util/
│   ├── file_format/
│   │   ├── format.py            # Applies template to new files
│   │   └── format.txt           # The template structure
│   └── inspect/
│       └── index.py             # Extracts questions & calls OpenAI
├── pyproject.toml               # Project dependencies
└── uv.lock                      # Locked dependencies
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `watchdog` | File system monitoring |
| `openai` | AI-powered question answering |
| `python-dotenv` | Environment variable management |

## License

MIT
