# 📋 FastMCP Gmail - Quick Command Reference

> **📖 See [../README.md](../README.md) for full project details**  
> **🔧 See [GMAIL_SETUP.md](GMAIL_SETUP.md) for Google Cloud Console setup**

## ⚡ New User Quick Start

```bash
make setup              # 1. Setup environment  
make setup-user-config  # 2. Centralized config (recommended)
make fix-gmail-auth     # 3. Get Google Cloud guide → download credentials.json
make auth-setup         # 4. Authenticate (opens browser)
make test-gmail         # 5. Test connection  
make demo               # 6. Try it out!

# Optional: Claude Desktop Integration
make setup-claude-desktop  # 7. Set up MCP server for Claude Desktop
```

## 🎯 Daily Commands

```bash
make run            # Process latest email with AI
make demo           # Enhanced Gmail reader demo  
make summary        # Generate daily email summary
make status         # Check project status
```

## 🔧 Setup & Troubleshooting

```bash
make verify-setup   # Check if ready for Gmail
make setup-user-config # Set up centralized configuration
make fix-gmail-auth # Gmail authentication help
make auth-setup     # Complete Gmail OAuth
make test-gmail     # Test Gmail connection  
make integration-test # Full integration test
```

## 🧪 Development

```bash
make test           # Run test suite
make lint           # Code linting
make format         # Format code  
make clean          # Clean cache/temp files
make help           # Show all commands
```

## 🚨 Quick Fixes

| Problem | Solution |
|---------|----------|
| `Access blocked: App not verified` | `make fix-gmail-auth` → add test user |
| `credentials.json not found` | Download from Google Cloud Console |
| `Authentication fails` | `rm token.json && make auth-setup` |
| `Commands not working` | `make verify-setup` |

---
*All commands work from project root. Run `make help` for complete list.*
