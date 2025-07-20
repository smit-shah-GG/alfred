#!/bin/bash

# Create Project Synergy (Alfred) file structure

# Create root level files
touch .env.example
touch .gitignore
touch requirements.txt
touch docker-compose.yml
touch Dockerfile
touch alfred.service
touch alfred.plist
touch alfred_installer.iss

# Create src directory structure
mkdir -p src/agents
mkdir -p src/core
mkdir -p src/models
mkdir -p src/api
mkdir -p src/ui/components
mkdir -p src/ui/styles
mkdir -p src/utils

# Create src files
touch src/__init__.py
touch src/main.py
touch src/config.py

# Create agents files
touch src/agents/__init__.py
touch src/agents/alfred.py
touch src/agents/analyzer.py
touch src/agents/organizer.py
touch src/agents/security_agent.py

# Create core files
touch src/core/__init__.py
touch src/core/file_processor.py
touch src/core/gemini_client.py
touch src/core/storage_manager.py
touch src/core/encryption.py
touch src/core/cache_manager.py

# Create models files
touch src/models/__init__.py
touch src/models/file_metadata.py
touch src/models/organization_rules.py
touch src/models/user_preferences.py

# Create api files
touch src/api/__init__.py
touch src/api/routes.py
touch src/api/websocket.py

# Create ui files
touch src/ui/__init__.py
touch src/ui/streamlit_app.py

# Create ui/components files
touch src/ui/components/file_uploader.py
touch src/ui/components/file_browser.py
touch src/ui/components/alfred_chat.py
touch src/ui/components/analytics_dash.py

# Create ui/styles files
touch src/ui/styles/custom.css

# Create utils files
touch src/utils/__init__.py
touch src/utils/helpers.py
touch src/utils/validators.py
touch src/utils/formatters.py

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures

# Create data directories
mkdir -p data/cache
mkdir -p data/uploads
mkdir -p data/configs

# Create scripts directory and files
mkdir -p scripts
touch scripts/setup.py
touch scripts/migrate.py
touch scripts/cleanup.py

# Create docs directory and files
mkdir -p docs
touch docs/API.md
touch docs/DEPLOYMENT.md
touch docs/SECURITY.md

echo "✅ Project Synergy file structure created successfully!"
echo "📁 Created directories:"
find . -type d | wc -l
echo "📄 Created files:"
find . -type f | wc -l
