# FastMCP Gmail - AI-Powered Email Assistant

A privacy-focused Gmail AI assistant that uses local LLM processing via Ollama to generate intelligent email responses and summaries. Built with FastMCP framework following the Model Context Protocol (MCP) for reliable AI interactions with **Claude Desktop** and **VS Code** integration.

## 🚀 Features

- **FastMCP Server**: Full MCP server implementation with 6 specialized Gmail tools
- **Multi-Platform Support**: Works with Claude Desktop, VS Code (Continue/Cline), and direct MCP clients
- **Smart Email Processing**: Fetches and processes Gmail messages using Google API
- **Local AI Processing**: Uses Ollama with Llama3 for privacy-focused local inference
- **Intelligent Caching**: JSON-based response caching to avoid redundant API calls
- **Confidence Scoring**: Only accepts high-confidence AI responses (≥85%)
- **Email Summarization**: Generates daily email summaries for unread messages with AI analysis
- **Professional Replies**: Automatically generates professional email responses
- **Conversation Logging**: Markdown-based logging of all AI interactions
- **Streaming Responses**: Real-time AI response streaming
- **Privacy Testing**: Comprehensive privacy validation and sensitive data protection
- **Gmail Search**: Advanced email search with query parameters and filters

## 📁 Project Structure

```
fastmcp_gmail/
├── main.py                     # Main email processing script
├── mcp_server.py               # FastMCP server with 6 Gmail tools
├── send_email_summary.py       # Daily email summary generator
├── requirements.txt            # Python dependencies
├── Makefile                    # Project automation with 30+ commands
├── GMAIL_SETUP.md             # Gmail API setup guide
├── core/
│   ├── mcp_agent.py           # Core MCP agent with confidence handling
│   ├── gmail_client.py        # Gmail API integration
│   ├── gmail_reader.py        # Enhanced Gmail reading functionality
│   ├── ollama_llm.py          # Ollama LLM integration
│   ├── llm_cache.py           # Response caching system
│   ├── llm_log.py             # Conversation logging
│   └── email_summarizer.py    # Email summarization logic
├── tests/
│   ├── manual/                # Manual interactive tests
│   │   └── test_real_setup.py # Gmail setup verification
│   ├── test_recent_emails.py  # Gmail email reading tests
│   ├── test_llm_privacy.py    # Privacy and security validation
│   ├── test_privacy_enhanced.py # Enhanced privacy analysis
│   └── test_*.py              # Automated unit tests (80+ tests)
├── scripts/
│   ├── fix_gmail_verification.py # Gmail troubleshooting utility
│   ├── setup_claude_desktop.py   # Claude Desktop MCP integration
│   ├── setup_vscode_mcp.py       # VS Code MCP integration  
│   ├── setup_dev.sh           # Development environment setup
│   └── build_package.sh       # Package build script
└── tools/
    └── parse_email.py         # Email parsing utilities
```

## 🛠 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed with Llama3 model
- Gmail API credentials
- Google account with Gmail access

## ⚡ Quick Start

### 1. Setup Environment
```bash
make setup          # Create virtual environment and install dependencies
make verify-setup   # Verify everything is ready for Gmail setup
```

### 2. Gmail API Setup (First Time)
```bash
# Get guided help for Google Cloud Console setup
make fix-gmail-auth

# After downloading credentials.json from Google Cloud Console:
make auth-setup     # Complete OAuth authentication
make test-gmail     # Verify Gmail connection works
```

**Gmail Setup Steps:**
1. **Google Cloud Console**: Create project → Enable Gmail API → Configure OAuth
2. **Download credentials**: Save `credentials.json` to project root
3. **Authenticate**: Run `make auth-setup` (opens browser)
4. **Test**: Run `make test-gmail` to verify connection

📖 **Detailed Gmail setup guide**: See [GMAIL_SETUP.md](GMAIL_SETUP.md)

### 3. Start Using

#### Option A: FastMCP Server (Recommended)
```bash
# Start the FastMCP server for Claude Desktop/VS Code
make run-fastmcp

# Set up Claude Desktop integration
make setup-claude-desktop

# Set up VS Code integration (Continue/Cline extensions)  
make setup-vscode
```

#### Option B: Direct Command Line
```bash
# Process latest email and generate reply
make run

# Generate daily email summary
make summary

# Run enhanced Gmail reader demo
make demo
```

## 🤖 FastMCP Server Integration

### Claude Desktop Setup
```bash
make setup-claude-desktop    # Automatic Claude Desktop configuration
```

### VS Code Setup  
```bash
make setup-vscode           # Configure Continue/Cline extensions
```

**Available MCP Tools:**
- `read_latest_emails` - Fetch recent Gmail messages
- `search_emails` - Search emails with Gmail queries  
- `get_email_details` - Get full email content and metadata
- `summarize_emails_tool` - AI-powered email summarization
- `send_email_summary` - Send summary emails
- `test_gmail_connection_tool` - Test Gmail API connectivity

## 🔧 Development Setup

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Using Make Commands
```bash
# Setup and Configuration
make setup           # Setup development environment
make verify-setup    # Verify Gmail setup readiness
make status         # Show current project status

# Gmail Authentication
make fix-gmail-auth  # Get help with Gmail API setup
make auth-setup     # Complete Gmail OAuth authentication
make test-gmail     # Test Gmail API connection

# Running the Application
make run            # Process latest email with AI
make demo           # Run enhanced Gmail reader demo
make summary        # Generate daily email summary

# FastMCP Server Commands
make run-fastmcp    # Start FastMCP server for Claude/VS Code
make setup-claude-desktop  # Configure Claude Desktop integration
make setup-vscode   # Configure VS Code integration
make test-fastmcp   # Test FastMCP server functionality

# Development and Testing
make test           # Run automated tests (80+ tests)
make test-emails    # Run Gmail email reading tests
make test-privacy   # Run privacy and security tests
make test-privacy-enhanced # Run comprehensive privacy analysis
make integration-test # Run full integration test with Gmail
make clean          # Clean cache and temporary files
make help           # Show all available commands
```

### Manual Setup (Alternative)
If you prefer manual setup:
- **Quick setup**: See [docs/GMAIL_SETUP.md](docs/GMAIL_SETUP.md) for essential steps
- **Command reference**: See [docs/WORKFLOW_CHEATSHEET.md](docs/WORKFLOW_CHEATSHEET.md) for all commands
- **Detailed guide**: This README contains the complete documentation

## 📁 Project Structure
```
fastmcp_gmail/
├── core/                   # Core modules
│   ├── email_summarizer.py # Email summarization logic
│   ├── gmail_client.py     # Gmail API client
│   ├── gmail_reader.py     # Gmail reading functionality
│   ├── llm_cache.py        # LLM caching system
│   ├── llm_log.py          # LLM logging utilities
│   ├── mcp_agent.py        # MCP agent implementation
│   └── ollama_llm.py       # Ollama LLM integration
├── tests/
│   ├── manual/             # Manual test scripts
│   │   └── test_real_setup.py
│   ├── test_recent_emails.py # Gmail email reading tests
│   ├── test_llm_privacy.py    # Privacy validation tests
│   ├── test_privacy_enhanced.py # Enhanced privacy analysis
│   └── test_gmail_reader.py # Automated tests (80+ total)
├── scripts/                # Utility scripts
│   ├── build_package.sh    # Package building
│   ├── setup_dev.sh        # Development setup
│   ├── setup_claude_desktop.py # Claude Desktop MCP setup
│   ├── setup_vscode_mcp.py     # VS Code MCP setup
│   └── fix_gmail_verification.py # Gmail auth troubleshooting
├── tools/
│   └── parse_email.py      # Email parsing utilities
├── main.py                 # Main application entry
├── mcp_server.py          # FastMCP server with 6 Gmail tools
├── send_email_summary.py   # Email summary sender
├── Makefile               # Development automation (30+ commands)
├── docs/                   # Documentation
│   ├── GMAIL_SETUP.md      # Quick Gmail setup reference
│   └── WORKFLOW_CHEATSHEET.md # Command quick reference
├── requirements.txt       # Python dependencies
├── .env.template          # Environment template
└── .gitignore            # Git ignore rules
```

## 📋 Usage

### FastMCP Server (Primary Method)
Start the FastMCP server and connect via Claude Desktop or VS Code:

```bash
# Start the server
make run-fastmcp

# In Claude Desktop: "What are my latest emails?"
# In VS Code: Use Continue extension with "List my recent Gmail messages"
```

### Direct Command Line
Process latest email and generate AI-powered professional reply:

```bash
python main.py
```

**Example Output:**
```
📧 Email from john@example.com, subject: Project Update

🤖 [Streaming response]: Thank you for the project update. I appreciate the detailed progress report and will review the attached documents. Let me know if you need any feedback or have questions about the next steps.
```

### Generate Email Summary
Creates a comprehensive AI summary of unread emails and sends it to yourself:

```bash
python send_email_summary.py
# Or via MCP: make run-fastmcp then ask "Summarize my unread emails"
```

## ⚙️ Configuration

### Gmail API Setup
1. The application requires `credentials.json` (OAuth client secrets)
2. On first run, it will open a browser for Gmail authorization
3. Authorization token is saved as `token.json` for future use

### LLM Configuration
- Default model: `llama3` via Ollama
- Confidence threshold: 85% (configurable in `mcp_agent.py`)
- Responses below threshold are marked as `[Low confidence]`

### Caching
- LLM responses cached in `cache/llm_cache.json`
- Email summaries cached in `cache/email_summary_cache.json`
- Conversation logs saved in `logs/llm_log.md`
- FastMCP server logs saved in `logs/fastmcp_server.log`

## 🔒 Privacy & Security

- **Local Processing**: All AI inference happens locally via Ollama
- **No External AI APIs**: No data sent to external LLM services (except optional Claude Desktop)
- **Minimal Permissions**: Only requires Gmail modify scope
- **Transparent Logging**: All interactions logged for review
- **Privacy Testing**: 12 comprehensive privacy validation tests
- **Sensitive Data Protection**: Automatic detection and redaction of SSNs, credit cards, passwords
- **Ephemeral Processing**: No persistent data storage beyond caching

## 📊 Architecture

### FastMCP Server
Built with the FastMCP framework providing:
- **6 Specialized Tools**: Gmail reading, searching, summarization, and connection testing
- **Multi-Platform Support**: Claude Desktop, VS Code (Continue/Cline), direct MCP clients
- **Robust Error Handling**: Comprehensive logging and graceful degradation
- **Streaming Responses**: Real-time AI response streaming

### MCP Agent Pattern
The project follows the Model Context Protocol pattern:
- **Agent**: Central coordinator (`MCPAgent`)
- **Tools**: Specialized components (Gmail client, LLM, cache)
- **Context**: Maintains conversation state and confidence scoring

### Confidence-Based Processing
```python
if confidence >= 0.85:
    return result["text"]
else:
    return f"[Low confidence] {result['text']}"
```

## 🧪 Testing

**80+ Comprehensive Tests:**
```bash
make test                    # Run all automated tests
make test-emails            # Gmail email reading functionality
make test-privacy           # Privacy and security validation
make test-privacy-enhanced  # Advanced privacy analysis
make test-all              # Complete test suite
```

**Test Coverage:**
- Gmail API integration and error handling
- Email data structure validation
- Privacy and sensitive data protection
- MCP server functionality
- Local LLM processing verification

## 📦 Building Release

```bash
make release
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test: `make test`
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

## 📝 License

This project is open source. See LICENSE file for details.

## 🔧 Troubleshooting

### Common Issues

**Gmail API Authentication:**
```bash
# Remove existing token and re-authenticate
rm token.json
python main.py
```

**Ollama Connection:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service if needed
ollama serve
```

**Missing Dependencies:**
```bash
make setup
```

**FastMCP Server Issues:**
```bash
# Check server status
make test-fastmcp

# View server logs
tail -f logs/fastmcp_server.log

# Restart Claude Desktop integration
make setup-claude-desktop
```

## 🛣 Roadmap

- [x] **FastMCP Server Implementation** - Complete MCP server with 6 Gmail tools
- [x] **Claude Desktop Integration** - Automated setup and configuration
- [x] **VS Code Integration** - Continue/Cline extension support
- [x] **Privacy Testing Framework** - Comprehensive privacy validation (12 tests)
- [x] **Email Reading Tests** - Full Gmail functionality testing (7 tests)
- [ ] Add email filtering and rules
- [ ] Support for multiple LLM backends
- [ ] Web interface for email management
- [ ] Email templates and customization
- [ ] Advanced summarization options
- [ ] Integration with calendar and tasks
- [ ] Batch email processing
- [ ] Email analytics and insights

---

## 🤖 AI Development Guidelines

This project is AI-assisted. Use these rules when working with GitHub Copilot, Claude 4.0, or any LLM agent in development:

### 🧠 Local LLM First
- Use a lightweight local LLM (e.g., Ollama) for first-pass email parsing and command handling.
- Escalate to Claude 4.0 or Copilot if model confidence < `85%`.

### 🧩 Project Framework
- Based on [FastMCP](https://github.com/modelcontext/fastmcp).
- Written in Python 3.12.
- Tools: `Paramiko`, `Telnetlib`, `LangChain`, `pexpect`, and `dotenv`.
- AI agent logic supports MCP tool routing with slot-based context and vector DB embeddings.

### 🪛 Coding with AI (Copilot / Claude)
- Apply Test-Driven Development (TDD):
  1. Write failing tests.
  2. Let AI generate code.
  3. Review, commit.
- Python dependencies defined in `requirements.txt`.
- All credentials must be stored in `.env.local` or local environment variables.

### 🚀 Feature Development & Bug Fix Workflow
When adding features or fixing bugs with AI assistance:

1. **Create Branch**: Create feature/bug branch from main
   ```bash
   git checkout -b feature/email-templates
   # or
   git checkout -b bugfix/cache-corruption
   ```

2. **Create Development Plan**: Document in `build/temp/plan.md`
   - **Objective**: Clear description of feature/fix
   - **Requirements**: Functional and technical requirements
   - **Implementation steps**: Break down into manageable tasks
   - **Test strategy**: Unit tests, integration tests, edge cases
   - **Acceptance criteria**: Definition of done

3. **Write Test Cases First** (TDD Approach):
   ```bash
   # Create test file in build/temp/ for experimentation
   touch build/temp/test_feature.py
   
   # Write failing tests that define expected behavior
   # Move finalized tests to tests/ directory
   ```

4. **Implement with AI**: Use AI to generate code based on failing tests
   - Store experimental code in `build/temp/`
   - Iterate with AI until tests pass
   - Move working code to appropriate source files

5. **Test & Refine**: Continuous testing and improvement
   ```bash
   make test                    # Run all tests
   make lint                    # Check code quality
   
   # Fix any issues with AI assistance
   # Update tests as needed
   ```

6. **Complete & Merge**: Finalize implementation
   ```bash
   git add .
   git commit -m "feat: add email templates feature"
   git push origin feature/email-templates
   # Create pull request
   ```

**Example Development Plan Template**:
```markdown
# Feature: Email Templates

## Objective
Add customizable email response templates for common scenarios.

## Requirements
- Store templates in JSON format
- Template variables support ({{name}}, {{date}})
- CLI command to list/select templates
- Integration with existing MCP agent

## Implementation Steps
1. Create template storage system
2. Add template variable parsing
3. Integrate with MCP agent workflow
4. Add CLI commands for template management

## Test Strategy
- Unit tests for template parsing
- Integration tests with MCP agent
- Edge cases: malformed templates, missing variables

## Acceptance Criteria
- [ ] Templates stored and loaded correctly
- [ ] Variables replaced properly
- [ ] CLI commands work as expected
- [ ] All tests pass
- [ ] Documentation updated
```

### 🛠 Packaging and Build Scripts
- Run `scripts/setup_dev.sh` to set up the local dev environment.
- Run `scripts/build_package.sh` to create a `.dmg` or `.tar.gz` package.
- Zips include all scripts, code, and config files.

### 🧪 Testing and Logs
- All generated code must be paired with a test case.
- Tool output should support Markdown and Mermaid.js diagrams.
- Internal logic should support CLI, Markdown, and HTML exports.

### 🗂 Build Directory Management
- **Use `build/` for all temporary artifacts**: Generated code, test outputs, logs, experiments.
- **Keep repository clean**: Only essential source code, scripts, documentation in git.
- **AI-generated files**: Store temporary test code, prototypes, and experiments in `build/temp/`.
- **Build artifacts**: Package outputs, compiled assets go in `build/dist/`.
- **Development logs**: Debug logs, AI conversation logs in `build/logs/`.
- **Structure example**:
  ```
  build/
  ├── temp/          # Temporary AI-generated code and experiments
  ├── dist/          # Package artifacts (.dmg, .tar.gz)
  ├── logs/          # Development and AI interaction logs
  ├── tests/         # Generated test outputs and reports
  └── docs/          # Generated documentation artifacts
  ```

### 🔐 Security
- Never hardcode API keys or passwords.
- Do not expose secrets in logs or prompt text.
- Keep `.env.local` in `.gitignore`.

---

**Built with ❤️ using local AI for privacy-focused email automation**