"""
validators.py - Input validation functions for Alfred

Validation utilities to ensure file safety, size limits, and proper inputs.
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, Set
import mimetypes


class ValidationError(Exception):
    """Custom exception for validation failures"""

    pass


# Configuration constants (can be moved to config later)
MAX_FILE_SIZE_MB = 100  # Maximum file size in MB
MAX_FILENAME_LENGTH = 255  # Maximum filename length
DANGEROUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".com", ".scr", ".vbs", ".js", ".jar"}
ALLOWED_CHARACTERS_PATTERN = re.compile(r"^[\w\s\-._()]+$")


def validate_file_path(filepath: Path, must_exist: bool = True) -> bool:
    """
    Validate that a file path is safe and accessible.

    Args:
        filepath: Path to validate
        must_exist: If True, checks that file exists

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    filepath = Path(filepath)

    # Check for path traversal attempts
    try:
        # Resolve to absolute path and check it doesn't escape
        resolved = filepath.resolve()
        if ".." in str(filepath):
            raise ValidationError("Path traversal detected")
    except Exception as e:
        raise ValidationError(f"Invalid path: {e}")

    # Check existence if required
    if must_exist and not filepath.exists():
        raise ValidationError(f"File does not exist: {filepath}")

    # Check if it's actually a file (not directory)
    if must_exist and not filepath.is_file():
        raise ValidationError(f"Path is not a file: {filepath}")

    return True


def validate_file_size(filepath: Path, max_size_mb: Optional[float] = None) -> bool:
    """
    Validate that file size is within acceptable limits.

    Args:
        filepath: Path to file
        max_size_mb: Maximum size in megabytes (uses default if None)

    Returns:
        True if valid

    Raises:
        ValidationError: If file is too large
    """
    if max_size_mb is None:
        max_size_mb = MAX_FILE_SIZE_MB

    filepath = Path(filepath)
    if not filepath.exists():
        raise ValidationError(f"File does not exist: {filepath}")

    size_mb = filepath.stat().st_size / (1024 * 1024)

    if size_mb > max_size_mb:
        raise ValidationError(f"File too large: {size_mb:.1f}MB (max: {max_size_mb}MB)")

    return True


def validate_filename(filename: str, strict: bool = False) -> bool:
    """
    Validate that filename is safe and reasonable.

    Args:
        filename: Filename to validate
        strict: If True, only allows alphanumeric, spaces, and basic punctuation

    Returns:
        True if valid

    Raises:
        ValidationError: If filename is invalid
    """
    # Check length
    if len(filename) > MAX_FILENAME_LENGTH:
        raise ValidationError(
            f"Filename too long: {len(filename)} chars (max: {MAX_FILENAME_LENGTH})"
        )

    # Check for empty
    if not filename or filename.isspace():
        raise ValidationError("Filename cannot be empty")

    # Check for dangerous characters
    dangerous_chars = ["/", "\\", "\0", "\n", "\r", "\t"]
    if any(char in filename for char in dangerous_chars):
        raise ValidationError("Filename contains invalid characters")

    # Strict mode - only allow safe characters
    if strict and not ALLOWED_CHARACTERS_PATTERN.match(filename):
        raise ValidationError("Filename contains special characters (strict mode)")

    # Check for reserved Windows filenames
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }

    name_without_ext = filename.split(".")[0].upper()
    if name_without_ext in reserved_names:
        raise ValidationError(f"Reserved filename: {filename}")

    return True


def validate_file_extension(
    filepath: Path,
    allowed_extensions: Optional[Set[str]] = None,
    block_dangerous: bool = True,
) -> bool:
    """
    Validate file extension is allowed and safe.

    Args:
        filepath: Path to file
        allowed_extensions: Set of allowed extensions (e.g., {'.pdf', '.doc'})
        block_dangerous: If True, blocks potentially dangerous extensions

    Returns:
        True if valid

    Raises:
        ValidationError: If extension is not allowed
    """
    extension = filepath.suffix.lower()

    # Check against dangerous extensions
    if block_dangerous and extension in DANGEROUS_EXTENSIONS:
        raise ValidationError(f"Potentially dangerous file type: {extension}")

    # Check against allowed list if provided
    if allowed_extensions and extension not in allowed_extensions:
        raise ValidationError(
            f"File type not allowed: {extension}. "
            f"Allowed types: {', '.join(sorted(allowed_extensions))}"
        )

    return True


def is_supported_file_type(filepath: Path) -> bool:
    """
    Check if file type is supported by Alfred for analysis.

    Args:
        filepath: Path to file

    Returns:
        True if file type can be analyzed
    """
    supported_extensions = {
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
        # Archives (for extraction)
        ".zip",
        # Common formats
        ".md",
        ".log",
    }

    return filepath.suffix.lower() in supported_extensions


def validate_directory_path(
    dirpath: Path, must_exist: bool = False, must_be_writable: bool = True
) -> bool:
    """
    Validate directory path for safety and accessibility.

    Args:
        dirpath: Directory path to validate
        must_exist: If True, directory must already exist
        must_be_writable: If True, checks write permissions

    Returns:
        True if valid

    Raises:
        ValidationError: If validation fails
    """
    dirpath = Path(dirpath)

    # Check for path traversal
    try:
        resolved = dirpath.resolve()
        if ".." in str(dirpath):
            raise ValidationError("Path traversal detected")
    except Exception as e:
        raise ValidationError(f"Invalid directory path: {e}")

    # Check existence
    if must_exist and not dirpath.exists():
        raise ValidationError(f"Directory does not exist: {dirpath}")

    if dirpath.exists() and not dirpath.is_dir():
        raise ValidationError(f"Path is not a directory: {dirpath}")

    # Check write permissions
    if must_be_writable and dirpath.exists():
        test_file = dirpath / ".alfred_write_test"
        try:
            test_file.touch()
            test_file.unlink()
        except Exception:
            raise ValidationError(f"Directory is not writable: {dirpath}")

    return True


def validate_mime_type(
    filepath: Path, allowed_types: Optional[List[str]] = None
) -> bool:
    """
    Validate file MIME type.

    Args:
        filepath: Path to file
        allowed_types: List of allowed MIME types (e.g., ['application/pdf'])

    Returns:
        True if valid

    Raises:
        ValidationError: If MIME type is not allowed
    """
    mime_type, _ = mimetypes.guess_type(str(filepath))

    if mime_type is None:
        # Try to determine from extension
        extension = filepath.suffix.lower()
        if extension:
            mime_type = mimetypes.types_map.get(extension, "application/octet-stream")
        else:
            mime_type = "application/octet-stream"

    if allowed_types and mime_type not in allowed_types:
        raise ValidationError(
            f"MIME type not allowed: {mime_type}. "
            f"Allowed types: {', '.join(allowed_types)}"
        )

    return True


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Sanitize filename by replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid chars with

    Returns:
        Sanitized filename
    """
    # Handle empty filename
    if not filename:
        return "unnamed"

    # Replace path separators
    filename = filename.replace("/", replacement)
    filename = filename.replace("\\", replacement)

    # Replace other dangerous characters
    dangerous_chars = ["\0", "\n", "\r", "\t", ":", "*", "?", '"', "<", ">", "|"]
    for char in dangerous_chars:
        filename = filename.replace(char, replacement)

    # Handle Windows reserved names
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }

    name_parts = filename.split(".")
    if name_parts[0].upper() in reserved_names:
        name_parts[0] = f"{replacement}{name_parts[0]}"
        filename = ".".join(name_parts)

    # Remove leading/trailing spaces and dots
    filename = filename.strip(" .")

    # Ensure filename isn't empty after sanitization
    if not filename:
        filename = "unnamed"

    # Truncate if too long
    if len(filename) > MAX_FILENAME_LENGTH:
        # Keep extension if possible
        if "." in filename:
            name, ext = filename.rsplit(".", 1)
            max_name_length = MAX_FILENAME_LENGTH - len(ext) - 1
            filename = f"{name[:max_name_length]}.{ext}"
        else:
            filename = filename[:MAX_FILENAME_LENGTH]

    return filename


def validate_category_name(category: str) -> bool:
    """
    Validate category name for folder creation.

    Args:
        category: Category name to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If category name is invalid
    """
    if not category or category.isspace():
        raise ValidationError("Category name cannot be empty")

    if len(category) > 50:
        raise ValidationError("Category name too long (max 50 chars)")

    # Only allow alphanumeric, spaces, underscores, and hyphens
    if not re.match(r"^[\w\s\-]+$", category):
        raise ValidationError(
            "Category name can only contain letters, numbers, spaces, "
            "underscores, and hyphens"
        )

    return True


def validate_file_operation(
    source: Path, destination: Path, operation: str = "move"
) -> bool:
    """
    Validate that a file operation (move/copy) is safe to perform.

    Args:
        source: Source file path
        destination: Destination file path
        operation: Type of operation ('move' or 'copy')

    Returns:
        True if operation is valid

    Raises:
        ValidationError: If operation would be unsafe
    """
    source = Path(source)
    destination = Path(destination)

    # Validate source
    validate_file_path(source, must_exist=True)

    # Check they're not the same
    if source.resolve() == destination.resolve():
        raise ValidationError("Source and destination are the same")

    # Check destination directory is writable
    validate_directory_path(destination.parent, must_be_writable=True)

    # For move operations, check source is not read-only
    if operation == "move":
        if not os.access(source, os.W_OK):
            raise ValidationError(f"Cannot move read-only file: {source}")

    return True


def validate_batch_operation(files: List[Path], max_files: int = 100) -> bool:
    """
    Validate batch file operation isn't too large.

    Args:
        files: List of file paths
        max_files: Maximum number of files allowed

    Returns:
        True if valid

    Raises:
        ValidationError: If batch is too large
    """
    if len(files) > max_files:
        raise ValidationError(
            f"Too many files in batch: {len(files)} (max: {max_files})"
        )

    # Check total size
    total_size = sum(f.stat().st_size for f in files if f.exists())
    max_total_mb = 500  # 500MB total

    if total_size > max_total_mb * 1024 * 1024:
        raise ValidationError(
            f"Batch too large: {total_size / 1024 / 1024:.1f}MB "
            f"(max: {max_total_mb}MB)"
        )

    return True
