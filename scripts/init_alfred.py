#!/usr/bin/env python3
"""
setup.py - Initial setup script for Alfred

Run this after cloning the repo to set up your development environment.
"""

import os
import sys
import shutil
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"🎩 {text}")
    print(f"{'=' * 60}")


def check_python_version():
    """Ensure Python 3.10+ is being used."""
    print("\n📌 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required. You have {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor} - OK")


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    print("\n📌 Setting up environment file...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("✅ .env file already exists")
        return

    if not env_example.exists():
        print("❌ .env.example not found!")
        return

    shutil.copy(env_example, env_file)
    print("✅ Created .env file from .env.example")
    print("⚠️  Please edit .env and add your GEMINI_API_KEY")


def create_directory_structure():
    """Create necessary directories."""
    print("\n📌 Creating directory structure...")

    directories = [
        # Development folders
        "dev_folders/watched/downloads",
        "dev_folders/watched/desktop",
        "dev_folders/watched/documents",
        "dev_folders/organized/Documents/Invoices/2024",
        "dev_folders/organized/Documents/Invoices/2025",
        "dev_folders/organized/Documents/Contracts",
        "dev_folders/organized/Documents/Reports",
        "dev_folders/organized/Documents/Projects",
        "dev_folders/organized/Documents/Personal",
        "dev_folders/organized/Documents/Screenshots",
        "dev_folders/organized/Documents/Archives",
        # Data folders
        "data/cache",
        "data/uploads",
        "data/configs",
        # Log folder
        "logs",
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Create .gitkeep files in data folders
    for folder in ["data/cache", "data/uploads"]:
        gitkeep = Path(folder) / ".gitkeep"
        gitkeep.touch()

    print(f"✅ Created {len(directories)} directories")


def create_test_files():
    """Create some test files in the watched folders."""
    print("\n📌 Creating test files...")

    test_files = [
        ("dev_folders/watched/downloads/invoice.pdf", "Mock invoice content"),
        ("dev_folders/watched/downloads/asdfasdf.pdf", "Poorly named file"),
        ("dev_folders/watched/downloads/screenshot_2024-03-15.png", "Screenshot"),
        ("dev_folders/watched/desktop/important_document.docx", "Important doc"),
        ("dev_folders/watched/desktop/TODO.txt", "Task list"),
    ]

    for filepath, content in test_files:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    print(f"✅ Created {len(test_files)} test files")


def check_requirements():
    """Check if required packages are installed."""
    print("\n📌 Checking Python packages...")

    try:
        import streamlit

        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not installed")
        print("   Run: pip install -r requirements.txt")

    try:
        import google.generativeai

        print("✅ Google Generative AI installed")
    except ImportError:
        print("❌ Google Generative AI not installed")
        print("   Run: pip install -r requirements.txt")


def setup_git_hooks():
    """Set up useful git hooks."""
    print("\n📌 Setting up git hooks...")

    # Create pre-commit hook for code formatting
    pre_commit = Path(".git/hooks/pre-commit")
    pre_commit.parent.mkdir(parents=True, exist_ok=True)

    pre_commit_content = """#!/bin/sh
# Format Python files with black before committing
FILES=$(git diff --cached --name-only --diff-filter=ACMR "*.py" | sed 's| |\\\\ |g')
if [ -n "$FILES" ]; then
    echo "Formatting Python files with black..."
    echo "$FILES" | xargs black --check --quiet
    if [ $? -ne 0 ]; then
        echo "❌ Some files need formatting. Run 'black .' to fix."
        exit 1
    fi
fi
"""

    if not pre_commit.exists():
        pre_commit.write_text(pre_commit_content)
        pre_commit.chmod(0o755)
        print("✅ Created pre-commit hook for code formatting")
    else:
        print("✅ Pre-commit hook already exists")


def display_next_steps():
    """Display next steps for the user."""
    print_header("Setup Complete! Next Steps")

    print(
        """
1. Edit .env file and add your GEMINI_API_KEY:
   - Get one at: https://makersuite.google.com/app/apikey
   - Add to .env: GEMINI_API_KEY=your-key-here

2. Install Python dependencies:
   pip install -r requirements.txt

3. Test the utils:
   python scripts/test_utils.py

4. Run Alfred UI:
   streamlit run src/ui/streamlit_app.py

5. Start developing!
   - Utils are in src/utils/
   - Test files are in dev_folders/watched/
   - Organized files go to dev_folders/organized/

Happy organizing! 🎩
"""
    )


def main():
    """Run all setup steps."""
    print_header("Alfred AI File Butler - Setup")

    check_python_version()
    create_env_file()
    create_directory_structure()
    create_test_files()
    check_requirements()
    setup_git_hooks()
    display_next_steps()


if __name__ == "__main__":
    main()
