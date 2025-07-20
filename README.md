# 🎩 Alfred - Your AI File Butler

> *"In a world of digital chaos, be the butler they need."*

Alfred is an intelligent file organization system that runs quietly in the background, automatically organizing your digital mess into a perfectly structured file system. Using Google's Gemini 2.5 AI, Alfred understands your documents and puts them exactly where they should be - and where you can actually find them.

## ✨ The Magic

Imagine never losing a file again. Alfred watches your Downloads, Desktop, and Documents folders, instantly organizing new files as they appear:

- 📄 **That invoice you just downloaded?** → `Documents/Invoices/2024/Amazon_Invoice_March.pdf`
- 📊 **Random spreadsheet from email?** → `Documents/Projects/ClientName/Budget_Analysis_2024.xlsx`
- 📸 **Screenshot mess on desktop?** → `Documents/Screenshots/2024/March/`
- 📝 **"asdfasdf.pdf"?** → Alfred figures out it's actually your tax return and files it properly

## 🚀 Features

### 🧠 Intelligent Understanding
- **Reads ANY document**: PDFs, images, spreadsheets, presentations - Gemini 2.5 understands them all
- **Context-aware filing**: Knows "Invoice_123" near "Contract_ABC" means they're related
- **Learns your style**: Adapts to how YOU organize (even if you call invoices "bills")

### 📁 Human-Friendly Organization
- **No cryptic folders**: Files go to logical places like `/Documents/Invoices/2024/`
- **Works with your system**: Respects Windows, macOS, and Linux conventions
- **Always findable**: Even if Alfred stops, your files are right where you'd expect

### 🎭 Personality Plus
- **British butler charm**: "I've taken the liberty of organizing your 'definitely_organized' folder, sir."
- **Gentle mockery**: "Another 'untitled.docx'? How creative. I'll handle it."
- **Celebrates wins**: "Splendid! You actually named this file properly!"

### 🔒 Secure by Design
- **Your files stay yours**: Optional encryption for sensitive documents
- **Local first**: Works offline, syncs when connected
- **Privacy focused**: We can't see your files, even if we wanted to

## 📋 Requirements

- Python 3.10+
- Google Cloud account (for Gemini API)
- 4GB RAM minimum
- Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)

## 🛠️ Installation

### Quick Start (Coming Soon)
```bash
# One-line installer for the brave
curl -sSL https://get.alfred-ai.com | bash
```

### Developer Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/alfred-file-butler.git
   cd alfred-file-butler
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Add your Gemini API key
   # Get one at: https://makersuite.google.com/app/apikey
   echo "GEMINI_API_KEY=your-key-here" >> .env
   ```

4. **Run Alfred**
   ```bash
   # Development mode (with UI)
   python src/main.py
   
   # Background service mode
   python src/main.py --daemon
   ```

## 🎮 Usage

### First Run
1. Alfred will ask which folders to watch (or use defaults)
2. Grant file system permissions when prompted
3. That's it! Alfred starts organizing immediately

### System Tray/Menu Bar
- **📁 Open Organized Files**: Quick access to your Documents
- **⏸️ Pause Alfred**: Take a break from organization
- **🔄 Organize Now**: Manually trigger organization
- **⚙️ Settings**: Customize Alfred's behavior
- **💬 Alfred Says...**: See recent organization activities

### Example Interactions

**Your messy Downloads folder:**
```
Downloads/
├── invoice.pdf
├── download (1).pdf
├── screenshot_2024-03-15.png
├── important_doc_FINAL_v2_ACTUALLY_FINAL.docx
└── qwerty.xlsx
```

**After Alfred's magic:**
```
Documents/
├── Invoices/
│   └── 2024/
│       └── March/
│           └── SupplierName_Invoice_2024-03-15.pdf
├── Projects/
│   └── ProjectX/
│       └── Proposal_Final_Version.docx
├── Screenshots/
│   └── 2024/
│       └── March/
│           └── Screenshot_2024-03-15_143022.png
└── Financial/
    └── Reports/
        └── Quarterly_Report_Q1_2024.xlsx
```

## 🔧 Configuration

Alfred's behavior can be customized via `~/.alfred/config.json`:

```json
{
  "watch_folders": [
    "~/Downloads",
    "~/Desktop",
    "~/Documents/Unsorted"
  ],
  "organization_style": "type_based",  // or "project_based", "time_based"
  "alfred_personality": "charming",     // or "sassy", "professional"
  "auto_rename": true,
  "ask_before_moving": false
}
```

## 🧪 Development

### Running Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Full test suite
pytest
```

### Building from Source
```bash
# Build executable
python scripts/build.py

# Platform-specific builds
python scripts/build.py --platform windows
python scripts/build.py --platform macos
python scripts/build.py --platform linux
```

### Contributing
We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📊 How It Works

```mermaid
graph LR
    A[New File Appears] --> B[Alfred Detects]
    B --> C[Gemini 2.5 Analyzes]
    C --> D[Determines Category]
    D --> E[Moves to Right Folder]
    E --> F[Notifies with Sass]
```

1. **File Watcher**: Monitors specified folders for new files
2. **AI Analysis**: Gemini 2.5 reads and understands the document
3. **Smart Categorization**: Determines the best location based on content
4. **Gentle Filing**: Moves file to human-readable location
5. **Witty Notification**: Alfred comments on your filing habits

## 🐛 Troubleshooting

### Alfred isn't organizing files
- Check if Alfred is running (system tray icon)
- Verify folder permissions
- Check logs at `~/.alfred/logs/`

### Files going to wrong places
- Alfred learns from corrections - just move the file where you want it
- Adjust organization rules in Settings
- Check if document type detection is working

### Performance issues
- Reduce number of watched folders
- Enable "batch processing" mode
- Check API rate limits

## 🗺️ Roadmap

- [x] Basic file organization
- [x] Gemini 2.5 integration
- [x] System tray application
- [ ] Learning from user corrections
- [ ] Team sharing features
- [ ] Mobile app for remote organization
- [ ] Integration with cloud storage
- [ ] Custom organization rules UI
- [ ] Multiple language support

## 📜 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Google's Gemini team for the incredible AI
- The ADK team for making agent development delightful
- Every person who's ever lost a file in their Downloads folder
- British butlers everywhere for the inspiration

## 💬 Alfred Says...

*"I do hope you'll find my services satisfactory. Your digital chaos doesn't stand a chance. Now, shall we begin organizing that Downloads folder of yours? I promise to be gentle with your... creative... file naming choices."*

---

<p align="center">
  Made with 🎩 by people who hate messy folders
</p>

<p align="center">
  <a href="https://alfred-ai.com">Website</a> •
  <a href="https://docs.alfred-ai.com">Documentation</a> •
  <a href="https://twitter.com/alfred_ai">Twitter</a> •
  <a href="https://discord.gg/alfred">Discord</a>
</p>
