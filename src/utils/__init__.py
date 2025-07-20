"""
Alfred Utils Module

Utility functions for file operations, validation, and formatting.
"""

# Import main functions for easier access
from .helpers import (
    FileOperationError,
    ensure_directory,
    safe_move_file,
    get_unique_filepath,
    get_file_metadata,
    calculate_file_hash,
    format_file_size,
    build_organized_path,
    copy_file_safe,
    get_file_type_category,
    read_json_file,
    write_json_file,
    list_files_in_directory,
    is_hidden_file,
    create_test_file,
)

from .validators import (
    ValidationError,
    validate_file_path,
    validate_file_size,
    validate_filename,
    validate_file_extension,
    is_supported_file_type,
    validate_directory_path,
    validate_mime_type,
    sanitize_filename,
    validate_category_name,
    validate_file_operation,
    validate_batch_operation,
)

from .formatters import (
    clean_filename,
    format_date_for_filename,
    create_descriptive_filename,
    format_document_type,
    clean_company_name,
    format_person_name,
    format_folder_path,
    humanize_file_size,
    format_time_ago,
    generate_unique_suffix,
    format_month_name,
    truncate_text,
    create_screenshot_filename,
)

__all__ = [
    # Exceptions
    "FileOperationError",
    "ValidationError",
    # Helper functions
    "ensure_directory",
    "safe_move_file",
    "get_unique_filepath",
    "get_file_metadata",
    "calculate_file_hash",
    "format_file_size",
    "build_organized_path",
    "copy_file_safe",
    "get_file_type_category",
    "read_json_file",
    "write_json_file",
    "list_files_in_directory",
    "is_hidden_file",
    "create_test_file",
    # Validator functions
    "validate_file_path",
    "validate_file_size",
    "validate_filename",
    "validate_file_extension",
    "is_supported_file_type",
    "validate_directory_path",
    "validate_mime_type",
    "sanitize_filename",
    "validate_category_name",
    "validate_file_operation",
    "validate_batch_operation",
    # Formatter functions
    "clean_filename",
    "format_date_for_filename",
    "create_descriptive_filename",
    "format_document_type",
    "clean_company_name",
    "format_person_name",
    "format_folder_path",
    "humanize_file_size",
    "format_time_ago",
    "generate_unique_suffix",
    "format_month_name",
    "truncate_text",
    "create_screenshot_filename",
]
