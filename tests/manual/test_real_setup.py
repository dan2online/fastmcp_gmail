#!/usr/bin/env python3
"""
Test script to verify real Gmail setup readiness
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        logger.info(f"✅ {description}: {filepath}")
        return True
    else:
        logger.warning(f"❌ {description} missing: {filepath}")
        return False


def check_environment_variables():
    """Check if required environment variables are set"""
    env_vars = {
        "GMAIL_CREDENTIALS_FILE": "Gmail credentials file path",
        "GMAIL_TOKEN_FILE": "Gmail token file path",
        "GMAIL_SCOPES": "Gmail API scopes",
        "OLLAMA_MODEL": "Ollama model name",
        "OLLAMA_HOST": "Ollama host URL",
    }

    logger.info("🔍 Checking environment variables...")
    missing_vars = []

    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: {value}")
        else:
            logger.info(f"⚠️  {var}: Using default (can be set in .env.local)")

    return True


def check_dependencies():
    """Check if all required dependencies are available"""
    logger.info("📦 Checking Python dependencies...")

    required_modules = [
        "google.auth",
        "google.oauth2.credentials",
        "google_auth_oauthlib.flow",
        "googleapiclient.discovery",
        "requests",
        "pytest",
    ]

    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✅ {module}")
        except ImportError:
            logger.error(f"❌ {module}")
            missing_modules.append(module)

    if missing_modules:
        logger.error(f"Missing modules: {missing_modules}")
        logger.error("Run 'make setup' to install dependencies")
        return False

    return True


def test_core_imports():
    """Test that core modules can be imported"""
    logger.info("🧪 Testing core module imports...")

    try:
        from core.gmail_client import load_env_config, get_gmail_service

        logger.info("✅ gmail_client module")

        from core.gmail_reader import GmailReader

        logger.info("✅ gmail_reader module")

        from core.email_summarizer import summarize_emails

        logger.info("✅ email_summarizer module")

        from core.ollama_llm import ollama_llm_streaming

        logger.info("✅ ollama_llm module")

        from core.mcp_agent import MCPAgent

        logger.info("✅ mcp_agent module")

        return True

    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        return False


def test_configuration_loading():
    """Test configuration loading"""
    logger.info("⚙️  Testing configuration loading...")

    try:
        from core.gmail_client import load_env_config

        config = load_env_config()

        logger.info(f"✅ Credentials file: {config['credentials_file']}")
        logger.info(f"✅ Token file: {config['token_file']}")
        logger.info(f"✅ Scopes: {config['scopes']}")

        return True

    except Exception as e:
        logger.error(f"❌ Configuration loading failed: {e}")
        return False


def main():
    """Run all setup checks"""
    logger.info("🚀 FastMCP Gmail - Real Setup Verification")
    logger.info("=" * 50)

    checks = [
        (
            "File Structure",
            lambda: (
                check_file_exists("core/gmail_client.py", "Gmail client")
                and check_file_exists("core/gmail_reader.py", "Gmail reader")
                and check_file_exists("docs/GMAIL_SETUP.md", "Setup guide")
                and check_file_exists(".env.template", "Environment template")
            ),
        ),
        ("Environment Variables", check_environment_variables),
        ("Python Dependencies", check_dependencies),
        ("Core Module Imports", test_core_imports),
        ("Configuration Loading", test_configuration_loading),
    ]

    results = []
    for check_name, check_func in checks:
        logger.info(f"\n📋 {check_name}:")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            logger.error(f"❌ {check_name} failed: {e}")
            results.append((check_name, False))

    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 SUMMARY:")

    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"  {status}: {check_name}")
        if not passed:
            all_passed = False

    logger.info("\n🎯 NEXT STEPS:")
    if all_passed:
        logger.info("✅ All checks passed! Ready for real Gmail testing.")
        logger.info("📖 Follow docs/GMAIL_SETUP.md for Google Cloud Console setup")
        logger.info("🔑 Run 'make auth-setup' to authenticate with Gmail")
        logger.info("🧪 Run 'make test-gmail' to test connection")
    else:
        logger.info("❌ Some checks failed. Please fix the issues above.")
        logger.info("💡 Run 'make setup' to install dependencies")
        logger.info("📖 Check docs/GMAIL_SETUP.md for setup instructions")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
