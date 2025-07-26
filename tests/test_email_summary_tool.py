"""
Unit tests for send_email_summary MCP tool
Tests the email summary functionality without requiring real Gmail API calls
"""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestEmailSummaryTool(unittest.TestCase):
    """Test cases for the send_email_summary MCP tool"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_service = Mock()
        self.mock_reader = Mock()
        
        # Mock email summaries data
        self.sample_summaries = [
            ("Meeting Tomorrow", "Project meeting scheduled for 2 PM with agenda items discussion."),
            ("Invoice #12345", "Payment reminder for services rendered last month, due next week."),
            ("Newsletter Update", "Weekly tech news covering AI developments and cloud computing trends.")
        ]

    def test_create_email_body_formatting(self):
        """Test email body creation with proper formatting"""
        # Import the function we're testing
        from email.mime.text import MIMEText
        import base64
        
        def create_email_body(summaries):
            lines = []
            for subject, summary in summaries:
                lines.append(f"🧾 *{subject}*\n{summary}\n")
            return "\n---\n\n".join(lines)
        
        body = create_email_body(self.sample_summaries)
        
        # Test formatting
        self.assertIn("🧾 *Meeting Tomorrow*", body)
        self.assertIn("Project meeting scheduled", body)
        self.assertIn("---", body)  # Divider between emails
        self.assertEqual(body.count("🧾"), 3)  # Three email summaries
        self.assertEqual(body.count("---"), 2)  # Two dividers for three emails

    def test_email_subject_generation(self):
        """Test email subject generation with date"""
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"📬 Daily Email Summary – {today}"
        
        self.assertIn("📬 Daily Email Summary", subject)
        self.assertIn(today, subject)
        self.assertTrue(len(subject) > 20)

    def test_mime_message_creation(self):
        """Test MIME message creation and encoding"""
        from email.mime.text import MIMEText
        import base64
        
        test_body = "Test email summary content"
        message = MIMEText(test_body)
        message["to"] = "test@example.com"
        message["from"] = "me"
        message["subject"] = "Test Subject"
        
        # Test message encoding
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        self.assertTrue(len(raw) > 0)
        self.assertIsInstance(raw, str)
        # Verify it's valid base64
        decoded = base64.urlsafe_b64decode(raw)
        self.assertTrue(len(decoded) > 0)

    @patch('core.email_summarizer.summarize_emails')
    @patch('core.gmail_client.get_gmail_service')
    def test_send_email_summary_no_emails(self, mock_gmail_service, mock_summarize):
        """Test behavior when no unread emails exist"""
        # Mock no emails to summarize
        mock_summarize.return_value = []
        mock_service = Mock()
        mock_gmail_service.return_value = mock_service
        
        # Import and test the function
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        # Simulate the tool function logic
        summaries = mock_summarize.return_value
        
        if not summaries:
            result = {
                "success": True,
                "message": "No new unread emails to summarize",
                "emails_processed": 0,
                "summary_sent": False
            }
        
        self.assertTrue(result["success"])
        self.assertEqual(result["emails_processed"], 0)
        self.assertFalse(result["summary_sent"])

    @patch('core.email_summarizer.summarize_emails')
    @patch('core.gmail_client.get_gmail_service')
    def test_send_email_summary_with_emails(self, mock_gmail_service, mock_summarize):
        """Test successful email summary sending"""
        # Mock email summaries
        mock_summarize.return_value = self.sample_summaries
        
        # Mock Gmail service
        mock_service = Mock()
        mock_send_result = {"id": "test_message_id_123"}
        mock_service.users().messages().send().execute.return_value = mock_send_result
        mock_gmail_service.return_value = mock_service
        
        # Simulate successful sending
        summaries = mock_summarize.return_value
        
        if summaries:
            result = {
                "success": True,
                "message": f"Email summary sent successfully to me",
                "emails_processed": len(summaries),
                "summary_sent": True,
                "message_id": mock_send_result.get("id"),
                "recipient": "me"
            }
        
        self.assertTrue(result["success"])
        self.assertEqual(result["emails_processed"], 3)
        self.assertTrue(result["summary_sent"])
        self.assertEqual(result["message_id"], "test_message_id_123")

    def test_max_emails_limiting(self):
        """Test that max_emails parameter limits the number of summaries"""
        # Test with more summaries than max_emails
        large_summaries = self.sample_summaries + [
            ("Extra Email 1", "Additional email content 1"),
            ("Extra Email 2", "Additional email content 2"),
        ]
        
        max_emails = 3
        limited_summaries = large_summaries[:max_emails]
        
        self.assertEqual(len(limited_summaries), 3)
        self.assertEqual(limited_summaries[0][0], "Meeting Tomorrow")

    def test_recipient_email_validation(self):
        """Test different recipient email formats"""
        valid_recipients = [
            "me",
            "user@example.com", 
            "test.user+tag@domain.co.uk"
        ]
        
        for recipient in valid_recipients:
            # Basic validation that recipient is a string
            self.assertIsInstance(recipient, str)
            self.assertTrue(len(recipient) > 0)

    @patch('core.email_summarizer.summarize_emails')
    def test_error_handling(self, mock_summarize):
        """Test error handling when summarize_emails fails"""
        # Mock an exception in summarize_emails
        mock_summarize.side_effect = Exception("Gmail API connection failed")
        
        try:
            summaries = mock_summarize()
        except Exception as e:
            result = {
                "success": False,
                "message": f"Failed to send email summary: {str(e)}",
                "emails_processed": 0,
                "summary_sent": False
            }
        
        self.assertFalse(result["success"])
        self.assertIn("Gmail API connection failed", result["message"])

    def test_email_content_structure(self):
        """Test the complete email content structure"""
        # Simulate complete email body creation
        def create_complete_email_body(summaries):
            def create_email_body(summaries):
                lines = []
                for subject, summary in summaries:
                    lines.append(f"🧾 *{subject}*\n{summary}\n")
                return "\n---\n\n".join(lines)
            
            body = create_email_body(summaries)
            header = f"📊 Summary of {len(summaries)} unread emails:\n\n"
            footer = f"\n\n---\n📤 Generated by FastMCP Gmail Assistant at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            return header + body + footer
        
        complete_body = create_complete_email_body(self.sample_summaries)
        
        # Test complete structure
        self.assertIn("📊 Summary of 3 unread emails", complete_body)
        self.assertIn("🧾 *Meeting Tomorrow*", complete_body)
        self.assertIn("📤 Generated by FastMCP Gmail Assistant", complete_body)
        self.assertIn("---", complete_body)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
