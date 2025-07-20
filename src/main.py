"""
main.py - Entry point for Alfred

This will be the main CLI interface for Alfred.
For now, it's a placeholder that shows Alfred is working.
"""

import sys
from pathlib import Path
from .config import config
from .utils import clean_filename


def main():
    """Main entry point for Alfred CLI."""
    print("🎩 Alfred AI File Butler")
    print("=" * 40)

    # Display configuration
    config.display_config()

    # Simple demo
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        cleaned = clean_filename(filename)
        print(f"\nCleaning filename:")
        print(f"  Original: {filename}")
        print(f"  Cleaned:  {cleaned}")
    else:
        print("\nUsage: alfred <filename>")
        print("Example: alfred 'invoice__FINAL_v2 (1) - Copy.pdf'")

    print("\n💡 Full UI coming soon! For now, run:")
    print("   streamlit run src/ui/streamlit_app.py")


if __name__ == "__main__":
    main()
