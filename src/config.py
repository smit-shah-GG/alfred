"""
config.py - Configuration management for Alfred

Loads configuration from environment variables and provides defaults.
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration for Alfred."""

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    IS_DEVELOPMENT = ENVIRONMENT == "development"

    # Paths - Use dev folders in development, real folders in production
    if IS_DEVELOPMENT:
        WATCH_FOLDERS = os.getenv(
            "ALFRED_WATCH_FOLDERS",
            "dev_folders/watched/downloads,dev_folders/watched/desktop,dev_folders/watched/documents",
        ).split(",")
        ORGANIZE_ROOT = Path(os.getenv("ALFRED_ORGANIZE_ROOT", "dev_folders/organized"))
    else:
        WATCH_FOLDERS = os.getenv(
            "ALFRED_WATCH_FOLDERS", "~/Downloads,~/Desktop,~/Documents"
        ).split(",")
        ORGANIZE_ROOT = Path(os.getenv("ALFRED_ORGANIZE_ROOT", "~/Documents"))

    # Convert to Path objects and expand user paths
    WATCH_FOLDERS = [Path(folder).expanduser() for folder in WATCH_FOLDERS]
    ORGANIZE_ROOT = ORGANIZE_ROOT.expanduser()

    # Google AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_FAST = "gemini-2.0-flash-exp"  # For quick operations
    GEMINI_MODEL_SMART = "gemini-2.0-flash-exp"  # Will update to 2.5 when available

    # File handling
    MAX_FILE_SIZE_MB = int(os.getenv("ALFRED_MAX_FILE_SIZE_MB", "100"))
    SUPPORTED_EXTENSIONS = {
        # Documents
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt",
        # Spreadsheets
        ".xls",
        ".xlsx",
        ".csv",
        ".ods",
        # Presentations
        ".ppt",
        ".pptx",
        ".odp",
        # Images
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
        # Data files
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        # Archives
        ".zip",
        # Common formats
        ".md",
        ".log",
    }

    # Security (optional for now)
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

    # Feature flags
    ENABLE_ALFRED_PERSONALITY = (
        os.getenv("ENABLE_ALFRED_PERSONALITY", "true").lower() == "true"
    )
    ENABLE_AUTO_ORGANIZE = os.getenv("ENABLE_AUTO_ORGANIZE", "false").lower() == "true"
    ENABLE_BATCH_PROCESSING = (
        os.getenv("ENABLE_BATCH_PROCESSING", "true").lower() == "true"
    )
    FAKE_PROCESSING_DELAY = float(os.getenv("FAKE_PROCESSING_DELAY", "0.5"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "alfred.log")

    # UI Settings
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "dark")

    # Alfred personality settings
    ALFRED_RESPONSES = {
        "greeting": [
            "Good day, sir. Ready to bring order to your digital chaos.",
            "Alfred at your service. Shall we tidy up those files?",
            "Ah, I see we have some organizing to do. Leave it to me.",
        ],
        "messy_filename": [
            "I see we're being creative with naming conventions today, sir.",
            "Ah, 'asdfasdf.pdf' - a classic. I'll fix that for you.",
            "Your naming skills are... unique. Allow me to assist.",
        ],
        "success": [
            "Filed successfully. You'll find it exactly where it should be.",
            "Organization complete. Your files are now in their proper place.",
            "Done. I've taken the liberty of giving it a sensible name as well.",
        ],
        "error": [
            "I'm terribly sorry, but I encountered an issue.",
            "My apologies, sir. Something went awry.",
            "How embarrassing. Let me try that again.",
        ],
    }

    @classmethod
    def validate(cls):
        """Validate configuration and raise errors if invalid."""
        errors = []

        # Check API key
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set. Please add it to your .env file.")

        # Check paths exist in development
        if cls.IS_DEVELOPMENT:
            for folder in cls.WATCH_FOLDERS:
                if not folder.exists():
                    errors.append(f"Watch folder does not exist: {folder}")

            if not cls.ORGANIZE_ROOT.exists():
                errors.append(f"Organize root does not exist: {cls.ORGANIZE_ROOT}")

        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))

    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        # Create organize root
        cls.ORGANIZE_ROOT.mkdir(parents=True, exist_ok=True)

        # Create watch folders in development
        if cls.IS_DEVELOPMENT:
            for folder in cls.WATCH_FOLDERS:
                folder.mkdir(parents=True, exist_ok=True)

        # Create standard organization structure
        categories = [
            "Documents/Invoices/2024",
            "Documents/Invoices/2025",
            "Documents/Contracts",
            "Documents/Reports",
            "Documents/Projects",
            "Documents/Personal",
            "Documents/Screenshots",
            "Documents/Archives",
        ]

        for category in categories:
            (cls.ORGANIZE_ROOT / category).mkdir(parents=True, exist_ok=True)

    @classmethod
    def display_config(cls):
        """Display current configuration (hiding sensitive values)."""
        print("\n🎩 Alfred Configuration")
        print("=" * 50)
        print(f"Environment: {cls.ENVIRONMENT}")
        print(f"Watch Folders: {[str(f) for f in cls.WATCH_FOLDERS]}")
        print(f"Organize Root: {cls.ORGANIZE_ROOT}")
        print(f"Gemini API Key: {'✓ Set' if cls.GEMINI_API_KEY else '✗ Not Set'}")
        print(
            f"Auto-organize: {'✓ Enabled' if cls.ENABLE_AUTO_ORGANIZE else '✗ Disabled'}"
        )
        print(
            f"Alfred Personality: {'✓ Enabled' if cls.ENABLE_ALFRED_PERSONALITY else '✗ Disabled'}"
        )
        print("=" * 50)


# Create a singleton instance
config = Config()

# Convenience exports
WATCH_FOLDERS = config.WATCH_FOLDERS
ORGANIZE_ROOT = config.ORGANIZE_ROOT
GEMINI_API_KEY = config.GEMINI_API_KEY
