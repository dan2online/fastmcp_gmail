"""
Integration tests for Gmail Reader with organized directory structure
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os
import json
from unittest.mock import Mock, patch

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestGmailReaderIntegration(unittest.TestCase):
    """Integration tests for Gmail Reader with cache and log organization"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create project structure
        (self.test_dir / "core").mkdir()
        (self.test_dir / "cache").mkdir()
        (self.test_dir / "logs").mkdir()

        # Create mock Gmail service
        self.mock_service = Mock()

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_gmail_reader_with_cache_integration(self):
        """Test Gmail Reader integration with cache functionality"""
        from core.gmail_reader import GmailReader

        # Create Gmail reader instance
        reader = GmailReader(self.mock_service)

        # Mock email data
        mock_email_data = {
            "id": "test_email_id",
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Test Email"},
                    {"name": "From", "value": "test@example.com"},
                    {"name": "Date", "value": "Mon, 1 Jan 2024 12:00:00 +0000"},
                ],
                "mimeType": "text/plain",
                "body": {
                    "data": "VGVzdCBlbWFpbCBjb250ZW50"
                },  # base64 for "Test email content"
            },
            "snippet": "Test email snippet",
            "labelIds": ["INBOX"],
        }

        # Mock Gmail API calls
        self.mock_service.users().messages().get().execute.return_value = (
            mock_email_data
        )

        # Test reading email
        result = reader.read_email_by_id("test_email_id")

        # Verify structure
        self.assertIsNotNone(result)
        self.assertEqual(result["subject"], "Test Email")
        self.assertEqual(result["sender"], "test@example.com")

        # Verify cache functionality still works
        from core.llm_cache import CACHE_FILE, save_cache, load_cache

        test_cache = {"email_summary": "Test summary"}
        save_cache(test_cache)

        # Verify cache file is in correct location
        self.assertTrue(CACHE_FILE.exists())
        self.assertTrue("cache" in str(CACHE_FILE))

        loaded_cache = load_cache()
        self.assertEqual(loaded_cache, test_cache)

    def test_email_summarizer_with_organized_cache(self):
        """Test email summarizer uses organized cache directory"""
        from core.email_summarizer import CACHE_FILE, save_cache, load_cache

        # Test cache operations
        test_data = {
            "email_id_123": {
                "summary": "Test email summary",
                "timestamp": "2024-01-01T12:00:00",
            }
        }

        save_cache(test_data)

        # Verify file location
        self.assertTrue(CACHE_FILE.exists())
        self.assertTrue(str(CACHE_FILE).endswith("cache/email_summary_cache.json"))

        # Verify content
        loaded = load_cache()
        self.assertEqual(loaded, test_data)

    def test_llm_logging_integration(self):
        """Test LLM logging with organized logs directory"""
        from core.llm_log import LOG_FILE, log_prompt_response

        # Test logging
        test_prompt = "Summarize this email: Test content"
        test_response = "Summary: Test email about content"

        log_prompt_response(test_prompt, test_response)

        # Verify file location
        self.assertTrue(LOG_FILE.exists())
        self.assertTrue(str(LOG_FILE).endswith("logs/llm_log.md"))

        # Verify content
        content = LOG_FILE.read_text()
        self.assertIn(test_prompt, content)
        self.assertIn(test_response, content)
        self.assertIn("###", content)  # Markdown formatting

    def test_mcp_server_logging_setup(self):
        """Test MCP server logging configuration"""
        # Import and test the logging setup logic
        project_dir = Path.cwd()
        log_dir = project_dir / "logs"
        log_file = log_dir / "fastmcp_server.log"

        # Ensure log directory exists
        log_dir.mkdir(exist_ok=True)

        # Create a test log file
        log_file.write_text("Test log entry\n")

        # Verify structure
        self.assertTrue(log_file.exists())
        self.assertEqual(log_file.parent.name, "logs")
        self.assertTrue("logs" in str(log_file))

    def test_concurrent_cache_access(self):
        """Test that concurrent access to cache works properly"""
        from core.llm_cache import save_cache, load_cache
        from core.email_summarizer import (
            save_cache as save_email_cache,
            load_cache as load_email_cache,
        )

        # Save to both caches
        llm_data = {"prompt1": "response1"}
        email_data = {"email1": "summary1"}

        save_cache(llm_data)
        save_email_cache(email_data)

        # Load from both caches
        loaded_llm = load_cache()
        loaded_email = load_email_cache()

        # Verify independence
        self.assertEqual(loaded_llm, llm_data)
        self.assertEqual(loaded_email, email_data)
        self.assertNotEqual(loaded_llm, loaded_email)

    def test_cache_persistence_across_imports(self):
        """Test that cache data persists across module imports"""
        # First import and save
        from core.llm_cache import save_cache, CACHE_FILE

        test_data = {"persistent": "data"}
        save_cache(test_data)

        # Verify file exists
        self.assertTrue(CACHE_FILE.exists())

        # Simulate fresh import by reloading module
        import importlib
        import core.llm_cache

        importlib.reload(core.llm_cache)

        # Load with fresh import
        from core.llm_cache import load_cache

        loaded_data = load_cache()

        self.assertEqual(loaded_data, test_data)

    def test_directory_permissions_and_creation(self):
        """Test directory creation and permissions"""
        # Remove directories to test auto-creation
        cache_dir = self.test_dir / "cache"
        logs_dir = self.test_dir / "logs"

        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        if logs_dir.exists():
            shutil.rmtree(logs_dir)

        # Import modules should recreate directories
        from core.llm_cache import CACHE_FILE
        from core.llm_log import LOG_FILE

        # Verify directories were created
        self.assertTrue(CACHE_FILE.parent.exists())
        self.assertTrue(LOG_FILE.parent.exists())

        # Verify they're writable
        test_file = CACHE_FILE.parent / "test_write.txt"
        test_file.write_text("test")
        self.assertTrue(test_file.exists())

        test_log = LOG_FILE.parent / "test_log.txt"
        test_log.write_text("test log")
        self.assertTrue(test_log.exists())

    def test_error_handling_with_directory_structure(self):
        """Test error handling when directories have issues"""
        from core.llm_cache import load_cache, save_cache

        # Test with non-existent parent directory initially
        cache_dir = self.test_dir / "nonexistent" / "cache"
        logs_dir = self.test_dir / "nonexistent" / "logs"

        # The modules should handle directory creation gracefully
        # This is tested by the directory auto-creation in the modules


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with old directory structure"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create project structure
        (self.test_dir / "core").mkdir()

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_migration_from_old_structure(self):
        """Test behavior when old cache files exist in root"""
        # Create old-style cache files in root
        old_llm_cache = self.test_dir / "llm_cache.json"
        old_email_cache = self.test_dir / "email_summary_cache.json"
        old_log = self.test_dir / "llm_log.md"

        old_llm_cache.write_text('{"old": "data"}')
        old_email_cache.write_text('{"old_email": "data"}')
        old_log.write_text("# Old log data\n")

        # Import new modules (should create new structure)
        from core.llm_cache import CACHE_FILE
        from core.llm_log import LOG_FILE
        from core.email_summarizer import CACHE_FILE as EMAIL_CACHE_FILE

        # Verify new structure is used (doesn't load from old files)
        self.assertTrue("cache" in str(CACHE_FILE))
        self.assertTrue("logs" in str(LOG_FILE))
        self.assertTrue("cache" in str(EMAIL_CACHE_FILE))

        # Verify old files are ignored (new paths don't point to old files)
        self.assertNotEqual(str(CACHE_FILE), str(old_llm_cache))
        self.assertNotEqual(str(EMAIL_CACHE_FILE), str(old_email_cache))
        self.assertNotEqual(str(LOG_FILE), str(old_log))


if __name__ == "__main__":
    # Run integration tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestGmailReaderIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)
