# FastMCP Gmail - Project Makefile
# AI-Powered Email Assistant with Local LLM Processing

.PHONY: help setup clean test run summary install-ollama check-deps lint format release dev-install setup-build

# Default target
help:
	@echo "🚀 FastMCP Gmail - AI Email Assistant"
	@echo ""
	@echo "Available commands:"
	@echo "  setup          - Setup development environment"
	@echo "  setup-build    - Create build directory structure"
	@echo "  run            - Process latest email and generate reply"
	@echo "  summary        - Generate daily email summary"
	@echo "  test           - Run tests"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code with black"
	@echo "  check-deps     - Check system dependencies"
	@echo "  install-ollama - Install Ollama and Llama3 model"
	@echo "  clean          - Clean cache and temporary files"
	@echo "  release        - Prepare release package"
	@echo "  dev-install    - Install development dependencies"
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
	rm -f llm_cache.json
	rm -f email_summary_cache.json
	rm -f llm_log.md
	rm -rf __pycache__/
	rm -rf core/__pycache__/
	rm -rf tools/__pycache__/
	rm -rf .pytest_cache/
	rm -rf *.pyc
	rm -rf build/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

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
	@if [ -f llm_cache.json ]; then \
		echo "  ✅ LLM cache exists ($$(wc -l < llm_cache.json) entries)"; \
	else \
		echo "  ⚠️  No LLM cache"; \
	fi
	@if [ -f email_summary_cache.json ]; then \
		echo "  ✅ Email summary cache exists"; \
	else \
		echo "  ⚠️  No email summary cache"; \
	fi
