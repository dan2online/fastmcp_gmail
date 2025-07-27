"""
Enhanced main script demonstrating Gmail reader functionality
"""

from core.mcp_agent import MCPAgent
from core.ollama_llm import ollama_llm_streaming
from core.llm_cache import cached_llm
from core.gmail_client import get_latest_email
from core.gmail_reader import create_gmail_reader
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function with enhanced Gmail reading capabilities"""
    agent = MCPAgent(local_llm=lambda p: cached_llm(p, ollama_llm_streaming))

    print("🚀 FastMCP Gmail - Enhanced Email Processing")
    print("=" * 50)

    # Option 1: Use existing functionality (backward compatibility)
    print("\n📧 Option 1: Latest Email (Original)")
    email = get_latest_email()
    if email is None:
        print("📭 No emails found.")
    else:
        subject, sender, body = email
        print(f"📧 Email from {sender}")
        print(f"📝 Subject: {subject}")
        print(f"💬 Content: {body[:200]}{'...' if len(body) > 200 else ''}")

        prompt = f"Write a professional reply to this email from {sender} with subject '{subject}':\n\n{body}"
        response = agent.run(prompt)
        print(f"\n🤖 AI Response:\n{response}")

    # Option 2: Use enhanced Gmail reader
    print("\n" + "=" * 50)
    print("📧 Option 2: Enhanced Email Reader")

    try:
        # Create enhanced Gmail reader
        reader = create_gmail_reader(logger=logger)

        # Read multiple emails
        print("\n📬 Reading latest 5 emails...")
        emails = reader.read_emails(count=5)

        if not emails:
            print("📭 No emails found.")
            return

        # Process each email
        for i, email_data in enumerate(emails, 1):
            print(f"\n📧 Email {i}/{len(emails)}")
            print(f"   📝 Subject: {email_data['subject']}")
            print(f"   👤 From: {email_data['sender']}")
            print(f"   📅 Date: {email_data['date']}")
            print(f"   🏷️  Labels: {', '.join(email_data['labels'])}")
            print(f"   📎 Attachments: {len(email_data['attachments'])}")
            print(f"   ⭐ Importance: {email_data['metadata']['importance']}")
            print(f"   👁️  Unread: {email_data['metadata']['is_unread']}")

            # Show content preview
            content_text = email_data["content"]["text"]
            if content_text:
                preview = content_text[:150].replace("\n", " ")
                print(
                    f"   💬 Preview: {preview}{'...' if len(content_text) > 150 else ''}"
                )

            # Generate AI response for unread emails
            if (
                email_data["metadata"]["is_unread"] and i <= 3
            ):  # Limit to first 3 unread
                print(f"   🤖 Generating AI response...")
                prompt = f"Write a professional reply to this email from {email_data['sender']} with subject '{email_data['subject']}':\n\n{content_text}"
                response = agent.run(prompt)
                print(
                    f"   📝 AI Response: {response[:100]}{'...' if len(response) > 100 else ''}"
                )

        # Demonstrate search functionality
        print(f"\n🔍 Searching for unread emails...")
        unread_emails = reader.search_emails("is:unread", max_results=3)
        print(f"   Found {len(unread_emails)} unread emails")

        for email_data in unread_emails:
            print(f"   📧 {email_data['subject']} - from {email_data['sender']}")

    except Exception as e:
        logger.error(f"Error with enhanced Gmail reader: {e}")
        print(f"❌ Enhanced reader failed: {e}")
        print("📧 Falling back to original functionality...")


def demo_advanced_features():
    """Demonstrate advanced Gmail reader features"""
    print("\n🚀 Advanced Gmail Reader Features Demo")
    print("=" * 50)

    try:
        reader = create_gmail_reader(logger=logger)

        # Search with different queries
        queries = ["from:noreply", "has:attachment", "is:important", "newer_than:7d"]

        for query in queries:
            print(f"\n🔍 Search: {query}")
            results = reader.search_emails(query, max_results=2)
            print(f"   Found {len(results)} emails")

            for email_data in results:
                print(f"   📧 {email_data['subject'][:50]}...")
                if email_data["attachments"]:
                    print(
                        f"      📎 Attachments: {[att['filename'] for att in email_data['attachments']]}"
                    )

        # Demonstrate content types
        print(f"\n📄 Content Type Analysis")
        emails = reader.read_emails(count=10)

        content_stats = {
            "text_only": 0,
            "html_only": 0,
            "multipart": 0,
            "with_attachments": 0,
        }

        for email_data in emails:
            content = email_data["content"]
            if content["html"] and not content["text"]:
                content_stats["html_only"] += 1
            elif content["text"] and not content["html"]:
                content_stats["text_only"] += 1
            elif content["text"] and content["html"]:
                content_stats["multipart"] += 1

            if email_data["attachments"]:
                content_stats["with_attachments"] += 1

        print(f"   📊 Analysis of {len(emails)} emails:")
        for stat_type, count in content_stats.items():
            print(f"      {stat_type.replace('_', ' ').title()}: {count}")

    except Exception as e:
        logger.error(f"Error in advanced features demo: {e}")
        print(f"❌ Advanced features demo failed: {e}")


if __name__ == "__main__":
    main()

    # Uncomment to run advanced features demo
    # demo_advanced_features()
