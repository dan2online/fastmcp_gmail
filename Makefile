# FastMCP Gmail - Project Makefile
# AI-Powered Email Assistant with Local LLM Processing

.PHONY: help setup clean test run summary install-ollama check-deps lint format release dev-install setup-build demo

# Default target
help:
	@echo "🚀 FastMCP Gmail - AI Email Assistant"
	@echo ""
	@echo "🎯 **NEW USER? START HERE:**"
	@echo "  quick-setup    - Complete setup workflow guide"
	@echo "  setup          - Initial environment setup"
	@echo "  verify-setup   - Check if ready for Gmail"
	@echo ""
	@echo "🔧 Development Commands:"
	@echo "  run            - Process latest email and generate reply"
	@echo "  test           - Run tests with HTML report"
	@echo "  test-structure - Run directory structure tests"
	@echo "  test-integration - Run Gmail reader integration tests"
	@echo "  test-email-summary - Run email summary tool tests"
	@echo "  test-privacy       - Run privacy and LLM sanity tests"
	@echo "  test-privacy-enhanced - Run advanced privacy analysis"
	@echo "  test-all       - Run all test suites"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code with black"
	@echo "  clean          - Clean cache and temporary files"
	@echo "  clean-all      - Clean everything including MCP configurations"
	@echo ""
	@echo "📧 Gmail Testing Commands:"
	@echo "  fix-gmail-auth - Fix Gmail verification issues"
	@echo "  auth-setup     - Set up Gmail authentication"
	@echo "  test-gmail     - Test Gmail API connection"
	@echo "  integration-test - Run full integration test"
	@echo "  test-email-summary-manual - Manual test with real Gmail"
	@echo ""
	@echo "🤖 AI Development Commands:"
	@echo "  ai-test        - Run AI feature tests (TDD)"
	@echo "  demo           - Run Gmail MCP operations demo"
	@echo "  summary        - Generate daily email summary"
	@echo ""
	@echo "🏗️ Build Commands:"
	@echo "  build          - Build distribution package"
	@echo "  release        - Prepare release package"
	@echo "  status         - Show project status"
	@echo ""
	@echo "🛠️ System Commands:"
	@echo "  check-deps     - Check system dependencies"
	@echo "  setup-user-config - Set up centralized user configuration"
	@echo "  setup-claude-desktop - Set up MCP server for Claude Desktop"
	@echo "  setup-vscode   - Set up MCP server for VS Code"
	@echo "  fix-claude     - Fix Claude Desktop configuration and test"
	@echo "  dev-setup      - Complete VS Code development environment setup"
	@echo "  install-ollama - Install Ollama and Llama3 model"
	@echo "  dev-install    - Install development dependencies"
	@echo ""
	@echo "🚀 FastMCP Development:"
	@echo "  run-fastmcp    - Start FastMCP Gmail server"
	@echo "  test-fastmcp   - Test FastMCP server tools"
	@echo ""
	@echo "📖 Documentation:"
	@echo "  cat docs/WORKFLOW_CHEATSHEET.md - Quick setup reference"
	@echo "  cat docs/GMAIL_SETUP.md         - Gmail API setup guide"
	@echo "  cat README.md              - Project overview"
	@echo ""
	@echo "🎯 Workflows:"
	@echo "  quick-setup    - Show quick Gmail setup workflow"
	@echo "  dev-workflow   - Show VS Code development workflow"
	@echo ""

# Setup development environment
setup: check-deps setup-build
	@echo "🔧 Setting up development environment..."
	python3 -m venv .venv
	@echo "📦 Installing Python dependencies..."
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "📋 Next steps:"
	@echo "  1. Activate virtual environment: source .venv/bin/activate"
	@echo "  2. Setup Gmail API credentials (see README.md)"
	@echo "  3. Install Ollama: make install-ollama"
	@echo "  4. Run the application: make run"

# Check system dependencies
check-deps:
	@echo "🔍 Checking system dependencies..."
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found. Please install Python 3.8+"; exit 1; }
	@python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" || { echo "❌ Python 3.8+ required"; exit 1; }
	@echo "✅ Python 3.8+ found"

# Install Ollama and Llama3 model
install-ollama:
	@echo "🤖 Installing Ollama and Llama3..."
	@if command -v brew >/dev/null 2>&1; then \
		echo "📦 Installing Ollama via Homebrew..."; \
		brew install ollama; \
	else \
		echo "⚠️  Homebrew not found. Please install Ollama manually:"; \
		echo "    Visit: https://ollama.ai/"; \
		exit 1; \
	fi
	@echo "📥 Pulling Llama3 model..."
	ollama pull llama3
	@echo "✅ Ollama and Llama3 ready!"

# Run main application
run:
	@echo "📧 Processing latest email..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ ! -f credentials.json ]; then echo "⚠️  Gmail credentials not found. Please add credentials.json"; exit 1; fi
	.venv/bin/python main.py

# Run enhanced Gmail demo
demo:
	@echo "🚀 Running Gmail MCP demo..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ ! -f credentials.json ] && [ ! -f ~/.local/fastmcp_gmail/credentials.json ]; then \
		echo "⚠️  Gmail credentials not found."; \
		echo "   Run 'make setup-user-config' for centralized config"; \
		echo "   Or add credentials.json to project directory"; \
		exit 1; \
	fi
	.venv/bin/python scripts/demo_gmail_mcp.py

# Generate email summary
summary:
	@echo "📊 Generating email summary..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ ! -f credentials.json ]; then echo "⚠️  Gmail credentials not found. Please add credentials.json"; exit 1; fi
	.venv/bin/python send_email_summary.py

# Run tests
test: setup-build
	@echo "🧪 Running tests..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ -d tests ]; then \
		.venv/bin/python -m pytest tests/ -v --html=build/tests/report.html --self-contained-html; \
	else \
		echo "📝 No tests directory found. Creating basic test structure..."; \
		mkdir -p tests; \
		echo "import unittest\n\nclass TestBasic(unittest.TestCase):\n    def test_import(self):\n        from core.mcp_agent import MCPAgent\n        self.assertTrue(True)\n\nif __name__ == '__main__':\n    unittest.main()" > tests/test_basic.py; \
		.venv/bin/python -m pytest tests/ -v --html=build/tests/report.html --self-contained-html; \
	fi
	@echo "📊 Test report generated: build/tests/report.html"

# Run directory structure tests
test-structure:
	@echo "🏗️ Running directory structure tests..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@mkdir -p build/tests
	.venv/bin/python -m pytest tests/test_directory_structure.py -v --html=build/tests/structure_report.html --self-contained-html
	@echo "📊 Structure test report: build/tests/structure_report.html"

# Run Gmail reader integration tests  
test-integration:
	@echo "🔗 Running Gmail reader integration tests..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@mkdir -p build/tests
	.venv/bin/python -m pytest tests/test_gmail_reader_integration.py -v --html=build/tests/integration_report.html --self-contained-html
	@echo "📊 Integration test report: build/tests/integration_report.html"

# Run email summary tool tests
test-email-summary:
	@echo "📧 Running email summary tool tests..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@mkdir -p build/tests
	.venv/bin/python -m pytest tests/test_email_summary_tool.py -v --html=build/tests/email_summary_report.html --self-contained-html
	@echo "📊 Email summary test report: build/tests/email_summary_report.html"

# Manual test for email summary tool with real Gmail
test-email-summary-manual:
	@echo "🧪 Running manual email summary test with real Gmail..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ ! -f credentials.json ] && [ ! -f ~/.local/fastmcp_gmail/credentials.json ]; then \
		echo "⚠️  Gmail credentials not found. Please add credentials.json or run 'make setup-user-config'"; \
		exit 1; \
	fi
	.venv/bin/python tests/manual/test_email_summary_manual.py

# Run all tests including new email summary tests
test-all: test test-structure test-integration test-email-summary test-privacy test-emails
	@echo "✅ All test suites completed!"

# Run privacy and LLM sanity tests
test-privacy:
	@echo "🔒 Running privacy and LLM sanity tests..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@mkdir -p build/tests
	.venv/bin/python tests/test_llm_privacy.py
	@echo "✅ Privacy tests completed"

# Run enhanced privacy analysis
test-privacy-enhanced:
	@echo "🛡️ Running enhanced privacy analysis..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@mkdir -p build/tests
	.venv/bin/python tests/test_privacy_enhanced.py
	@echo "🔒 Enhanced privacy analysis completed"

# Run Gmail email reading tests
test-emails:
	@echo "📧 Running Gmail email reading tests..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@mkdir -p build/tests
	.venv/bin/python -m pytest tests/test_recent_emails.py -v --html=build/tests/email_reading_report.html --self-contained-html
	@echo "📊 Email reading test report: build/tests/email_reading_report.html"

# Manual display of recent emails (not automated test)
show-emails:
	@echo "📧 Displaying recent Gmail emails..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ ! -f credentials.json ] && [ ! -f ~/.local/fastmcp_gmail/credentials.json ]; then \
		echo "⚠️  Gmail credentials not found. Please add credentials.json or run 'make setup-user-config'"; \
		exit 1; \
	fi
	.venv/bin/python tests/test_recent_emails.py

# Install development dependencies
dev-install: setup
	@echo "🛠 Installing development dependencies..."
	.venv/bin/pip install black flake8 pytest pytest-html mypy
	@echo "✅ Development dependencies installed!"

# Code linting
lint:
	@echo "🔍 Running code linting..."
	@if [ ! -f .venv/bin/flake8 ]; then echo "Installing linting tools..."; make dev-install; fi
	.venv/bin/flake8 core/ main.py send_email_summary.py --max-line-length=100 --ignore=E501,W503
	@echo "✅ Linting complete!"

# Code formatting
format:
	@echo "🎨 Formatting code..."
	@if [ ! -f .venv/bin/black ]; then echo "Installing formatting tools..."; make dev-install; fi
	.venv/bin/black core/ main.py send_email_summary.py --line-length=100
	@echo "✅ Code formatted!"

# Clean cache and temporary files
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	rm -rf cache/
	rm -rf logs/
	rm -rf __pycache__/
	rm -rf core/__pycache__/
	rm -rf tools/__pycache__/
	rm -rf .pytest_cache/
	rm -rf *.pyc
	rm -rf build/dist/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache and temporary files cleaned!"

# Clean everything including MCP configurations
clean-all: clean
	@echo "🗑️ Cleaning MCP configurations..."
	@# Claude Desktop configuration cleanup
	@if [ -f ~/Library/Application\ Support/Claude/claude_desktop_config.json ]; then \
		echo "  🔍 Found Claude Desktop config, checking for FastMCP Gmail entries..."; \
		if grep -q "fastmcp.*gmail\|gmail.*fastmcp" ~/Library/Application\ Support/Claude/claude_desktop_config.json 2>/dev/null; then \
			echo "  ⚠️  Found FastMCP Gmail entries in Claude Desktop config"; \
			echo "  📝 Manual cleanup required: ~/Library/Application Support/Claude/claude_desktop_config.json"; \
			echo "     Remove the FastMCP Gmail server entry from mcpServers section"; \
		else \
			echo "  ✅ No FastMCP Gmail entries found in Claude Desktop config"; \
		fi; \
	else \
		echo "  ✅ No Claude Desktop config found"; \
	fi
	@# VS Code configuration cleanup
	@if [ -f ~/.continue/config.json ]; then \
		echo "  🔍 Found Continue config, checking for FastMCP Gmail entries..."; \
		if grep -q "fastmcp.*gmail\|gmail.*fastmcp" ~/.continue/config.json 2>/dev/null; then \
			echo "  ⚠️  Found FastMCP Gmail entries in Continue config"; \
			echo "  📝 Manual cleanup required: ~/.continue/config.json"; \
			echo "     Remove the FastMCP Gmail server entry from mcpServers section"; \
		else \
			echo "  ✅ No FastMCP Gmail entries found in Continue config"; \
		fi; \
	else \
		echo "  ✅ No Continue config found"; \
	fi
	@if [ -f .vscode/settings.json ]; then \
		echo "  🔍 Found VS Code settings, checking for FastMCP Gmail entries..."; \
		if grep -q "fastmcp.*gmail\|gmail.*fastmcp" .vscode/settings.json 2>/dev/null; then \
			echo "  ⚠️  Found FastMCP Gmail entries in VS Code settings"; \
			echo "  📝 Manual cleanup required: .vscode/settings.json"; \
			echo "     Remove the FastMCP Gmail server entries"; \
		else \
			echo "  ✅ No FastMCP Gmail entries found in VS Code settings"; \
		fi; \
	else \
		echo "  ✅ No VS Code settings found"; \
	fi
	@echo ""
	@echo "🧹 Complete cleanup finished!"
	@echo "💡 Note: MCP configuration entries require manual removal if found"

# Create build directory structure
setup-build:
	@echo "📁 Setting up build directory structure..."
	mkdir -p build/temp
	mkdir -p build/dist
	mkdir -p build/logs
	mkdir -p build/tests
	mkdir -p build/docs
	@echo "✅ Build directory structure created!"

# Prepare release package
release: clean lint test setup-build
release: clean lint test setup-build
	@echo "📦 Preparing release package..."
	@VERSION=$$(date +%Y.%m.%d); \
	echo "🏷️  Version: $$VERSION"; \
	mkdir -p build/dist/fastmcp_gmail-$$VERSION; \
	cp -r core/ build/dist/fastmcp_gmail-$$VERSION/; \
	cp -r tools/ build/dist/fastmcp_gmail-$$VERSION/; \
	cp -r scripts/ build/dist/fastmcp_gmail-$$VERSION/; \
	cp main.py send_email_summary.py requirements.txt README.md Makefile LICENSE build/dist/fastmcp_gmail-$$VERSION/; \
	cd build/dist && tar -czf fastmcp_gmail-$$VERSION.tar.gz fastmcp_gmail-$$VERSION/; \
	echo "✅ Release package created: build/dist/fastmcp_gmail-$$VERSION.tar.gz"

# Development workflow shortcuts
dev: setup dev-install
	@echo "🚀 Development environment ready!"
	@echo "💡 Quick commands:"
	@echo "   make run     - Test email processing"
	@echo "   make summary - Test email summary"
	@echo "   make test    - Run tests"
	@echo "   make lint    - Check code quality"

# Check Ollama status
check-ollama:
	@echo "🤖 Checking Ollama status..."
	@if command -v ollama >/dev/null 2>&1; then \
		echo "✅ Ollama found"; \
		if ollama list | grep -q llama3; then \
			echo "✅ Llama3 model available"; \
		else \
			echo "⚠️  Llama3 model not found. Run 'make install-ollama'"; \
		fi; \
	else \
		echo "❌ Ollama not found. Run 'make install-ollama'"; \
	fi

# Full setup for new users
bootstrap: setup install-ollama
	@echo "🎉 Bootstrap complete!"
	@echo ""
	@echo "📋 Final setup steps:"
	@echo "  1. Add your Gmail API credentials as 'credentials.json'"
	@echo "  2. Run 'make run' to test email processing"
	@echo "  3. Run 'make summary' to test email summarization"

# Show project status
status:
	@echo "📊 FastMCP Gmail Project Status"
	@echo "==============================="
	@echo ""
	@echo "🐍 Python Environment:"
	@if [ -f .venv/bin/python ]; then \
		echo "  ✅ Virtual environment: .venv/"; \
		echo "  📦 Python version: $$(.venv/bin/python --version)"; \
	else \
		echo "  ❌ Virtual environment not found"; \
	fi
	@echo ""
	@echo "🔑 Gmail API:"
	@if [ -f credentials.json ]; then \
		echo "  ✅ Credentials file found"; \
	else \
		echo "  ❌ credentials.json not found"; \
	fi
	@if [ -f token.json ]; then \
		echo "  ✅ Auth token exists"; \
	else \
		echo "  ⚠️  No auth token (will authenticate on first run)"; \
	fi
	@echo ""
	@make check-ollama
	@echo ""
	@echo "💾 Cache Files:"
	@if [ -f cache/llm_cache.json ]; then \
		echo "  ✅ LLM cache exists ($$(wc -l < cache/llm_cache.json) entries)"; \
	else \
		echo "  ⚠️  No LLM cache"; \
	fi
	@if [ -f cache/email_summary_cache.json ]; then \
		echo "  ✅ Email summary cache exists"; \
	else \
		echo "  ⚠️  No email summary cache"; \
	fi
	@if [ -d logs ]; then \
		echo "  ✅ Logs directory exists ($$(ls logs/ 2>/dev/null | wc -l) files)"; \
	else \
		echo "  ⚠️  No logs directory"; \
	fi

# Gmail Authentication Setup
auth-setup:
	@echo "🔐 Setting up Gmail authentication..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	@if [ ! -f credentials.json ]; then \
		echo "❌ credentials.json not found!"; \
		echo "📖 Please follow the setup guide:"; \
		echo "   cat docs/GMAIL_SETUP.md"; \
		echo ""; \
		echo "💡 Quick steps:"; \
		echo "   1. Go to Google Cloud Console"; \
		echo "   2. Create OAuth2 credentials"; \
		echo "   3. Download as credentials.json"; \
		echo "   4. Run 'make auth-setup' again"; \
		exit 1; \
	fi
	@echo "✅ credentials.json found"
	@echo "🚀 Starting OAuth flow..."
	.venv/bin/python -c "from core.gmail_client import test_gmail_connection; test_gmail_connection()"
	@echo "✅ Authentication complete!"
	@echo "💾 Token saved to token.json"
	@echo "🎉 Ready to use Gmail API!"

# Test Gmail Connection
test-gmail:
	@echo "🔗 Testing Gmail API connection..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	.venv/bin/python -c "from core.gmail_client import test_gmail_connection; success, msg = test_gmail_connection(); print(f'✅ {msg}' if success else f'❌ {msg}')"

# Integration Test with Real Gmail
integration-test: test-gmail
	@echo "🧪 Running integration tests with Gmail..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	.venv/bin/python -c "import sys; sys.path.append('scripts'); from demo_gmail_mcp import main; main()"

# Verify Real Setup Readiness
verify-setup:
	@echo "🔍 Verifying real Gmail setup readiness..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	.venv/bin/python tests/manual/test_real_setup.py

# Fix Gmail Verification Issues
fix-gmail-auth:
	@echo "🔧 Gmail API verification troubleshooting..."
	@if [ ! -f .venv/bin/python ]; then echo "❌ Virtual environment not found. Run 'make setup' first."; exit 1; fi
	.venv/bin/python scripts/fix_gmail_verification.py

# Quick Setup Workflow Guide
quick-setup:
	@echo "🚀 FastMCP Gmail - Quick Setup Workflow"
	@echo "======================================"
	@echo ""
	@echo "📋 Follow these steps to set up Gmail access:"
	@echo ""
	@echo "1️⃣  **Environment Setup** (if not done yet):"
	@echo "   make setup"

# VS Code Development Workflow
dev-workflow:
	@echo "🖥️  FastMCP Gmail - VS Code Development Workflow"
	@echo "==============================================="
	@echo ""
	@echo "🚀 **Quick Start for VS Code Development:**"
	@echo ""
	@echo "1️⃣  **Complete Development Setup:**"
	@echo "   make dev-setup     # Sets up everything for VS Code"
	@echo ""
	@echo "2️⃣  **Configure Gmail API:**"
	@echo "   make auth-setup    # Set up Gmail credentials"
	@echo "   make test-gmail    # Verify Gmail connection"
	@echo ""
	@echo "3️⃣  **Install VS Code Extensions:**"
	@echo "   - Continue (AI assistant with MCP support)"
	@echo "   - Cline (MCP-native coding assistant)"
	@echo "   - Python extension pack"
	@echo ""
	@echo "4️⃣  **Test FastMCP Server:**"
	@echo "   make run-fastmcp   # Start server in terminal"
	@echo "   make test-fastmcp  # Test server tools"
	@echo ""
	@echo "5️⃣  **Use in VS Code:**"
	@echo "   - Open Command Palette (Cmd+Shift+P)"
	@echo "   - Try 'Continue: New Chat' or 'Cline: Start'"
	@echo "   - Ask: 'What are my latest emails?'"
	@echo ""
	@echo "📚 **Documentation:**"
	@echo "   VS Code Setup: make setup-vscode-mcp"
	@echo "   Gmail Setup:   docs/GMAIL_SETUP.md"
	@echo "   Quick Start:   README.md"
	@echo ""
	@echo "2️⃣  **Verify Readiness**:"
	@echo "   make verify-setup"
	@echo ""
	@echo "3️⃣  **Google Cloud Console Setup** (manual):"
	@echo "   - Go to: https://console.cloud.google.com/"
	@echo "   - Create project → Enable Gmail API"
	@echo "   - Configure OAuth consent screen"
	@echo "   - Add yourself as test user (if External app)"
	@echo "   - Create OAuth credentials → Download credentials.json"
	@echo ""
	@echo "4️⃣  **Authentication**:"
	@echo "   make auth-setup"
	@echo ""
	@echo "5️⃣  **Test & Verify**:"
	@echo "   make test-gmail"
	@echo "   make demo"
	@echo ""
	@echo "📖 Detailed guides:"
	@echo "   cat docs/GMAIL_SETUP.md      # Complete setup guide"
	@echo "   cat docs/WORKFLOW_CHEATSHEET.md  # Quick reference"
	@echo ""
	@echo "🆘 Need help?"
	@echo "   make fix-gmail-auth     # Troubleshooting guide"

# Set up centralized user configuration
setup-user-config:
	@echo "🏠 Setting up centralized user configuration..."
	.venv/bin/python scripts/setup_user_config.py

# Set up MCP server for Claude Desktop
setup-claude-desktop:
	@echo "🖥️  Setting up FastMCP Gmail for Claude Desktop..."
	.venv/bin/python scripts/setup_claude_desktop.py

# Set up MCP server for VS Code
setup-vscode:
	@echo "🖥️  Setting up FastMCP Gmail for VS Code..."
	.venv/bin/python scripts/setup_vscode_mcp.py

# Complete development environment setup for VS Code
dev-setup: setup dev-install setup-vscode
	@echo ""
	@echo "🎉 Development Environment Ready!"
	@echo "================================"
	@echo "✅ Virtual environment created"
	@echo "✅ Dependencies installed"
	@echo "✅ Development tools installed"
	@echo "✅ VS Code MCP integration configured"
	@echo ""
	@echo "🚀 Next Steps:"
	@echo "1. Restart VS Code to load new MCP configuration"
	@echo "2. Install recommended VS Code extensions:"
	@echo "   - Continue (AI coding assistant with MCP support)"
	@echo "   - Cline (MCP-native coding assistant)"
	@echo "   - Python extension pack"
	@echo "3. Test Gmail connection: make test-gmail"
	@echo "4. Run FastMCP server: make run-fastmcp"
	@echo ""
	@echo "📚 Documentation:"
	@echo "   VS Code Setup: make setup-vscode-mcp"
	@echo "   Gmail Setup:   docs/GMAIL_SETUP.md"

# Run FastMCP server for development/testing
run-fastmcp:
	@echo "🚀 Starting FastMCP Gmail server..."
	@echo "📋 Available tools: read_latest_emails, search_emails, get_email_details, summarize_emails_tool, test_gmail_connection_tool"
	@echo "🔗 Connect via: Continue, Cline, or manual MCP testing"
	@echo ""
	.venv/bin/python mcp_server.py

# Test FastMCP server tools
test-fastmcp:
	@echo "🧪 Testing FastMCP server tools..."
	@echo ""
	@echo "📝 Testing tool list..."
	@(echo '{"method":"tools/list","jsonrpc":"2.0","id":1}' | .venv/bin/python mcp_server.py) || echo "⚠️  Initialize with proper MCP client for full testing"
	@echo ""
	@echo "💡 For full testing, use VS Code with Continue/Cline extensions"
	@echo "   Or test with Claude Desktop after running: make setup-claude-desktop"

# Fix Claude Desktop configuration and test
fix-claude: setup-claude-desktop
	@echo ""
	@echo "🔧 Testing MCP server startup..."
	@timeout 3 .venv/bin/python mcp_server.py > /dev/null 2>&1 && echo "✅ MCP server starts correctly" || echo "⚠️  Server startup issue - check logs"
	@echo ""
	@echo "🔍 Checking Claude Desktop config..."
	@if [ -f "$$HOME/Library/Application Support/Claude/claude_desktop_config.json" ]; then \
		echo "✅ Claude Desktop config file exists"; \
		if grep -q "fastmcp-gmail" "$$HOME/Library/Application Support/Claude/claude_desktop_config.json" 2>/dev/null; then \
			echo "✅ FastMCP Gmail server configured in Claude Desktop"; \
		else \
			echo "❌ FastMCP Gmail server not found in Claude config"; \
		fi \
	else \
		echo "❌ Claude Desktop config file not found"; \
	fi
	@echo ""
	@echo "🎯 Next Steps:"
	@echo "   1. Restart Claude Desktop application"
	@echo "   2. Look for Gmail tools in Claude's interface"
	@echo "   3. Test with: 'What are my latest emails?'"
	@echo ""
	@echo "🆘 If issues persist:"
	@echo "   - Check server logs: tail -f logs/fastmcp_server.log"
	@echo "   - Run: make test-fastmcp"
	@echo "   - Verify Gmail: make test-gmail"
