import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
import argparse

# =========================
# Core Logic
# =========================
def slugify(text: str) -> str:
    if not text:
        return "untitled"

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)

    text = text.strip("-")   # <-- FIX

    return text[:100] or "untitled"

def get_next_adr_number(path: Path) -> int:
    numbers = []

    for f in path.glob("????-*.md"):
        try:
            n = int(f.name[:4])
            if 1 <= n <= 9999:
                numbers.append(n)
        except ValueError:
            continue

    return max(numbers, default=0) + 1

def build_adr_content(
    num: int,
    title: str,
    author: str,
    status: str,
    context: str,
    decision: str,
    consequences: str,
    today: str,
) -> str:
    return f"""# {num:04d} - {title}

**Status:** {status.capitalize()}  
**Date:** {today}  
**Author:** {author}

## Context
{context or "No detailed context provided."}

## Decision
{decision or "No decision recorded yet."}

## Consequences
{consequences or "No consequences recorded yet."}

---

*Once accepted, do not modify — create a superseding ADR instead.*
"""

def default_author() -> str:
    return (
        os.getenv("GIT_AUTHOR_NAME")
        or os.getenv("USERNAME")
        or os.getenv("USER")
        or "Unknown"
    )

# =========================
# CLI
# =========================
def prompt(text: str, default: str | None = None) -> str:
    if default:
        value = input(f"{text} [{default}]: ").strip()
        return value or default
    return input(f"{text}: ").strip()

def prompt_int(text: str, default: int) -> int:
    while True:
        raw = input(f"{text} [{default:04d}]: ").strip()
        if not raw:
            return default

        if raw.isdigit():
            val = int(raw)
            if 1 <= val <= 9999:
                return val

        print("Invalid number (1–9999).")

def multiline_input(prompt_text: str) -> str:
    print(f"\n{prompt_text}")
    print("(Finish with '---' on a new line)")

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "---":
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    return "\n".join(lines).strip()

def confirm_overwrite(path: Path) -> bool:
    if not path.exists():
        return True
    return input(f"{path.name} exists. Overwrite? (y/N): ").lower() == "y"

# =========================
# CLI Argument Parsing
# =========================
def parse_args():
    parser = argparse.ArgumentParser(description="ADR Creator")

    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--status", choices=["proposed", "accepted", "superseded"])
    parser.add_argument("--dir", type=Path)
    parser.add_argument("--number", type=int)

    return parser.parse_args()

# =========================
# Application Flow
# =========================
def run():
    args = parse_args()

    print("=" * 70)
    print("ADR Creator")
    print("=" * 70)

    # Directory
    adr_dir = args.dir or (Path.cwd() / "docs" / "adr")

    try:
        adr_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory: {e}")
        sys.exit(1)

    # Number
    next_num = get_next_adr_number(adr_dir)
    num = args.number or prompt_int("ADR number", next_num)

    # Title
    title = args.title or ""
    while not title:
        title = prompt("Title")

    slug = slugify(title)
    filename = f"{num:04d}-{slug}.md"
    filepath = adr_dir / filename

    if not confirm_overwrite(filepath):
        print("Cancelled.")
        sys.exit(0)

    # Author
    author = args.author or prompt("Author", default_author())

    # Status
    status = args.status or prompt(
        "Status (proposed/accepted/superseded)", "proposed"
    ).lower()

    if status not in {"proposed", "accepted", "superseded"}:
        status = "proposed"

    # Sections (interactive only if not CLI-driven)
    if args.title:
        # CLI mode → minimal input
        context = ""
        decision = ""
        consequences = ""
    else:
        context = multiline_input("## Context")
        decision = multiline_input("## Decision")
        consequences = multiline_input("## Consequences")

    today = date.today().strftime("%Y-%m-%d")

    content = build_adr_content(
        num=num,
        title=title,
        author=author,
        status=status,
        context=context,
        decision=decision,
        consequences=consequences,
        today=today,
    )

    try:
        filepath.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"Failed to write file: {e}")
        sys.exit(1)

    print("\nADR created:")
    print(filepath)

# =========================
# Entrypoint
# =========================
if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)