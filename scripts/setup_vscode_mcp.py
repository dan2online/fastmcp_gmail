#!/usr/bin/env python3
"""
Setup FastMCP Gmail server for VS Code
"""

import json
import os
from pathlib import Path
import sys
import platform

def setup_vscode_mcp():
    """Set up FastMCP Gmail server for VS Code"""
    
    # Get project path
    project_path = Path(__file__).parent.parent.absolute()
    mcp_server_path = project_path / "mcp_server.py"
    
    print(f"🖥️  FastMCP Gmail - VS Code Setup")
    print(f"================================")
    print(f"Project path: {project_path}")
    print()
    
    # Check if mcp_server.py exists (FastMCP implementation)
    if not mcp_server_path.exists():
        print(f"❌ FastMCP server not found: {mcp_server_path}")
        return False
    
    # Check virtual environment
    venv_python = project_path / ".venv" / "bin" / "python"
    if not venv_python.exists():
        print(f"⚠️  Virtual environment not found at {venv_python}")
        print(f"   Please run 'make setup' first to create the virtual environment")
        return False
    
    print(f"✅ Found MCP server: {mcp_server_path}")
    print(f"✅ Found Python environment: {venv_python}")
    print()
    
    # Option 1: Continue Extension
    print(f"📦 Option 1: Continue Extension (Recommended)")
    print(f"============================================")
    print(f"1. Install the Continue extension:")
    print(f"   - Open VS Code Extensions (Ctrl+Shift+X)")
    print(f"   - Search for 'Continue'")
    print(f"   - Install 'Continue - open-source AI code assistant'")
    print()
    print(f"2. Configure Continue with MCP server:")
    
    # Create Continue config
    continue_config = {
        "models": [
            {
                "title": "Claude 3.5 Sonnet",
                "provider": "anthropic",
                "model": "claude-3-5-sonnet-20241022",
                "apiKey": "[YOUR_ANTHROPIC_API_KEY]"
            }
        ],
        "mcpServers": {
            "fastmcp-gmail": {
                "command": str(venv_python),
                "args": [str(mcp_server_path)],
                "env": {
                    "PYTHONPATH": str(project_path)
                }
            }
        }
    }
    
    # Find Continue config path
    continue_config_path = Path.home() / ".continue" / "config.json"
    
    print(f"   Add this to your Continue config at: {continue_config_path}")
    print(f"   ```json")
    print(f"   {json.dumps(continue_config, indent=2)}")
    print(f"   ```")
    print()
    
    # Option 2: Cline Extension  
    print(f"📦 Option 2: Cline Extension")
    print(f"============================")
    print(f"1. Install the Cline extension:")
    print(f"   - Search for 'Cline' in VS Code Extensions")
    print(f"   - Install 'Cline' by saoudrizwan")
    print()
    print(f"2. Cline automatically supports MCP servers")
    print(f"   - Use Command Palette: 'Cline: Add MCP Server'")
    print(f"   - Add server with command: {venv_python}")
    print(f"   - Args: {mcp_server_path}")
    print()
    
    # Option 3: Manual MCP testing
    print(f"🔧 Option 3: Manual Testing")
    print(f"===========================")
    print(f"Test the MCP server directly in VS Code terminal:")
    print(f"```bash")
    print(f"cd {project_path}")
    print(f"")
    print(f"# Test connection")
    print(f'echo \'{{"method":"tools/list","jsonrpc":"2.0","id":1}}\' | {venv_python} {mcp_server_path}')
    print(f"")
    print(f"# Test Gmail connection")
    print(f'echo \'{{"method":"tools/call","params":{{"name":"test_gmail_connection","arguments":{{}}}},"jsonrpc":"2.0","id":2}}\' | {venv_python} {mcp_server_path}')
    print(f"")
    print(f"# Read latest emails")
    print(f'echo \'{{"method":"tools/call","params":{{"name":"read_latest_emails","arguments":{{"count":2}}}},"jsonrpc":"2.0","id":3}}\' | {venv_python} {mcp_server_path}')
    print(f"```")
    print()
    
    # Option 4: GitHub Copilot Chat with MCP
    print(f"🤖 Option 4: GitHub Copilot with MCP Extensions")
    print(f"===============================================")
    print(f"Install MCP-compatible extensions:")
    print(f"- 'Copilot MCP' by automatalabs")
    print(f"- 'MCP-Client' by m1self") 
    print(f"- 'VSCode MCP Server' by semanticworkbenchteam")
    print()
    
    # Write a simple launcher script
    launcher_script = project_path / "run_mcp_server.sh"
    with open(launcher_script, 'w') as f:
        f.write(f"""#!/bin/bash
# FastMCP Gmail Server Launcher for VS Code
cd "{project_path}"
"{venv_python}" "{mcp_server_path}" "$@"
""")
    
    # Make executable
    os.chmod(launcher_script, 0o755)
    
    print(f"✅ Created launcher script: {launcher_script}")
    print()
    print(f"🎯 Quick Start Commands:")
    print(f"   - Test server: ./run_mcp_server.sh")
    print(f"   - Check Gmail: make test-gmail")
    print(f"   - View logs: tail -f logs/fastmcp_server.log")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = setup_vscode_mcp()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
