from pathlib import Path

from util.ai import AIAgent

structure_path = "util/file_format/format.txt"
structure = Path(structure_path).read_text(encoding="utf-8")


def format_file(file_path: Path) -> None:
    file_path.write_text(structure, encoding="utf-8")


def agent_format_file(file_path: Path) -> None:
    print(f"\n[AI] Starting formatting: {file_path.name}...")
    try:
        content = file_path.read_text(encoding="utf-8")

        formatted_content = AIAgent().generate_content(
            instruction=(
                "You are an expert at organizing notes. Format the content using this template: "
                f"{structure}. Keep notes above the questions section and use bullet points."
            ),
            contents=content,
        )

        file_path.write_text(formatted_content, encoding="utf-8")
        print(f"[AI] Success: {file_path.name} has been formatted.")

    except Exception as exc:
        print(f"[AI] Error formatting {file_path.name}: {exc}")
        print("[AI] Moving on...")
