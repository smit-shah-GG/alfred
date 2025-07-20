# Alfred Utils Module

Core utility functions for the Alfred AI File Butler system.

## Overview

The utils module provides three main components:

1. **helpers.py** - File operations and path management
2. **validators.py** - Input validation and safety checks  
3. **formatters.py** - Filename cleaning and formatting

## Quick Start

```python
from utils import *

# Clean up a messy filename
clean = clean_filename("invoice__FINAL_v2 (1) - Copy.pdf")
# Result: "invoice_final_v2.pdf"

# Validate a file is safe to process
validate_file_path(Path("document.pdf"))
validate_file_size(Path("huge_file.pdf"), max_size_mb=50)

# Build organized paths
path = build_organized_path(
    base_dir=Path("Documents"),
    category="Invoices", 
    subcategories=["Amazon"],
    filename="invoice.pdf",
    date_based=True
)
# Result: Documents/Invoices/2024/December/invoice.pdf

# Get file metadata
metadata = get_file_metadata(Path("document.pdf"))
print(f"Size: {metadata['size_human']}")
print(f"Type: {metadata['mime_type']}")
```

## Key Functions

### File Operations (helpers.py)

- `safe_move_file()` - Move files without overwriting
- `get_file_metadata()` - Extract comprehensive file info
- `build_organized_path()` - Create human-readable folder structures
- `ensure_directory()` - Create directories safely

### Validation (validators.py)

- `validate_file_path()` - Check for path traversal attacks
- `validate_filename()` - Ensure filenames are safe
- `is_supported_file_type()` - Check if Alfred can analyze the file
- `sanitize_filename()` - Clean dangerous characters

### Formatting (formatters.py)

- `clean_filename()` - Transform messy names into clean ones
- `create_descriptive_filename()` - Generate names from document content
- `format_date_for_filename()` - Consistent date formatting
- `humanize_file_size()` - Convert bytes to readable format

## Testing

Run the test script to see all utilities in action:

```bash
python scripts/test_utils.py
```

This will:
- Clean various messy filenames
- Validate file operations
- Build organization paths
- Create and move test files
- Show formatting examples

## Design Principles

1. **Safety First** - All operations validate inputs and handle errors
2. **Human-Readable** - Paths and names that make sense to users
3. **Cross-Platform** - Works on Windows, macOS, and Linux
4. **No Dependencies** - Core utils use only Python stdlib where possible
5. **Well-Tested** - Comprehensive test coverage

## Error Handling

The utils use custom exceptions for clear error messages:

```python
from utils import FileOperationError, ValidationError

try:
    safe_move_file(source, dest)
except FileOperationError as e:
    print(f"Move failed: {e}")

try:
    validate_filename("CON.txt")  # Reserved Windows name
except ValidationError as e:
    print(f"Invalid filename: {e}")
```

## Configuration

Utils respect settings from `config.py`:
- `MAX_FILE_SIZE_MB` - Maximum file size to process
- `SUPPORTED_EXTENSIONS` - File types Alfred can analyze
- `ORGANIZE_ROOT` - Base directory for organized files

## Contributing

When adding new utilities:
1. Add to appropriate module (helpers/validators/formatters)
2. Include comprehensive docstrings
3. Add to `__all__` in `__init__.py`
4. Write tests in `test_utils.py`
5. Handle cross-platform differences
