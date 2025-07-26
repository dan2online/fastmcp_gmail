"""
Basic tests for FastMCP Gmail project
"""
import unittest
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestImports(unittest.TestCase):
    """Test that all core modules can be imported"""
    
    def test_import_mcp_agent(self):
        """Test MCPAgent import"""
        from core.mcp_agent import MCPAgent
        agent = MCPAgent()
        self.assertIsNotNone(agent)
    
    def test_import_gmail_client(self):
        """Test Gmail client import"""
        from core.gmail_client import get_gmail_service
        self.assertIsNotNone(get_gmail_service)
    
    def test_import_ollama_llm(self):
        """Test Ollama LLM import"""
        from core.ollama_llm import ollama_llm_streaming
        self.assertIsNotNone(ollama_llm_streaming)
    
    def test_import_llm_cache(self):
        """Test LLM cache import"""
        from core.llm_cache import cached_llm, load_cache, save_cache
        self.assertIsNotNone(cached_llm)
        self.assertIsNotNone(load_cache)
        self.assertIsNotNone(save_cache)
    
    def test_import_email_summarizer(self):
        """Test email summarizer import"""
        from core.email_summarizer import summarize_emails
        self.assertIsNotNone(summarize_emails)


class TestMCPAgent(unittest.TestCase):
    """Test MCPAgent functionality"""
    
    def test_agent_creation(self):
        """Test creating an MCPAgent instance"""
        from core.mcp_agent import MCPAgent
        agent = MCPAgent()
        self.assertIsNotNone(agent)
        self.assertIsNone(agent.local_llm)
    
    def test_agent_with_mock_llm(self):
        """Test MCPAgent with a mock LLM"""
        from core.mcp_agent import MCPAgent
        
        def mock_llm(prompt):
            return {"text": "Mock response", "confidence": 0.9}
        
        agent = MCPAgent(local_llm=mock_llm)
        response = agent.run("Test prompt")
        self.assertEqual(response, "Mock response")
    
    def test_agent_low_confidence(self):
        """Test MCPAgent with low confidence response"""
        from core.mcp_agent import MCPAgent
        
        def low_confidence_llm(prompt):
            return {"text": "Uncertain response", "confidence": 0.5}
        
        agent = MCPAgent(local_llm=low_confidence_llm)
        response = agent.run("Test prompt")
        self.assertTrue(response.startswith("[Low confidence]"))
    
    def test_agent_no_llm(self):
        """Test MCPAgent without LLM"""
        from core.mcp_agent import MCPAgent
        agent = MCPAgent()
        response = agent.run("Test prompt")
        self.assertTrue(response.startswith("[No LLM available]"))


class TestLLMCache(unittest.TestCase):
    """Test LLM caching functionality"""
    
    def setUp(self):
        """Setup test environment"""
        # Clean up any existing cache files
        import os
        import shutil
        for cache_dir in ["cache", "logs"]:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        import os
        import shutil
        for cache_dir in ["cache", "logs"]:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
    
    def test_cache_operations(self):
        """Test basic cache load/save operations"""
        from core.llm_cache import load_cache, save_cache
        
        # Test empty cache (should be empty after cleanup)
        cache = load_cache()
        self.assertEqual(cache, {})
        
        # Test save and load
        test_data = {"test_prompt": {"text": "test_response", "confidence": 0.9}}
        save_cache(test_data)
        loaded_cache = load_cache()
        self.assertEqual(loaded_cache, test_data)


class TestEmailParsing(unittest.TestCase):
    """Test email parsing utilities"""
    
    def test_parse_email_headers(self):
        """Test email header parsing"""
        from tools.parse_email import extract_subject_and_sender
        
        raw_email = """Subject: Test Subject
From: test@example.com
To: recipient@example.com

Test email body
"""
        result = extract_subject_and_sender(raw_email)
        self.assertEqual(result["subject"], "Test Subject")
        self.assertEqual(result["sender"], "test@example.com")


if __name__ == '__main__':
    unittest.main()
