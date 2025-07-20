"""
helpers.py - General utility functions for Alfred file operations

Core utilities for safe file handling, path manipulation, and metadata extraction.
"""

import os
import shutil
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple, List
import json


class FileOperationError(Exception):
    """Custom exception for file operation failures"""

    pass


def ensure_directory(path: Path) -> Path:
    """
    Create directory if it doesn't exist, including parents.

    Args:
        path: Directory path to create

    Returns:
        Path object of created/existing directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_move_file(source: Path, destination: Path, overwrite: bool = False) -> Path:
    """
    Safely move a file to destination, handling conflicts.

    Args:
        source: Source file path
        destination: Destination file path
        overwrite: If False, adds number suffix to prevent overwriting

    Returns:
        Final destination path (might be different if conflict avoided)

    Raises:
        FileOperationError: If move fails
    """
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileOperationError(f"Source file does not exist: {source}")

    # Ensure destination directory exists
    ensure_directory(destination.parent)

    # Handle existing file conflict
    if destination.exists() and not overwrite:
        destination = get_unique_filepath(destination)

    try:
        shutil.move(str(source), str(destination))
        return destination
    except Exception as e:
        raise FileOperationError(f"Failed to move file: {e}")


def get_unique_filepath(filepath: Path) -> Path:
    """
    Generate unique filepath by adding number suffix if file exists.

    Examples:
        invoice.pdf → invoice_2.pdf → invoice_3.pdf

    Args:
        filepath: Original filepath

    Returns:
        Unique filepath that doesn't exist
    """
    if not filepath.exists():
        return filepath

    base = filepath.stem
    extension = filepath.suffix
    directory = filepath.parent
    counter = 2

    while True:
        new_path = directory / f"{base}_{counter}{extension}"
        if not new_path.exists():
            return new_path
        counter += 1


def get_file_metadata(filepath: Path) -> Dict[str, Any]:
    """
    Extract comprehensive metadata from a file.

    Args:
        filepath: Path to file

    Returns:
        Dictionary containing file metadata
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileOperationError(f"File does not exist: {filepath}")

    stats = filepath.stat()

    # Get MIME type
    mime_type, _ = mimetypes.guess_type(str(filepath))

    return {
        "filename": filepath.name,
        "stem": filepath.stem,
        "extension": filepath.suffix.lower(),
        "size_bytes": stats.st_size,
        "size_human": format_file_size(stats.st_size),
        "created_time": datetime.fromtimestamp(stats.st_ctime),
        "modified_time": datetime.fromtimestamp(stats.st_mtime),
        "mime_type": mime_type or "application/octet-stream",
        "absolute_path": str(filepath.absolute()),
        "parent_directory": str(filepath.parent),
        "file_hash": calculate_file_hash(filepath),
    }


def calculate_file_hash(filepath: Path, algorithm: str = "md5") -> str:
    """
    Calculate hash of file for duplicate detection.

    Args:
        filepath: Path to file
        algorithm: Hash algorithm (md5, sha256)

    Returns:
        Hex digest of file hash
    """
    hash_func = hashlib.new(algorithm)

    with open(filepath, "rb") as f:
        # Read in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes to human readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human readable size (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def build_organized_path(
    base_dir: Path,
    category: str,
    subcategories: List[str] = None,
    filename: str = None,
    date_based: bool = True,
) -> Path:
    """
    Build a human-readable organized file path.

    Examples:
        Documents/Invoices/2024/March/Amazon_Invoice.pdf
        Documents/Projects/ClientName/Proposals/Proposal_v2.docx

    Args:
        base_dir: Base directory (e.g., Documents)
        category: Main category (e.g., Invoices, Projects)
        subcategories: Additional folder levels
        filename: Final filename
        date_based: If True, adds year/month folders

    Returns:
        Complete path object
    """
    path_parts = [base_dir, category]

    if date_based:
        now = datetime.now()
        path_parts.extend([str(now.year), now.strftime("%B")])

    if subcategories:
        path_parts.extend(subcategories)

    path = Path(*path_parts)

    if filename:
        path = path / filename

    return path


def copy_file_safe(source: Path, destination: Path) -> Path:
    """
    Copy file with safety checks and conflict handling.

    Args:
        source: Source file path
        destination: Destination file path

    Returns:
        Final destination path
    """
    source = Path(source)
    destination = Path(destination)

    if not source.exists():
        raise FileOperationError(f"Source file does not exist: {source}")

    ensure_directory(destination.parent)

    if destination.exists():
        destination = get_unique_filepath(destination)

    try:
        shutil.copy2(str(source), str(destination))
        return destination
    except Exception as e:
        raise FileOperationError(f"Failed to copy file: {e}")


def get_file_type_category(filepath: Path) -> str:
    """
    Determine general category of file based on extension.

    Args:
        filepath: Path to file

    Returns:
        Category string (e.g., 'document', 'image', 'spreadsheet')
    """
    extension = filepath.suffix.lower()

    categories = {
        "document": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
        "spreadsheet": [".xls", ".xlsx", ".csv", ".ods"],
        "presentation": [".ppt", ".pptx", ".odp"],
        "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "video": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
        "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
        "archive": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "code": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json", ".xml"],
        "data": [".json", ".xml", ".yaml", ".yml", ".sql"],
    }

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "other"


def read_json_file(filepath: Path) -> Dict[str, Any]:
    """
    Safely read and parse JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data
    """
    filepath = Path(filepath)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileOperationError(f"JSON file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise FileOperationError(f"Invalid JSON in file {filepath}: {e}")


def write_json_file(filepath: Path, data: Dict[str, Any], pretty: bool = True) -> None:
    """
    Safely write data to JSON file.

    Args:
        filepath: Path to write to
        data: Data to serialize
        pretty: If True, format with indentation
    """
    filepath = Path(filepath)
    ensure_directory(filepath.parent)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        raise FileOperationError(f"Failed to write JSON file: {e}")


def list_files_in_directory(
    directory: Path, recursive: bool = False, extensions: List[str] = None
) -> List[Path]:
    """
    List files in directory with optional filtering.

    Args:
        directory: Directory to scan
        recursive: If True, include subdirectories
        extensions: List of extensions to filter (e.g., ['.pdf', '.doc'])

    Returns:
        List of Path objects for matching files
    """
    directory = Path(directory)

    if not directory.exists():
        return []

    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"

    files = []
    for path in directory.glob(pattern):
        if path.is_file():
            if extensions is None or path.suffix.lower() in extensions:
                files.append(path)

    return files


def is_hidden_file(filepath: Path) -> bool:
    """
    Check if file is hidden (starts with . on Unix, has hidden attribute on Windows).

    Args:
        filepath: Path to check

    Returns:
        True if file is hidden
    """
    filepath = Path(filepath)

    # Unix-style hidden files
    if filepath.name.startswith("."):
        return True

    # Windows hidden files (requires Windows-specific check)
    if os.name == "nt":
        import ctypes

        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
            return attrs != -1 and attrs & 2  # FILE_ATTRIBUTE_HIDDEN = 2
        except:
            pass

    return False


def create_test_file(filepath: Path, content: str = "Test content") -> Path:
    """
    Create a test file with given content (useful for testing).

    Args:
        filepath: Path where to create file
        content: Content to write

    Returns:
        Path to created file
    """
    filepath = Path(filepath)
    ensure_directory(filepath.parent)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath
