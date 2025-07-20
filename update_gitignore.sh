#!/bin/bash

# Add dev_folders to .gitignore

# Check if .gitignore exists, create if it doesn't
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore file..."
    touch .gitignore
fi

# Check if dev_folders is already in .gitignore
if grep -q "^dev_folders" .gitignore; then
    echo "⚠️  dev_folders is already in .gitignore"
else
    # Add a newline if file doesn't end with one
    [ -s .gitignore ] && [ "$(tail -c 1 .gitignore | wc -l)" -eq 0 ] && echo "" >>.gitignore

    # Add dev_folders section
    echo "# Development test folders" >>.gitignore
    echo "dev_folders/" >>.gitignore
    echo "" >>.gitignore

    echo "✅ Added dev_folders/ to .gitignore"
fi

# Also add other development-specific items while we're at it
echo "Adding other development items to .gitignore..."

# Function to add item if not already present
add_to_gitignore() {
    if ! grep -q "^$1" .gitignore; then
        echo "$1" >>.gitignore
    fi
}

# Add common development items
add_to_gitignore "*.pyc"
add_to_gitignore "__pycache__/"
add_to_gitignore ".env"
add_to_gitignore ".env.local"
add_to_gitignore "venv/"
add_to_gitignore "env/"
add_to_gitignore ".vscode/"
add_to_gitignore ".idea/"
add_to_gitignore "*.log"
add_to_gitignore ".DS_Store"
add_to_gitignore "data/cache/*"
add_to_gitignore "data/uploads/*"
add_to_gitignore "!data/cache/.gitkeep"
add_to_gitignore "!data/uploads/.gitkeep"

echo "✅ .gitignore updated successfully!"
echo ""
echo "📄 Current .gitignore contents:"
echo "--------------------------------"
cat .gitignore
