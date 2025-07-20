#!/usr/bin/env python3
"""
Test script to demonstrate Alfred utils functionality.

Run this from the project root: python scripts/test_utils.py
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import *
import json
from datetime import datetime


def test_filename_cleaning():
    """Test filename cleaning functionality."""
    print("\n=== Testing Filename Cleaning ===")

    test_cases = [
        "invoice__FINAL_v2 (1) - Copy.pdf",
        "ScreenShot 2024-03-15 at 2.34.56 PM.png",
        "asdfasdf.pdf",
        "Document(1)(2)(3) - Copy - Copy.docx",
        "    spaces    everywhere    .txt",
        "CAPSLOCK_FILE_NAME_V3_FINAL_FINAL.PDF",
        "αβγδ unicode χαρακτήρες.pdf",  # Unicode characters
        "my/file\\with:invalid*chars?.doc",
    ]

    for filename in test_cases:
        cleaned = clean_filename(filename)
        print(f"Original: {filename:50} → Cleaned: {cleaned}")


def test_file_validation():
    """Test file validation functionality."""
    print("\n\n=== Testing File Validation ===")

    # Test filename validation
    test_names = [
        ("normal_file.pdf", True),
        ("CON.txt", False),  # Reserved Windows name
        ("file/with/slashes.doc", False),
        ("", False),
        ("a" * 300 + ".txt", False),  # Too long
    ]

    for filename, should_pass in test_names:
        try:
            validate_filename(filename)
            result = "✓ Valid"
        except ValidationError as e:
            result = f"✗ Invalid: {e}"

        print(f"Filename: {filename:30} → {result}")

    # Test supported file types
    print("\n--- Supported File Types ---")
    test_files = [
        "document.pdf",
        "spreadsheet.xlsx",
        "image.jpg",
        "executable.exe",
        "archive.zip",
        "video.mp4",
    ]

    for file in test_files:
        path = Path(file)
        supported = is_supported_file_type(path)
        print(f"{file:20} → {'✓ Supported' if supported else '✗ Not supported'}")


def test_organization_paths():
    """Test organization path building."""
    print("\n\n=== Testing Organization Path Building ===")

    base_dir = Path("dev_folders/organized/Documents")

    # Test different organization strategies
    examples = [
        {
            "desc": "Invoice with date-based organization",
            "category": "Invoices",
            "subcategories": ["Amazon"],
            "filename": "Amazon_Invoice_2024-03-15.pdf",
            "date_based": True,
        },
        {
            "desc": "Project without date",
            "category": "Projects",
            "subcategories": ["ClientX", "Contracts"],
            "filename": "Service_Agreement_v2.pdf",
            "date_based": False,
        },
        {
            "desc": "Screenshot with date folders",
            "category": "Screenshots",
            "subcategories": None,
            "filename": "screenshot_20240315_143022.png",
            "date_based": True,
        },
    ]

    for example in examples:
        path = build_organized_path(
            base_dir=base_dir,
            category=example["category"],
            subcategories=example["subcategories"],
            filename=example["filename"],
            date_based=example["date_based"],
        )
        print(f"\n{example['desc']}:")
        print(f"  → {path}")


def test_descriptive_filenames():
    """Test descriptive filename generation."""
    print("\n\n=== Testing Descriptive Filename Generation ===")

    test_cases = [
        {
            "document_type": "invoice",
            "entities": {
                "company": "Amazon.com Inc.",
                "invoice_number": "12345",
                "document_date": datetime(2024, 3, 15),
            },
            "original": "download.pdf",
        },
        {
            "document_type": "contract",
            "entities": {"person": "John A. Doe", "reference": "AGR-2024-0315"},
            "original": "scan0001.pdf",
        },
        {
            "document_type": "report",
            "entities": {"company": "The Home Depot"},
            "original": "untitled.docx",
        },
    ]

    for case in test_cases:
        filename = create_descriptive_filename(
            document_type=case["document_type"],
            entities=case["entities"],
            original_name=case["original"],
        )
        print(f"\nOriginal: {case['original']}")
        print(f"Type: {case['document_type']}")
        print(f"Entities: {json.dumps(case['entities'], default=str, indent=2)}")
        print(f"Generated: {filename}")


def test_file_operations():
    """Test file operations in dev folders."""
    print("\n\n=== Testing File Operations ===")

    # Create test files
    test_dir = Path("dev_folders/watched/downloads")
    ensure_directory(test_dir)

    # Create a test file
    test_file = test_dir / "test_document.txt"
    created_file = create_test_file(test_file, "This is a test document for Alfred.")
    print(f"Created test file: {created_file}")

    # Get file metadata
    metadata = get_file_metadata(created_file)
    print(f"\nFile Metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")

    # Test safe move
    dest_dir = Path("dev_folders/organized/Documents/Tests")
    dest_file = dest_dir / "test_document_organized.txt"

    try:
        moved_file = safe_move_file(created_file, dest_file)
        print(f"\nMoved file to: {moved_file}")
    except FileOperationError as e:
        print(f"\nMove failed: {e}")


def test_formatting_helpers():
    """Test various formatting helpers."""
    print("\n\n=== Testing Formatting Helpers ===")

    # Test file size formatting
    sizes = [500, 1024, 1048576, 1073741824, 1099511627776]
    print("\nFile Sizes:")
    for size in sizes:
        print(f"  {size:15,} bytes → {humanize_file_size(size)}")

    # Test time formatting
    print("\nTime Formatting:")
    from datetime import timedelta

    now = datetime.now()

    times = [
        (now - timedelta(seconds=30), "30 seconds ago"),
        (now - timedelta(minutes=5), "5 minutes ago"),
        (now - timedelta(hours=2), "2 hours ago"),
        (now - timedelta(days=1), "yesterday"),
        (now - timedelta(days=7), "a week ago"),
    ]

    for time, desc in times:
        formatted = format_time_ago(time)
        print(f"  {desc:20} → {formatted}")


def main():
    """Run all tests."""
    print("🎩 Alfred Utils Test Suite")
    print("=" * 60)

    test_filename_cleaning()
    test_file_validation()
    test_organization_paths()
    test_descriptive_filenames()
    test_file_operations()
    test_formatting_helpers()

    print("\n\n✅ All tests completed!")
    print("\nNote: Check dev_folders/organized/ to see the moved test file.")


if __name__ == "__main__":
    main()
