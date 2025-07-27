"""
Manual test for send_email_summary MCP tool with real Gmail setup
This test requires valid Gmail credentials and tests the actual MCP tool function
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_real_email_summary_tool():
    """Test the actual send_email_summary MCP tool with real Gmail"""
    print("🧪 Manual Test: send_email_summary MCP Tool")
    print("=" * 50)

    try:
        # Test Gmail connection first
        print("\n1️⃣ Testing Gmail connection...")
        from core.gmail_client import test_gmail_connection

        connection_result = test_gmail_connection()
        if not connection_result.get("success", False):
            print(
                f"❌ Gmail connection failed: {connection_result.get('message', 'Unknown error')}"
            )
            return False

        print(f"✅ Gmail connected: {connection_result.get('message', 'Success')}")

        # Test email summarizer
        print("\n2️⃣ Testing email summarizer...")
        from core.email_summarizer import summarize_emails

        summaries = summarize_emails()
        print(f"📊 Found {len(summaries)} unread emails to summarize")

        if summaries:
            print("📧 Sample summaries:")
            for i, (subject, summary) in enumerate(summaries[:3], 1):
                print(f"   {i}. {subject[:50]}...")
                print(f"      {summary[:100]}...")

        # Test the actual MCP tool function
        print("\n3️⃣ Testing send_email_summary MCP tool...")

        # Import the MCP server to get the tool function
        import mcp_server

        # Get the send_email_summary function
        send_email_summary = mcp_server.send_email_summary

        # Test with sending to self (safe test)
        print("📤 Testing email summary to self...")
        result = send_email_summary(recipient_email="me", max_emails=5)

        print(f"🎯 Result: {result}")

        if result.get("success", False):
            print("✅ Email summary sent successfully!")
            print(f"   📧 Recipient: {result.get('recipient', 'Unknown')}")
            print(f"   📊 Emails processed: {result.get('emails_processed', 0)}")
            print(f"   📬 Message ID: {result.get('message_id', 'Unknown')}")
            print(f"   📝 Subject: {result.get('subject', 'Unknown')}")
        else:
            print(f"❌ Email summary failed: {result.get('message', 'Unknown error')}")
            return False

        # Test edge cases
        print("\n4️⃣ Testing edge cases...")

        # Test with external email (dry run - commented out for safety)
        print("📝 Note: External recipient test skipped for safety")
        print("   To test: send_email_summary('your-email@example.com', 3)")

        # Test with max_emails = 0
        print("🔢 Testing with max_emails=0...")
        zero_result = send_email_summary(recipient_email="me", max_emails=0)
        print(f"   Result: {zero_result.get('message', 'Unknown')}")

        print("\n🎉 All manual tests completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Manual test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_email_summary_components():
    """Test individual components of the email summary system"""
    print("\n🔧 Testing Individual Components")
    print("=" * 30)

    try:
        # Test email body creation
        print("📝 Testing email body formatting...")
        sample_summaries = [
            ("Test Subject 1", "This is a test summary for email 1"),
            ("Test Subject 2", "This is a test summary for email 2"),
        ]

        def create_email_body(summaries):
            lines = []
            for subject, summary in summaries:
                lines.append(f"🧾 *{subject}*\n{summary}\n")
            return "\n---\n\n".join(lines)

        body = create_email_body(sample_summaries)
        print(f"✅ Email body created (length: {len(body)} chars)")

        # Test MIME creation
        print("📧 Testing MIME message creation...")
        from email.mime.text import MIMEText
        import base64

        message = MIMEText(body)
        message["to"] = "test@example.com"
        message["from"] = "me"
        message["subject"] = "Test Summary"

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        print(f"✅ MIME message encoded (length: {len(raw)} chars)")

        # Test date formatting
        print("📅 Testing date formatting...")
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"📬 Daily Email Summary – {today}"
        print(f"✅ Subject generated: {subject}")

        print("🎯 All component tests passed!")
        return True

    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False


def interactive_test():
    """Interactive test allowing user to specify parameters"""
    print("\n🎮 Interactive Test Mode")
    print("=" * 25)

    try:
        recipient = input("📧 Enter recipient email (default: me): ").strip() or "me"
        max_emails_input = input("🔢 Enter max emails (default: 5): ").strip() or "5"

        try:
            max_emails = int(max_emails_input)
        except ValueError:
            print("❌ Invalid number, using default (5)")
            max_emails = 5

        print(f"\n🚀 Testing with recipient='{recipient}', max_emails={max_emails}")

        # Confirm before sending
        if recipient != "me":
            confirm = input(f"⚠️  Send email to {recipient}? (y/N): ").strip().lower()
            if confirm != "y":
                print("❌ Test cancelled by user")
                return False

        # Import and run the tool
        import mcp_server

        result = mcp_server.send_email_summary(
            recipient_email=recipient, max_emails=max_emails
        )

        print(f"\n📊 Result:")
        for key, value in result.items():
            print(f"   {key}: {value}")

        return result.get("success", False)

    except KeyboardInterrupt:
        print("\n❌ Test cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Interactive test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 FastMCP Gmail - Email Summary Tool Manual Test")
    print("=" * 55)

    # Check if credentials exist
    cred_files = [
        "credentials.json",
        str(Path.home() / ".local/fastmcp_gmail/credentials.json"),
    ]
    has_credentials = any(os.path.exists(f) for f in cred_files)

    if not has_credentials:
        print("❌ No Gmail credentials found!")
        print("   Please run 'make setup' first or add credentials.json")
        sys.exit(1)

    print("✅ Gmail credentials found")

    # Run tests
    success = True

    # Component tests (safe, no Gmail API calls)
    success &= test_email_summary_components()

    # Real Gmail tests
    try:
        success &= test_real_email_summary_tool()
    except Exception as e:
        print(f"❌ Real Gmail test skipped due to error: {e}")
        success = False

    # Interactive test (optional)
    run_interactive = input("\n🎮 Run interactive test? (y/N): ").strip().lower()
    if run_interactive == "y":
        success &= interactive_test()

    # Final result
    print(f"\n{'🎉 ALL TESTS PASSED!' if success else '❌ SOME TESTS FAILED!'}")
    sys.exit(0 if success else 1)
