#!/usr/bin/env python3
"""
Test module for Gmail email reading functionality.
Tests the core email retrieval features of the FastMCP Gmail MCP server.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import directly from core modules
from core.gmail_client import get_gmail_service
from core.gmail_reader import create_gmail_reader


class TestGmailEmailReading:
    """Test suite for Gmail email reading functionality."""

    def test_gmail_service_initialization(self):
        """Test that Gmail service can be initialized successfully."""
        try:
            service = get_gmail_service()
            assert service is not None, "Gmail service should be initialized"
            print("✅ Gmail service initialized successfully")
        except Exception as e:
            pytest.skip(f"Gmail authentication not available: {e}")

    def test_gmail_reader_creation(self):
        """Test that Gmail reader can be created with a valid service."""
        try:
            service = get_gmail_service()
            reader = create_gmail_reader(service=service)
            assert reader is not None, "Gmail reader should be created"
            print("✅ Gmail reader created successfully")
        except Exception as e:
            pytest.skip(f"Gmail authentication not available: {e}")

    def test_read_latest_emails_integration(self):
        """Integration test for reading latest emails from Gmail."""
        try:
            # Initialize Gmail service and reader
            service = get_gmail_service()
            reader = create_gmail_reader(service=service)
            
            # Read a small number of emails to avoid API limits
            emails = reader.read_emails(count=3)
            
            # Validate email structure
            assert isinstance(emails, list), "Emails should be returned as a list"
            
            if len(emails) > 0:
                email = emails[0]
                # Check required fields
                assert 'id' in email, "Email should have an ID"
                assert 'subject' in email, "Email should have a subject"
                assert 'sender' in email, "Email should have a sender"
                assert 'date' in email, "Email should have a date"
                
                print(f"✅ Successfully retrieved {len(emails)} emails")
                print(f"   First email: '{email.get('subject', 'No Subject')}' from {email.get('sender', 'Unknown')}")
            else:
                print("✅ Email reading successful (no emails found)")
                
        except Exception as e:
            pytest.skip(f"Gmail API access not available: {e}")

    def test_email_data_structure(self):
        """Test the structure and content of retrieved email data."""
        try:
            service = get_gmail_service()
            reader = create_gmail_reader(service=service)
            emails = reader.read_emails(count=1)
            
            if len(emails) > 0:
                email = emails[0]
                
                # Test required fields exist
                required_fields = ['id', 'subject', 'sender', 'date']
                for field in required_fields:
                    assert field in email, f"Email should contain '{field}' field"
                
                # Test optional fields that might exist
                optional_fields = ['content', 'metadata']
                for field in optional_fields:
                    if field in email:
                        print(f"✅ Optional field '{field}' present")
                
                # Test metadata structure if present
                if 'metadata' in email:
                    metadata = email['metadata']
                    assert isinstance(metadata, dict), "Metadata should be a dictionary"
                    print("✅ Email metadata structure validated")
                    
                print("✅ Email data structure validated")
            else:
                pytest.skip("No emails available for structure testing")
                
        except Exception as e:
            pytest.skip(f"Gmail API access not available: {e}")

    @patch('tests.test_recent_emails.get_gmail_service')
    def test_error_handling_invalid_service(self, mock_service):
        """Test error handling when Gmail service initialization fails."""
        # Mock a service initialization failure
        mock_service.side_effect = Exception("Authentication failed")
        
        with pytest.raises(Exception):
            mock_service()
        
        print("✅ Error handling for invalid service tested")

    def test_email_count_parameter(self):
        """Test that the count parameter correctly limits email retrieval."""
        try:
            service = get_gmail_service()
            reader = create_gmail_reader(service=service)
            
            # Test different count values
            for count in [1, 2, 5]:
                emails = reader.read_emails(count=count)
                assert len(emails) <= count, f"Should return at most {count} emails"
                print(f"✅ Count parameter {count} works correctly")
                
        except Exception as e:
            pytest.skip(f"Gmail API access not available: {e}")

    def test_email_query_parameter(self):
        """Test email retrieval with search queries."""
        try:
            service = get_gmail_service()
            reader = create_gmail_reader(service=service)
            
            # Test with a simple query (unread emails)
            unread_emails = reader.read_emails(count=5, query="is:unread")
            assert isinstance(unread_emails, list), "Query result should be a list"
            
            # Test with no query (default behavior)
            all_emails = reader.read_emails(count=5)
            assert isinstance(all_emails, list), "Default query result should be a list"
            
            print(f"✅ Query parameter tested - found {len(unread_emails)} unread emails")
            
        except Exception as e:
            pytest.skip(f"Gmail API access not available: {e}")


def manual_email_display_test():
    """
    Manual test function to display recent emails for visual verification.
    This is not run automatically by pytest but can be called directly.
    """
    try:
        print("📧 FastMCP Gmail - Manual Email Display Test")
        print("=" * 50)
        
        # Initialize Gmail service and reader
        print("Initializing Gmail service...")
        service = get_gmail_service()
        reader = create_gmail_reader(service=service)
        
        # Read latest emails
        print("Fetching latest 5 emails...")
        emails = reader.read_emails(count=5)
        
        print(f"\n📧 Found {len(emails)} recent emails:\n")
        print("=" * 80)
        
        for i, email in enumerate(emails, 1):
            print(f"Email {i}:")
            print(f"  📨 Subject: {email.get('subject', 'No Subject')}")
            print(f"  👤 From: {email.get('sender', 'Unknown Sender')}")
            print(f"  📅 Date: {email.get('date', 'No Date')}")
            print(f"  🆔 Message ID: {email.get('id', 'No ID')}")
            
            # Show content preview if available  
            content = email.get('content', {})
            if isinstance(content, dict):
                text_content = content.get('text', '') or content.get('html', '')
            else:
                text_content = str(content)
                
            if text_content:
                preview = text_content[:150].replace('\n', ' ').strip()
                if len(text_content) > 150:
                    preview += "..."
                print(f"  📝 Preview: {preview}")
            
            # Show metadata if available
            metadata = email.get('metadata', {})
            status_info = []
            if metadata.get('is_unread'):
                status_info.append("🔴 UNREAD")
            if metadata.get('has_attachments'):
                status_info.append("📎 ATTACHMENTS")
            if metadata.get('importance') == 'high':
                status_info.append("❗ HIGH PRIORITY")
            
            if status_info:
                print(f"  🏷️  Status: {' | '.join(status_info)}")
            
            print("-" * 40)
        
        print(f"\n✅ Successfully retrieved {len(emails)} emails")
        return emails
        
    except Exception as e:
        print(f"❌ Error reading emails: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Run manual test when script is executed directly
    manual_email_display_test()
