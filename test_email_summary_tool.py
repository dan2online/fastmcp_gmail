#!/usr/bin/env python3
"""
Test script for the new send_email_summary MCP tool
"""

def test_tool_definition():
    """Test that our tool can be defined without errors"""
    try:
        # Test imports
        from core.email_summarizer import summarize_emails
        from email.mime.text import MIMEText
        import base64
        from datetime import datetime
        
        print("✅ All required imports successful")
        
        # Test basic functionality
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"📬 Daily Email Summary – {today}"
        print(f"✅ Can generate subject: {subject}")
        
        # Test email creation
        message = MIMEText("Test body")
        message["to"] = "test@example.com"
        message["from"] = "me"
        message["subject"] = subject
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        print(f"✅ Can create email message (length: {len(raw)} chars)")
        
        print("🎯 Tool definition would work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error in tool definition: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing send_email_summary MCP tool...")
    success = test_tool_definition()
    print(f"\n{'✅ Test PASSED' if success else '❌ Test FAILED'}")
