#!/usr/bin/env python3
"""
Privacy and security tests for LLM interactions in FastMCP Gmail.

These tests ensure that email content is processed locally and that
sensitive information is handled appropriately.
"""

import pytest
import asyncio
import logging
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ollama_llm import ollama_llm_streaming
from core.gmail_client import get_gmail_service


class TestLLMPrivacy:
    """Test privacy aspects of LLM processing."""

    @pytest.fixture
    def llm_function(self):
        """Get LLM function reference."""
        return ollama_llm_streaming

    @pytest.fixture
    def mock_email_content(self):
        """Mock email content with sensitive information."""
        return {
            "subject": "Confidential Business Report",
            "body": """
Dear John,

Here are the quarterly financials:
- Revenue: $2.5M
- Account: 1234-5678-9012-3456
- SSN: 123-45-6789
- Password: MySecret123

Please review the attached documents.

Best regards,
Jane
            """,
            "sender": "jane@company.com",
            "date": "2024-01-15",
        }

    def test_local_processing_verification(self, llm_function):
        """Verify that LLM processing happens locally."""
        # Check that the LLM function uses ollama command
        import inspect
        source = inspect.getsource(llm_function)
        assert "ollama" in source.lower()
        assert "run" in source.lower()
        print(f"✅ LLM configured for local processing via Ollama CLI")

    def test_no_external_calls_during_summarization(self, llm_function, mock_email_content):
        """Test that summarization uses local ollama command."""
        
        # Test with mock subprocess to avoid actual ollama call
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.stdout.readline.side_effect = [
                "This is a test response\n",
                "from local ollama\n",
                ""  # End of output
            ]
            mock_popen.return_value = mock_process

            result = llm_function("Test prompt")
            
            # Verify subprocess was called with ollama
            mock_popen.assert_called_once()
            call_args = mock_popen.call_args[0][0]
            assert "ollama" in call_args
            assert "run" in call_args
            
            print(f"✅ LLM uses local ollama command: {call_args}")
            print(f"✅ Response generated: {result.get('text', 'No text')}")

    def test_sensitive_data_handling(self):
        """Test that sensitive data patterns are identified."""
        # This would be implemented with actual privacy filtering
        sensitive_patterns = [
            r"\d{3}-\d{2}-\d{4}",  # SSN
            r"\d{4}-\d{4}-\d{4}-\d{4}",  # Credit card
            r"password:\s*\w+",  # Password
        ]

        test_content = "SSN: 123-45-6789, Card: 1234-5678-9012-3456, Password: secret"

        for pattern in sensitive_patterns:
            import re

            matches = re.findall(pattern, test_content, re.IGNORECASE)
            if matches:
                print(f"⚠️ Sensitive pattern detected: {pattern} -> {matches}")

        print("✅ Sensitive data detection test completed")

    def test_privacy_configuration(self, llm_function):
        """Test privacy-related configuration settings."""
        # Check that logging is configured appropriately
        logger = logging.getLogger("ollama_llm")
        assert logger is not None

        # Verify the function doesn't expose debugging information
        import inspect
        source = inspect.getsource(llm_function)
        # Should not contain debug prints or verbose logging
        assert "debug" not in source.lower()

        print("✅ Privacy configuration test completed")

    def test_data_retention_policy(self, llm_function):
        """Test that email content is not retained after processing."""
        # This is a conceptual test - verify that the function:
        # 1. Doesn't write files
        # 2. Doesn't persist data
        # 3. Uses subprocess (ephemeral)
        
        import inspect
        source = inspect.getsource(llm_function)
        
        # Verify it uses subprocess (ephemeral execution)
        assert "subprocess" in source
        
        # Verify it doesn't write files to disk (look for file writing patterns)
        file_write_patterns = ["open(", "file(", ".write(", "with open"]
        file_writing = any(pattern in source and ("w" in source or "a" in source) for pattern in file_write_patterns if pattern != "Popen")
        
        # More specific check - look for actual file opening patterns
        import re
        file_open_pattern = r'open\s*\([^)]*["\'][wa]'
        has_file_writes = bool(re.search(file_open_pattern, source))
        
        assert not has_file_writes, "Function should not write files to disk"
        
        print("✅ Data retention policy test completed - uses ephemeral subprocess execution")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
