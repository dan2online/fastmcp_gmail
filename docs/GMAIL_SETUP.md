# Gmail API Setup Guide

> **📖 See [../README.md](../README.md) for complete project overview and make commands**  
> **📋 See [WORKFLOW_CHEATSHEET.md](WORKFLOW_CHEATSHEET.md) for quick command reference**

## 🚀 Quick Setup (6 Commands)

```bash
make setup              # 1. Setup environment
make setup-user-config  # 2. Set up centralized config (recommended)
make fix-gmail-auth     # 3. Get Google Cloud Console guide  
# (Download credentials.json to ~/.local/fastmcp_gmail/ or project root)
make auth-setup         # 4. Authenticate with Gmail
make test-gmail         # 5. Test connection
make demo               # 6. Try the demo

# Optional: Use with Claude Desktop
make setup-claude-desktop  # 7. Set up MCP server for Claude Desktop
```

> **💡 Tip**: Run `make help` to see all available commands  
> **🖥️ Claude Desktop**: Use `make setup-claude-desktop` for interactive setup
> **🔧 VS Code**: Use `make setup-vscode-mcp` for development environment

---

## 🔧 Google Cloud Console Setup

**Essential Steps** (follow `make fix-gmail-auth` for detailed guidance):

1. **Create Google Cloud Project** → Enable Gmail API
2. **OAuth Consent Screen** → Add yourself as test user (for external apps)
3. **Create Credentials** → Desktop app → Download as `credentials.json`

## 🚨 Common Issues

### "Access blocked: App not verified" (Error 403)
```bash
make fix-gmail-auth  # Follow the test user setup guide
```

### Authentication fails
```bash
rm token.json       # Clear old tokens
make auth-setup     # Re-authenticate
```

### Commands not working
```bash
make verify-setup   # Check what's missing
make help          # See all commands
```

## 🔒 Security Notes

- **Centralized Config**: Use `make setup-user-config` to store sensitive files in `~/.local/fastmcp_gmail/`
- Never commit `credentials.json` or `token.json` to git
- Files are automatically loaded from user config directory first, then project directory
- Use `~/.local/fastmcp_gmail/fastmcp_gmail.env` for environment configuration
- All processing happens locally (privacy-focused)

---
*For detailed troubleshooting and advanced config, see the original documentation in git history*
