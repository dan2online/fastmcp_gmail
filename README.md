# FastMCP Gmail - AI-Powered Email Assistant

A privacy-focused Gmail AI assistant that uses local LLM processing via Ollama to generate intelligent email responses and summaries. Built following the Model Context Protocol (MCP) pattern for reliable AI interactions.

## 🚀 Features

- **Smart Email Processing**: Fetches and processes Gmail messages using Google API
- **Local AI Processing**: Uses Ollama with Llama3 for privacy-focused local inference
- **Intelligent Caching**: JSON-based response caching to avoid redundant API calls
- **Confidence Scoring**: Only accepts high-confidence AI responses (≥85%)
- **Email Summarization**: Generates daily email summaries for unread messages
- **Professional Replies**: Automatically generates professional email responses
- **Conversation Logging**: Markdown-based logging of all AI interactions
- **Streaming Responses**: Real-time AI response streaming

## 📁 Project Structure

```
fastmcp_gmail/
├── main.py                     # Main email processing script
├── send_email_summary.py       # Daily email summary generator
├── requirements.txt            # Python dependencies
├── Makefile                    # Project automation
├── core/
│   ├── mcp_agent.py           # Core MCP agent with confidence handling
│   ├── gmail_client.py        # Gmail API integration
│   ├── ollama_llm.py          # Ollama LLM integration
│   ├── llm_cache.py           # Response caching system
│   ├── llm_log.py             # Conversation logging
│   └── email_summarizer.py    # Email summarization logic
├── scripts/
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
make setup
```

### 2. Configure Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Download and save as `credentials.json` in project root

### 3. Install Ollama and Llama3
```bash
# Install Ollama (macOS)
brew install ollama

# Pull Llama3 model
ollama pull llama3
```

### 4. Run the Application
```bash
# Process latest email and generate reply
make run

# Generate daily email summary
make summary
```

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
make setup      # Setup development environment
make test       # Run tests (when available)
make clean      # Clean cache and temporary files
make release    # Prepare release package
```

## 📋 Usage

### Process Latest Email
The main script fetches your latest Gmail message and generates an AI-powered professional reply:

```bash
python main.py
```

**Example Output:**
```
📧 Email from john@example.com, subject: Project Update

🤖 [Streaming response]: Thank you for the project update. I appreciate the detailed progress report and will review the attached documents. Let me know if you need any feedback or have questions about the next steps.
```

### Generate Email Summary
Creates a comprehensive summary of unread emails and sends it to yourself:

```bash
python send_email_summary.py
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
- LLM responses cached in `llm_cache.json`
- Email summaries cached in `email_summary_cache.json`
- Conversation logs saved in `llm_log.md`

## 🔒 Privacy & Security

- **Local Processing**: All AI inference happens locally via Ollama
- **No External AI APIs**: No data sent to external LLM services
- **Minimal Permissions**: Only requires Gmail modify scope
- **Transparent Logging**: All interactions logged for review

## 📊 Architecture

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

```bash
make test
```

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

## 🛣 Roadmap

- [ ] Add email filtering and rules
- [ ] Support for multiple LLM backends
- [ ] Web interface for email management
- [ ] Email templates and customization
- [ ] Advanced summarization options
- [ ] Integration with calendar and tasks

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