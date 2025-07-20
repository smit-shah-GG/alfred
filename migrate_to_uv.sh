#!/bin/bash
# migrate_to_uv.sh - Migrate Alfred from pip to uv

echo "🎩 Migrating Alfred to UV package manager"
echo "========================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo ""
    echo "Install it with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Or on Windows:"
    echo "  irm https://astral.sh/uv/install.ps1 | iex"
    exit 1
fi

echo "✅ UV is installed: $(uv --version)"

# Remove old virtual environment
if [ -d "venv" ]; then
    echo "🗑️  Removing old venv directory..."
    rm -rf venv
fi

if [ -d ".venv" ]; then
    echo "🗑️  Removing existing .venv directory..."
    rm -rf .venv
fi

# Create new virtual environment with uv
echo "📦 Creating new virtual environment with UV..."
uv venv

# Detect OS and set activation command
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE_CMD=".venv\\Scripts\\activate"
else
    ACTIVATE_CMD="source .venv/bin/activate"
fi

echo ""
echo "✅ Virtual environment created!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   $ACTIVATE_CMD"
echo ""
echo "2. Install dependencies:"
echo "   uv pip install -e \".[dev]\""
echo ""
echo "3. Copy your .env file:"
echo "   cp .env.example .env"
echo "   # Then add your GEMINI_API_KEY"
echo ""
echo "4. Run the setup:"
echo "   python scripts/setup.py"
echo ""
echo "🚀 UV is 10-100x faster than pip. Enjoy the speed!"
