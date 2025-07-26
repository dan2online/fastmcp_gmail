#!/usr/bin/env python3
"""
Setup FastMCP Gmail server for Claude Desktop
"""

import json
import os
from pathlib import Path
import sys
import platform

def find_claude_config_path():
    """Find Claude Desktop configuration file path"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        return Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    else:  # Linux and others
        return Path.home() / ".config" / "claude" / "claude_desktop_config.json"

def setup_claude_desktop():
    """Set up FastMCP Gmail server in Claude Desktop"""
    
    # Get project path
    project_path = Path(__file__).parent.parent.absolute()
    mcp_server_path = project_path / "mcp_server.py"
    
    # Find Claude Desktop config
    config_path = find_claude_config_path()
    
    print(f"🖥️  FastMCP Gmail - Claude Desktop Setup")
    print(f"========================================")
    print(f"Project path: {project_path}")
    print(f"Claude config: {config_path}")
    print()
    
    # Check if mcp_server.py exists (FastMCP implementation)
    if not mcp_server_path.exists():
        print(f"❌ FastMCP server not found: {mcp_server_path}")
        print(f"   Make sure you're running this from the project directory")
        return False
    
    # Create config directory if needed
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read existing config or create new one
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON in {config_path}, creating backup...")
            backup_path = config_path.with_suffix('.json.backup')
            config_path.rename(backup_path)
            config = {}
    else:
        config = {}
    
    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    # Add FastMCP Gmail server - use virtual environment Python
    venv_python = project_path / ".venv" / "bin" / "python"
    if not venv_python.exists():
        print(f"⚠️  Virtual environment not found at {venv_python}")
        print(f"   Please run 'make setup' first to create the virtual environment")
        return False
    
    server_config = {
        "command": str(venv_python),
        "args": [str(mcp_server_path)],
        "env": {
            "PYTHONPATH": str(project_path)
        }
    }
    
    config["mcpServers"]["fastmcp-gmail"] = server_config
    
    # Write config back
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ FastMCP Gmail server added to Claude Desktop config")
        print(f"   Config file: {config_path}")
        print()
        print(f"🔧 Server Configuration:")
        print(f"   Name: fastmcp-gmail")
        print(f"   Command: {venv_python}")
        print(f"   Script: {mcp_server_path}")
        print()
        print(f"🎯 Next Steps:")
        print(f"   1. Restart Claude Desktop")
        print(f"   2. Look for Gmail tools in Claude's tool panel")
        print(f"   3. Test with: 'What are my latest emails?'")
        print()
        print(f"🆘 Troubleshooting:")
        print(f"   - Check server logs: tail -f {project_path}/logs/fastmcp_server.log")
        print(f"   - Test manually: {venv_python} {mcp_server_path}")
        print(f"   - Verify Gmail: make test-gmail")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to write config: {e}")
        return False

if __name__ == "__main__":
    try:
        success = setup_claude_desktop()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
