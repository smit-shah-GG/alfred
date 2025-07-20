#!/bin/bash

# Create development folders for Alfred testing

# Create the main dev_folders structure
mkdir -p dev_folders/watched/downloads
mkdir -p dev_folders/watched/desktop
mkdir -p dev_folders/watched/documents

# Create organized folder (where Alfred will put files)
# Let's create a basic structure Alfred might use
mkdir -p dev_folders/organized/Documents/Invoices/2024
mkdir -p dev_folders/organized/Documents/Invoices/2025
mkdir -p dev_folders/organized/Documents/Contracts
mkdir -p dev_folders/organized/Documents/Reports
mkdir -p dev_folders/organized/Documents/Projects
mkdir -p dev_folders/organized/Documents/Personal
mkdir -p dev_folders/organized/Documents/Screenshots
mkdir -p dev_folders/organized/Documents/Archives

# # Create some test files to play with (optional)
# echo "Creating some test files in watched folders..."

# # Create dummy test files
# touch "dev_folders/watched/downloads/invoice.pdf"
# touch "dev_folders/watched/downloads/document.docx"
# touch "dev_folders/watched/downloads/screenshot_2024-03-15.png"
# touch "dev_folders/watched/downloads/asdfasdf.pdf"
# touch "dev_folders/watched/downloads/untitled(1).txt"

# touch "dev_folders/watched/desktop/important_file.xlsx"
# touch "dev_folders/watched/desktop/TODO.txt"
# touch "dev_folders/watched/desktop/random_notes.md"

# Create a README in dev_folders to explain what this is
cat >dev_folders/README.md <<'EOF'
# Development Folders

This directory contains test folders for Alfred development.

## Structure:
- `watched/` - Folders that Alfred monitors for new files
  - `downloads/` - Simulates user's Downloads folder
  - `desktop/` - Simulates user's Desktop
  - `documents/` - Simulates user's Documents folder

- `organized/` - Where Alfred moves organized files
  - Pre-structured with common folder patterns
  - Alfred will create new folders as needed

## Usage:
1. Drop test files into any `watched/` subfolder
2. Run Alfred
3. Watch files get organized into `organized/` folder

This entire directory is gitignored and for local testing only.
EOF

echo "✅ Development folders created successfully!"
echo "📁 Structure:"
tree dev_folders -L 3 2>/dev/null || find dev_folders -type d | head -20
