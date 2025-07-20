"""
formatters.py - Output formatting functions for Alfred

Functions to clean filenames, format dates, and create human-friendly naming.
"""

import re
import unicodedata
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any
import calendar


def clean_filename(
    filename: str, keep_spaces: bool = True, max_length: Optional[int] = 100
) -> str:
    """
    Clean up messy filename into something reasonable.

    Examples:
        "invoice__FINAL_v2 (1) - Copy.pdf" → "invoice_final_v2.pdf"
        "ScreenShot 2024-03-15 at 2.34.56 PM.png" → "screenshot_2024-03-15_143456.png"

    Args:
        filename: Original filename
        keep_spaces: If True, converts spaces to underscores; if False, removes them
        max_length: Maximum length for filename (excluding extension)

    Returns:
        Cleaned filename
    """
    # Split name and extension
    if "." in filename:
        name, extension = filename.rsplit(".", 1)
        extension = "." + extension.lower()
    else:
        name = filename
        extension = ""

    # Remove Unicode characters and normalize
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase
    name = name.lower()

    # Replace common patterns
    name = re.sub(r"\s*\(\d+\)\s*", "", name)  # Remove (1), (2), etc.
    name = re.sub(r"\s*-\s*copy\s*", "", name)  # Remove "- Copy"
    name = re.sub(r"\s*copy\s*of\s*", "", name)  # Remove "Copy of"
    name = re.sub(r"_+", "_", name)  # Multiple underscores to single
    name = re.sub(r"-+", "-", name)  # Multiple hyphens to single
    name = re.sub(r"\s+", " ", name)  # Multiple spaces to single

    # Handle version indicators
    name = re.sub(r"final_final", "final", name)
    name = re.sub(r"final_v\d+", lambda m: m.group(0).replace("final_", ""), name)

    # Replace spaces
    if keep_spaces:
        name = name.replace(" ", "_")
    else:
        name = name.replace(" ", "")

    # Remove special characters except underscore and hyphen
    name = re.sub(r"[^a-z0-9_\-]", "", name)

    # Clean up edges
    name = name.strip("_- ")

    # Handle empty result
    if not name:
        name = "unnamed"

    # Truncate if needed
    if max_length and len(name) > max_length:
        name = name[:max_length].rstrip("_-")

    return name + extension


def format_date_for_filename(
    date_obj: Optional[datetime] = None, format_style: str = "compact"
) -> str:
    """
    Format date for use in filenames.

    Args:
        date_obj: Datetime object (uses current time if None)
        format_style: Style of formatting
            - "compact": 20240315 (good for sorting)
            - "readable": 2024-03-15
            - "full": 2024-03-15_143045

    Returns:
        Formatted date string
    """
    if date_obj is None:
        date_obj = datetime.now()

    formats = {
        "compact": "%Y%m%d",
        "readable": "%Y-%m-%d",
        "full": "%Y-%m-%d_%H%M%S",
        "american": "%m-%d-%Y",
        "european": "%d-%m-%Y",
    }

    return date_obj.strftime(formats.get(format_style, formats["readable"]))


def create_descriptive_filename(
    document_type: str,
    entities: Dict[str, Any],
    original_name: Optional[str] = None,
    include_date: bool = True,
) -> str:
    """
    Create descriptive filename based on document analysis.

    Examples:
        Invoice from Amazon → "Amazon_Invoice_2024-03-15.pdf"
        Contract with John Doe → "Contract_JohnDoe_2024-03-15.pdf"

    Args:
        document_type: Type of document (invoice, contract, etc.)
        entities: Extracted entities (company, person, date, etc.)
        original_name: Original filename for reference
        include_date: Whether to append date

    Returns:
        Descriptive filename
    """
    parts = []

    # Add primary entity (company or person)
    if entities.get("company"):
        parts.append(clean_company_name(entities["company"]))
    elif entities.get("person"):
        parts.append(format_person_name(entities["person"]))

    # Add document type
    parts.append(format_document_type(document_type))

    # Add specific identifiers
    if entities.get("invoice_number"):
        parts.append(f"IN{entities['invoice_number']}")
    elif entities.get("reference"):
        parts.append(entities["reference"][:10])  # Truncate long references

    # Add date
    if include_date:
        if entities.get("document_date"):
            date_str = format_date_for_filename(entities["document_date"])
        else:
            date_str = format_date_for_filename()
        parts.append(date_str)

    # Get extension from original or default to .pdf
    extension = ".pdf"
    if original_name and "." in original_name:
        extension = "." + original_name.rsplit(".", 1)[1].lower()

    # Join parts with underscore
    filename = "_".join(filter(None, parts))

    # Clean up and add extension
    filename = clean_filename(filename + extension)

    return filename


def format_document_type(doc_type: str) -> str:
    """
    Format document type for use in filenames.

    Args:
        doc_type: Raw document type

    Returns:
        Formatted document type
    """
    type_mapping = {
        "invoice": "Invoice",
        "receipt": "Receipt",
        "contract": "Contract",
        "agreement": "Agreement",
        "proposal": "Proposal",
        "report": "Report",
        "statement": "Statement",
        "tax": "TaxDoc",
        "resume": "Resume",
        "cv": "CV",
        "letter": "Letter",
        "memo": "Memo",
        "presentation": "Presentation",
        "spreadsheet": "Spreadsheet",
        "form": "Form",
        "application": "Application",
        "certificate": "Certificate",
        "license": "License",
        "policy": "Policy",
        "manual": "Manual",
        "guide": "Guide",
    }

    # Try exact match first
    doc_type_lower = doc_type.lower()
    if doc_type_lower in type_mapping:
        return type_mapping[doc_type_lower]

    # Try partial match
    for key, value in type_mapping.items():
        if key in doc_type_lower:
            return value

    # Default: capitalize first letter
    return doc_type.capitalize()


def clean_company_name(company: str) -> str:
    """
    Clean company name for use in filenames.

    Examples:
        "Amazon.com Inc." → "Amazon"
        "The Home Depot" → "HomeDepot"

    Args:
        company: Company name

    Returns:
        Cleaned company name
    """
    # Remove common suffixes
    suffixes = [
        "Inc.",
        "Inc",
        "LLC",
        "Ltd.",
        "Ltd",
        "Corporation",
        "Corp.",
        "Corp",
        "Company",
        "Co.",
        "Co",
        "Group",
        "Holdings",
        "Limited",
        "GmbH",
        "AG",
        "SA",
        "PLC",
        "LLP",
        "LP",
    ]

    name = company
    for suffix in suffixes:
        name = re.sub(rf"\s*\b{re.escape(suffix)}\b\.?\s*$", "", name, flags=re.I)

    # Remove "The" from beginning
    name = re.sub(r"^\s*the\s+", "", name, flags=re.I)

    # Remove special characters and spaces
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "", name)  # Remove all spaces for filename

    # Limit length
    return name[:30]


def format_person_name(person: str) -> str:
    """
    Format person name for use in filenames.

    Examples:
        "John A. Doe" → "JohnDoe"
        "doe, jane" → "JaneDoe"

    Args:
        person: Person's name

    Returns:
        Formatted name
    """
    # Handle "Last, First" format
    if "," in person:
        parts = person.split(",", 1)
        person = f"{parts[1].strip()} {parts[0].strip()}"

    # Split into parts
    parts = person.split()

    # Take first and last name only
    if len(parts) >= 2:
        formatted = f"{parts[0]}{parts[-1]}"
    else:
        formatted = "".join(parts)

    # Remove special characters
    formatted = re.sub(r"[^\w]", "", formatted)

    # Capitalize properly
    return formatted.capitalize()


def format_folder_path(
    category: str,
    subcategory: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[str] = None,
) -> str:
    """
    Format a human-readable folder path.

    Examples:
        ("Invoices", "Amazon", 2024, "March") → "Invoices/Amazon/2024/March"
        ("Projects", "ClientX") → "Projects/ClientX"

    Args:
        category: Main category
        subcategory: Optional subcategory
        year: Optional year
        month: Optional month name

    Returns:
        Formatted folder path
    """
    parts = [category]

    if subcategory:
        parts.append(subcategory)

    if year:
        parts.append(str(year))

    if month:
        # Ensure month is properly capitalized
        parts.append(month.capitalize())

    return "/".join(parts)


def humanize_file_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"

    units = ["KB", "MB", "GB", "TB"]
    size = float(size_bytes) / 1024

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} PB"


def format_time_ago(timestamp: datetime) -> str:
    """
    Format timestamp as human-readable time ago.

    Examples:
        "2 minutes ago"
        "3 hours ago"
        "Yesterday"
        "Last week"

    Args:
        timestamp: Datetime to format

    Returns:
        Human-readable time string
    """
    now = datetime.now()
    diff = now - timestamp

    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 172800:
        return "yesterday"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} days ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        return timestamp.strftime("%B %d, %Y")


def generate_unique_suffix(base_name: str, existing_names: List[str]) -> str:
    """
    Generate unique filename suffix if name already exists.

    Args:
        base_name: Base filename without extension
        existing_names: List of existing filenames

    Returns:
        Unique filename with suffix if needed
    """
    if base_name not in existing_names:
        return base_name

    counter = 2
    while f"{base_name}_{counter}" in existing_names:
        counter += 1

    return f"{base_name}_{counter}"


def format_month_name(month_number: int) -> str:
    """
    Convert month number to full month name.

    Args:
        month_number: Month (1-12)

    Returns:
        Full month name
    """
    try:
        return calendar.month_name[month_number]
    except (IndexError, KeyError):
        return f"Month{month_number}"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)].rstrip() + suffix


def create_screenshot_filename(original: str = None) -> str:
    """
    Create standardized filename for screenshots.

    Args:
        original: Original screenshot filename

    Returns:
        Formatted screenshot filename
    """
    timestamp = datetime.now()

    # Try to extract any useful info from original
    display_info = ""
    if original and "at" in original.lower():
        # macOS style: "Screenshot 2024-03-15 at 2.34.56 PM"
        display_info = "_macos"
    elif original and re.search(r"\d+x\d+", original):
        # Has resolution info
        match = re.search(r"(\d+x\d+)", original)
        if match:
            display_info = f"_{match.group(1)}"

    formatted_date = timestamp.strftime("%Y%m%d_%H%M%S")
    return f"screenshot_{formatted_date}{display_info}.png"
