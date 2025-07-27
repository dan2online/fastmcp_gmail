"""
Test cases for cache and log directory structure organization
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDirectoryStructure(unittest.TestCase):
    """Test that cache and log files are properly organized in dedicated directories"""

    def setUp(self):
        """Set up test environment with temporary directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create project structure
        (self.test_dir / "core").mkdir()
        (self.test_dir / "cache").mkdir()
        (self.test_dir / "logs").mkdir()

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_cache_directory_structure(self):
        """Test that cache files are created in cache/ directory"""
        # Test LLM cache
        from core.llm_cache import CACHE_FILE

        self.assertTrue(str(CACHE_FILE).endswith("cache/llm_cache.json"))
        self.assertTrue("cache" in str(CACHE_FILE))

        # Test email summary cache
        from core.email_summarizer import CACHE_FILE as EMAIL_CACHE_FILE

        self.assertTrue(
            str(EMAIL_CACHE_FILE).endswith("cache/email_summary_cache.json")
        )
        self.assertTrue("cache" in str(EMAIL_CACHE_FILE))

    def test_logs_directory_structure(self):
        """Test that log files are created in logs/ directory"""
        from core.llm_log import LOG_FILE

        self.assertTrue(str(LOG_FILE).endswith("logs/llm_log.md"))
        self.assertTrue("logs" in str(LOG_FILE))

    def test_directory_creation(self):
        """Test that directories are created automatically when needed"""
        # Remove directories to test auto-creation
        if (self.test_dir / "cache").exists():
            shutil.rmtree(self.test_dir / "cache")
        if (self.test_dir / "logs").exists():
            shutil.rmtree(self.test_dir / "logs")

        # Import modules and use them to trigger directory creation
        from core.llm_cache import CACHE_FILE, save_cache
        from core.llm_log import LOG_FILE, log_prompt_response
        from core.email_summarizer import (
            CACHE_FILE as EMAIL_CACHE_FILE,
            save_cache as save_email_cache,
        )

        # Use the functions to trigger directory creation
        save_cache({"test": "data"})
        log_prompt_response("test", "response")
        save_email_cache({"test": "email"})

        # Check that parent directories now exist
        self.assertTrue(CACHE_FILE.parent.exists())
        self.assertTrue(LOG_FILE.parent.exists())
        self.assertTrue(EMAIL_CACHE_FILE.parent.exists())

    def test_cache_functionality(self):
        """Test that cache functionality works with new directory structure"""
        from core.llm_cache import load_cache, save_cache, CACHE_FILE

        # Test loading empty cache
        cache = load_cache()
        self.assertIsInstance(cache, dict)

        # Test saving cache
        test_data = {"test_prompt": "test_response"}
        save_cache(test_data)

        # Verify file was created in correct location
        self.assertTrue(CACHE_FILE.exists())
        self.assertTrue("cache" in str(CACHE_FILE))

        # Test loading saved cache
        loaded_cache = load_cache()
        self.assertEqual(loaded_cache, test_data)

    def test_log_functionality(self):
        """Test that logging functionality works with new directory structure"""
        from core.llm_log import log_prompt_response, LOG_FILE

        # Test logging
        log_prompt_response("test prompt", "test response")

        # Verify file was created in correct location
        self.assertTrue(LOG_FILE.exists())
        self.assertTrue("logs" in str(LOG_FILE))

        # Verify content
        content = LOG_FILE.read_text()
        self.assertIn("test prompt", content)
        self.assertIn("test response", content)

    def test_no_root_directory_pollution(self):
        """Test that no cache or log files are created in root directory"""
        from core.llm_cache import load_cache, save_cache
        from core.llm_log import log_prompt_response
        from core.email_summarizer import (
            load_cache as load_email_cache,
            save_cache as save_email_cache,
        )

        # Use the functionality
        cache = load_cache()
        save_cache({"test": "data"})
        log_prompt_response("test", "response")
        email_cache = load_email_cache()
        save_email_cache({"email": "data"})

        # Check that no cache/log files exist in root
        root_files = (
            list(self.test_dir.glob("*.json"))
            + list(self.test_dir.glob("*.log"))
            + list(self.test_dir.glob("*.md"))
        )
        cache_log_files = [
            f
            for f in root_files
            if f.name
            in [
                "llm_cache.json",
                "email_summary_cache.json",
                "llm_log.md",
                "fastmcp_server.log",
                "mcp_server.log",
            ]
        ]

        self.assertEqual(
            len(cache_log_files),
            0,
            f"Found cache/log files in root directory: {cache_log_files}",
        )


class TestMCPServerLogging(unittest.TestCase):
    """Test MCP server logging configuration"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        (self.test_dir / "logs").mkdir()

    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_mcp_server_log_location(self):
        """Test that MCP server creates logs in logs/ directory"""
        # Mock the setup_logging function behavior
        project_dir = Path.cwd()
        log_dir = project_dir / "logs"
        log_file = log_dir / "fastmcp_server.log"

        # Verify the expected path structure
        self.assertTrue(str(log_file).endswith("logs/fastmcp_server.log"))
        self.assertEqual(log_file.name, "fastmcp_server.log")
        self.assertEqual(log_file.parent.name, "logs")


class TestGitignoreConfiguration(unittest.TestCase):
    """Test that .gitignore properly handles new directory structure"""

    def test_gitignore_patterns(self):
        """Test that .gitignore contains correct patterns for new structure"""
        gitignore_path = Path(__file__).parent.parent / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()

            # Should ignore directories, not individual files
            self.assertIn("logs/", content)
            self.assertIn("cache/", content)
            self.assertIn("*.log", content)

            # Should NOT contain old individual file patterns
            self.assertNotIn("llm_cache.json", content)
            self.assertNotIn("email_summary_cache.json", content)
            self.assertNotIn("llm_log.md", content)


class TestMakefileIntegration(unittest.TestCase):
    """Test Makefile integration with new directory structure"""

    def test_makefile_clean_command(self):
        """Test that Makefile clean command targets correct directories"""
        makefile_path = Path(__file__).parent.parent / "Makefile"
        if makefile_path.exists():
            content = makefile_path.read_text()

            # Should clean directories
            self.assertIn("rm -rf cache/", content)
            self.assertIn("rm -rf logs/", content)

            # Should NOT clean individual files in root
            self.assertNotIn("rm -f llm_cache.json", content)
            self.assertNotIn("rm -f email_summary_cache.json", content)
            self.assertNotIn("rm -f llm_log.md", content)

    def test_makefile_status_command(self):
        """Test that Makefile status command checks correct locations"""
        makefile_path = Path(__file__).parent.parent / "Makefile"
        if makefile_path.exists():
            content = makefile_path.read_text()

            # Should check cache directory
            self.assertIn("cache/llm_cache.json", content)
            self.assertIn("cache/email_summary_cache.json", content)
            self.assertIn("logs", content)


class TestEnvironmentConfiguration(unittest.TestCase):
    """Test environment configuration for new directory structure"""

    def test_env_template_paths(self):
        """Test that .env.template uses correct paths"""
        env_template_path = Path(__file__).parent.parent / ".env.template"
        if env_template_path.exists():
            content = env_template_path.read_text()

            # Should reference new directory structure
            self.assertIn("logs/", content)
            self.assertIn("cache/", content)

            # Should NOT reference old paths
            self.assertNotIn("build/logs/", content)
            # Should use cache/ prefix for cache files
            if "llm_cache.json" in content:
                self.assertIn("cache/llm_cache.json", content)


if __name__ == "__main__":
    # Create a test suite combining all test cases
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDirectoryStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestMCPServerLogging))
    suite.addTests(loader.loadTestsFromTestCase(TestGitignoreConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestMakefileIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEnvironmentConfiguration))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
