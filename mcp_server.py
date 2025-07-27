#!/usr/bin/env python3
"""
FastMCP Gmail - Primary MCP Server Implementation
Uses FastMCP Framework for robust Model Context Protocol support
Provides Gmail reading and email processing tools for Claude Desktop and VS Code
"""

import logging
from typing import List, Optional
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastmcp import FastMCP
from core.gmail_client import get_gmail_service, test_gmail_connection
from core.gmail_reader import create_gmail_reader
from core.email_summarizer import summarize_emails
from core.ollama_llm import ollama_llm_streaming
from core.llm_cache import cached_llm

# Initialize FastMCP app
app = FastMCP("Gmail Assistant")

# Global variables for Gmail service (initialized once)
gmail_service = None
gmail_reader = None


def generate_email_summary(emails):
    """
    Generate AI summary for a list of emails
    
    Args:
        emails: List of email dictionaries
        
    Returns:
        Dictionary with summary and insights
    """
    if not emails:
        return {"summary": "No emails to summarize", "key_insights": [], "action_items": []}
    
    # Prepare email content for summarization
    email_content = []
    for email in emails[:10]:  # Limit to first 10 emails to avoid token limits
        content = f"From: {email.get('sender', 'Unknown')}\n"
        content += f"Subject: {email.get('subject', 'No Subject')}\n"
        content += f"Preview: {email.get('content_preview', '')[:200]}...\n"
        email_content.append(content)
    
    # Create summarization prompt
    combined_emails = "\n---\n".join(email_content)
    prompt = f"""Analyze these {len(emails)} emails and provide:
1. A concise overall summary (2-3 sentences)
2. Key insights (3-5 bullet points)
3. Action items needed (if any)

Emails:
{combined_emails}

Format your response as:
SUMMARY: [your summary]
INSIGHTS: [bullet points]
ACTIONS: [action items if any]"""
    
    try:
        # Use the cached LLM function
        result = cached_llm(prompt, ollama_llm_streaming)
        response_text = result.get("text", "Failed to generate summary")
        
        # Parse the response
        summary = "Summary not available"
        insights = []
        actions = []
        
        if "SUMMARY:" in response_text:
            summary_part = response_text.split("SUMMARY:")[1].split("INSIGHTS:")[0].strip()
            summary = summary_part if summary_part else "Summary generated successfully"
        
        if "INSIGHTS:" in response_text:
            insights_part = response_text.split("INSIGHTS:")[1].split("ACTIONS:")[0].strip()
            insights = [line.strip() for line in insights_part.split('\n') if line.strip()]
        
        if "ACTIONS:" in response_text:
            actions_part = response_text.split("ACTIONS:")[1].strip()
            actions = [line.strip() for line in actions_part.split('\n') if line.strip()]
        
        return {
            "summary": summary,
            "key_insights": insights,
            "action_items": actions,
            "raw_response": response_text
        }
        
    except Exception as e:
        return {
            "summary": f"Error generating summary: {str(e)}",
            "key_insights": [],
            "action_items": [],
            "error": str(e)
        }


def setup_logging():
    """Setup logging for the FastMCP server"""
    project_dir = Path(__file__).parent
    log_dir = project_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "fastmcp_server.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def ensure_gmail_connection():
    """Ensure Gmail service is initialized"""
    global gmail_service, gmail_reader

    if gmail_service is None:
        try:
            logger.info("Initializing Gmail service...")
            gmail_service = get_gmail_service()
            gmail_reader = create_gmail_reader(service=gmail_service)
            logger.info("Gmail service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gmail service: {e}")
            raise

    return gmail_service, gmail_reader


@app.tool
def read_latest_emails(count: int = 10, query: str = "") -> List[dict]:
    """
    Read the latest emails from Gmail inbox

    Args:
        count: Number of emails to read (default: 10)
        query: Gmail search query (optional, e.g., 'is:unread', 'from:someone@example.com')

    Returns:
        List of email dictionaries with subject, sender, date, content, etc.
    """
    try:
        logger.info(f"Reading {count} latest emails with query: '{query}'")
        service, reader = ensure_gmail_connection()

        # Use query parameter if provided, otherwise get latest emails
        search_query = query if query.strip() else None
        emails = reader.read_emails(count=count, query=search_query)

        # Simplify email data for Claude Desktop
        simplified_emails = []
        for email in emails:
            simplified_email = {
                "id": email.get("id"),
                "subject": email.get("subject", "(No Subject)"),
                "sender": email.get("sender", "(Unknown)"),
                "date": str(email.get("date")) if email.get("date") else "Unknown",
                "content_preview": (
                    email.get("content", {}).get("text", "")[:500] + "..."
                    if len(email.get("content", {}).get("text", "")) > 500
                    else email.get("content", {}).get("text", "")
                ),
                "is_unread": email.get("metadata", {}).get("is_unread", False),
                "has_attachments": email.get("metadata", {}).get(
                    "has_attachments", False
                ),
                "importance": email.get("metadata", {}).get("importance", "normal"),
            }
            simplified_emails.append(simplified_email)

        logger.info(f"Successfully retrieved {len(simplified_emails)} emails")
        return simplified_emails

    except Exception as e:
        logger.error(f"Error reading emails: {e}")
        return [{"error": f"Failed to read emails: {str(e)}"}]


@app.tool
def search_emails(query: str, max_results: int = 50) -> List[dict]:
    """
    Search emails using Gmail search syntax

    Args:
        query: Gmail search query (e.g., 'from:sender@example.com', 'subject:important', 'is:unread')
        max_results: Maximum number of results to return (default: 50)

    Returns:
        List of matching email dictionaries
    """
    try:
        logger.info(
            f"Searching emails with query: '{query}', max results: {max_results}"
        )
        service, reader = ensure_gmail_connection()

        emails = reader.search_emails(query=query, max_results=max_results)

        # Simplify email data for Claude Desktop
        simplified_emails = []
        for email in emails:
            simplified_email = {
                "id": email.get("id"),
                "subject": email.get("subject", "(No Subject)"),
                "sender": email.get("sender", "(Unknown)"),
                "date": str(email.get("date")) if email.get("date") else "Unknown",
                "content_preview": (
                    email.get("content", {}).get("text", "")[:300] + "..."
                    if len(email.get("content", {}).get("text", "")) > 300
                    else email.get("content", {}).get("text", "")
                ),
                "is_unread": email.get("metadata", {}).get("is_unread", False),
                "has_attachments": email.get("metadata", {}).get(
                    "has_attachments", False
                ),
                "importance": email.get("metadata", {}).get("importance", "normal"),
            }
            simplified_emails.append(simplified_email)

        logger.info(f"Found {len(simplified_emails)} emails matching query")
        return simplified_emails

    except Exception as e:
        logger.error(f"Error searching emails: {e}")
        return [{"error": f"Failed to search emails: {str(e)}"}]


@app.tool
def get_email_details(email_id: str) -> dict:
    """
    Get full details of a specific email by ID

    Args:
        email_id: Gmail message ID

    Returns:
        Complete email details including full content, attachments, etc.
    """
    try:
        logger.info(f"Getting details for email ID: {email_id}")
        service, reader = ensure_gmail_connection()

        email = reader.read_email_by_id(email_id)

        if not email:
            return {"error": f"Email with ID {email_id} not found"}

        # Return full email details
        detailed_email = {
            "id": email.get("id"),
            "thread_id": email.get("thread_id"),
            "subject": email.get("subject", "(No Subject)"),
            "sender": email.get("sender", "(Unknown)"),
            "recipients": email.get("recipients", []),
            "date": str(email.get("date")) if email.get("date") else "Unknown",
            "content": {
                "text": email.get("content", {}).get("text", ""),
                "html": email.get("content", {}).get("html", ""),
                "snippet": email.get("content", {}).get("snippet", ""),
            },
            "attachments": email.get("attachments", []),
            "labels": email.get("labels", []),
            "metadata": email.get("metadata", {}),
            "importance": email.get("metadata", {}).get("importance", "normal"),
        }

        logger.info(f"Successfully retrieved email details for {email_id}")
        return detailed_email

    except Exception as e:
        logger.error(f"Error getting email details: {e}")
        return {"error": f"Failed to get email details: {str(e)}"}


@app.tool
def summarize_emails_tool(count: int = 20, query: str = "is:unread") -> dict:
    """
    Generate a summary of emails using AI

    Args:
        count: Number of emails to summarize (default: 20)
        query: Gmail search query for emails to summarize (default: 'is:unread')

    Returns:
        AI-generated summary of the emails
    """
    try:
        logger.info(f"Generating summary for {count} emails with query: '{query}'")
        service, reader = ensure_gmail_connection()

        # Get emails to summarize
        emails = reader.read_emails(count=count, query=query)

        if not emails:
            return {"summary": "No emails found matching the criteria", "count": 0}

        # Generate summary using AI
        summary_result = generate_email_summary(emails)

        result = {
            "summary": summary_result.get("summary", "Failed to generate summary"),
            "count": len(emails),
            "query_used": query,
            "key_insights": summary_result.get("key_insights", []),
            "action_items": summary_result.get("action_items", []),
        }

        logger.info(f"Successfully generated summary for {len(emails)} emails")
        return result

    except Exception as e:
        logger.error(f"Error generating email summary: {e}")
        return {"error": f"Failed to generate summary: {str(e)}", "count": 0}


@app.tool
def test_gmail_connection_tool() -> dict:
    """
    Test the Gmail API connection and return status

    Returns:
        Connection status and basic account information
    """
    try:
        logger.info("Testing Gmail connection...")

        # Test connection
        connection_result = test_gmail_connection()

        if connection_result.get("success", False):
            # Get basic account info
            service, reader = ensure_gmail_connection()

            result = {
                "status": "connected",
                "success": True,
                "message": "Gmail connection successful",
                "account_info": connection_result.get("profile", {}),
                "total_messages": connection_result.get("message_count", 0),
            }
        else:
            result = {
                "status": "failed",
                "success": False,
                "message": connection_result.get("error", "Unknown connection error"),
            }

        logger.info(f"Gmail connection test result: {result['status']}")
        return result

    except Exception as e:
        logger.error(f"Error testing Gmail connection: {e}")
        return {
            "status": "error",
            "success": False,
            "message": f"Connection test failed: {str(e)}",
        }


@app.tool
def send_email_summary(recipient_email: str = "me", max_emails: int = 10) -> dict:
    """
    Generate and send an AI-powered email summary to a specified recipient

    Args:
        recipient_email: Email address to send summary to (default: "me" for self)
        max_emails: Maximum number of unread emails to include in summary (default: 10)

    Returns:
        Status of the email summary operation
    """
    try:
        logger.info(f"Generating and sending email summary to: {recipient_email}")

        # Import required modules for email sending
        from email.mime.text import MIMEText
        import base64
        from datetime import datetime

        # Get Gmail service
        service, reader = ensure_gmail_connection()

        # Generate summaries using existing functionality
        summaries = summarize_emails()

        if not summaries:
            logger.info("No new unread emails to summarize")
            return {
                "success": True,
                "message": "No new unread emails to summarize",
                "emails_processed": 0,
                "summary_sent": False,
            }

        # Limit the number of emails processed
        summaries = summaries[:max_emails]

        # Create email body with formatted summaries
        def create_email_body(summaries):
            lines = []
            for subject, summary in summaries:
                lines.append(f"🧾 *{subject}*\n{summary}\n")
            return "\n---\n\n".join(lines)

        body = create_email_body(summaries)
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"📬 Daily Email Summary – {today}"

        # Add header with summary count
        header = f"📊 Summary of {len(summaries)} unread emails:\n\n"
        body = header + body

        # Add footer
        footer = f"\n\n---\n📤 Generated by FastMCP Gmail Assistant at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        body = body + footer

        # Create and send email
        message = MIMEText(body)
        message["to"] = recipient_email
        message["from"] = "me"
        message["subject"] = subject

        # Encode message
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send email
        result = (
            service.users().messages().send(userId="me", body={"raw": raw}).execute()
        )

        logger.info(
            f"Successfully sent email summary with {len(summaries)} emails to {recipient_email}"
        )

        return {
            "success": True,
            "message": f"Email summary sent successfully to {recipient_email}",
            "emails_processed": len(summaries),
            "summary_sent": True,
            "message_id": result.get("id"),
            "recipient": recipient_email,
            "subject": subject,
        }

    except Exception as e:
        logger.error(f"Error sending email summary: {e}")
        return {
            "success": False,
            "message": f"Failed to send email summary: {str(e)}",
            "emails_processed": 0,
            "summary_sent": False,
        }


if __name__ == "__main__":
    logger.info("Starting FastMCP Gmail server...")

    # Initialize Gmail connection on startup
    try:
        ensure_gmail_connection()
        logger.info("Gmail service pre-initialized successfully")
    except Exception as e:
        logger.error(f"Failed to pre-initialize Gmail service: {e}")
        logger.warning("Gmail service will be initialized on first tool call")

    # Run the FastMCP server
    app.run()
