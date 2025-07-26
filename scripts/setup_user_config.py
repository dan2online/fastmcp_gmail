#!/usr/bin/env python3
"""
FastMCP Gmail Configuration Setup
Helps set up centralized configuration in ~/.local/fastmcp_gmail/
"""

import os
import shutil
from pathlib import Path
import sys

def setup_user_config():
    """Set up centralized user configuration directory"""
    
    # Get directories
    home_dir = Path.home()
    config_dir = home_dir / ".local" / "fastmcp_gmail"
    project_dir = Path(__file__).parent.parent
    
    print(f"🏠 FastMCP Gmail Configuration Setup")
    print(f"=====================================")
    print(f"Setting up configuration in: {config_dir}")
    print()
    
    # Create config directory
    config_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created config directory: {config_dir}")
    
    # Files to move/copy
    files_to_handle = [
        ('credentials.json', 'Gmail API credentials'),
        ('token.json', 'Gmail authentication token'),
        ('.env.local', 'Local environment configuration')
    ]
    
    moved_files = []
    created_files = []
    
    for filename, description in files_to_handle:
        project_file = project_dir / filename
        config_file = config_dir / filename
        
        # Handle .env.local -> fastmcp_gmail.env
        if filename == '.env.local':
            config_file = config_dir / "fastmcp_gmail.env"
        
        if project_file.exists():
            if not config_file.exists():
                # Move file to config directory
                shutil.move(str(project_file), str(config_file))
                print(f"📁 Moved {description}: {project_file} → {config_file}")
                moved_files.append(filename)
            else:
                print(f"⚠️  {description} already exists in config directory: {config_file}")
        else:
            if not config_file.exists():
                # Create template/placeholder
                if filename == '.env.local':
                    # Create environment template
                    env_content = """# FastMCP Gmail Configuration
# This file is loaded from ~/.local/fastmcp_gmail/fastmcp_gmail.env

# Gmail API Configuration
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.modify

# Logging Configuration
LOG_LEVEL=INFO

# LLM Configuration
LLM_CONFIDENCE_THRESHOLD=0.85

# Email Processing Configuration
MAX_EMAILS_PER_REQUEST=50
DEFAULT_EMAIL_COUNT=10
INCLUDE_SPAM_TRASH=false
"""
                    config_file.write_text(env_content)
                    print(f"📝 Created environment template: {config_file}")
                    created_files.append('fastmcp_gmail.env')
                else:
                    print(f"❌ {description} not found in project: {project_file}")
            else:
                print(f"✅ {description} already exists: {config_file}")
    
    print()
    print("📋 Configuration Summary:")
    print(f"   Config directory: {config_dir}")
    
    if moved_files:
        print(f"   Moved files: {', '.join(moved_files)}")
    if created_files:
        print(f"   Created files: {', '.join(created_files)}")
    
    print()
    print("🎯 Next Steps:")
    print("   1. If you haven't already, download credentials.json from Google Cloud Console")
    print(f"   2. Save credentials.json to: {config_dir}/credentials.json")
    print(f"   3. Run 'make auth-setup' to authenticate")
    print(f"   4. Configure settings in: {config_dir}/fastmcp_gmail.env")
    
    print()
    print("💡 Benefits:")
    print("   - Sensitive files kept in secure user directory")
    print("   - Project directory stays clean")
    print("   - Easy to share project without credentials")
    print("   - Configuration persists across project updates")

if __name__ == "__main__":
    try:
        setup_user_config()
    except Exception as e:
        print(f"❌ Error setting up configuration: {e}")
        sys.exit(1)
