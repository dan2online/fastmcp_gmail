"""
Enhanced Gmail Reader with comprehensive email processing capabilities
"""

import base64
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class GmailReader:
    """Enhanced Gmail reader with filtering, content extraction, and error handling"""

    def __init__(self, service, logger=None):
        """
        Initialize Gmail reader with service and optional logger

        Args:
            service: Gmail API service object
            logger: Optional logger for debugging and monitoring
        """
        self.service = service
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("GmailReader initialized")

    def read_emails(self, count=10, query=None, include_spam_trash=False):
        """
        Read multiple emails with optional filtering

        Args:
            count: Number of emails to read (default: 10)
            query: Gmail search query string (optional)
            include_spam_trash: Whether to include spam and trash (default: False)

        Returns:
            List of email dictionaries with enhanced content
        """
        try:
            self.logger.info(f"Reading {count} emails with query: {query}")

            # Build request parameters
            request_params = {"userId": "me", "maxResults": count}

            if query:
                request_params["q"] = query

            if not include_spam_trash:
                request_params["q"] = request_params.get("q", "") + " -in:spam -in:trash"

            # Get message list
            result = self.service.users().messages().list(**request_params).execute()
            messages = result.get("messages", [])

            if not messages:
                self.logger.info("No messages found")
                return []

            # Fetch detailed email data for each message
            emails = []
            for message in messages:
                try:
                    email_data = self.read_email_by_id(message["id"])
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    self.logger.error(f"Error reading email {message['id']}: {e}")
                    continue

            self.logger.info(f"Successfully read {len(emails)} emails")
            return emails

        except Exception as e:
            self.logger.error(f"Error reading emails: {e}")
            raise

    def read_email_by_id(self, email_id):
        """
        Read a specific email by ID

        Args:
            email_id: Gmail message ID

        Returns:
            Dictionary with email data and content
        """
        try:
            self.logger.debug(f"Reading email ID: {email_id}")

            # Get full email data
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=email_id, format="full")
                .execute()
            )

            # Extract and structure email data
            email_data = self._extract_email_data(message)

            self.logger.debug(f"Successfully read email: {email_data.get('subject', 'No Subject')}")
            return email_data

        except Exception as e:
            self.logger.error(f"Error reading email {email_id}: {e}")
            raise

    def search_emails(self, query, max_results=50):
        """
        Search emails using Gmail query syntax

        Args:
            query: Gmail search query
            max_results: Maximum number of results

        Returns:
            List of email dictionaries matching the query
        """
        self.logger.info(f"Searching emails with query: {query}")
        return self.read_emails(count=max_results, query=query)

    def get_email_content(self, email_data):
        """
        Extract and process email content

        Args:
            email_data: Raw email data from Gmail API

        Returns:
            Dictionary with processed content (text, html, snippet)
        """
        try:
            payload = email_data.get("payload", {})
            content = {"text": "", "html": "", "snippet": email_data.get("snippet", "")}

            # Handle different MIME types
            mime_type = payload.get("mimeType", "")

            if mime_type == "text/plain":
                content["text"] = self._decode_body_data(payload.get("body", {}))
            elif mime_type == "text/html":
                content["html"] = self._decode_body_data(payload.get("body", {}))
                content["text"] = self._html_to_text(content["html"])
            elif mime_type.startswith("multipart/"):
                content = self._extract_multipart_content(payload)

            return content

        except Exception as e:
            self.logger.error(f"Error extracting email content: {e}")
            return {"text": "", "html": "", "snippet": email_data.get("snippet", "")}

    def extract_attachments_info(self, email_data):
        """
        Extract attachment information from email

        Args:
            email_data: Raw email data from Gmail API

        Returns:
            List of attachment dictionaries
        """
        attachments = []
        try:
            payload = email_data.get("payload", {})
            parts = payload.get("parts", [])

            for part in parts:
                disposition = part.get("headers", {})
                filename = None

                # Look for Content-Disposition header
                for header in part.get("headers", []):
                    if header.get("name", "").lower() == "content-disposition":
                        if "attachment" in header.get("value", "").lower():
                            # Extract filename from header value
                            value = header.get("value", "")
                            if "filename=" in value:
                                filename = value.split("filename=")[1].strip('"')

                if filename or part.get("filename"):
                    attachment_info = {
                        "filename": filename or part.get("filename", "unknown"),
                        "mime_type": part.get("mimeType", "application/octet-stream"),
                        "size": part.get("body", {}).get("size", 0),
                        "attachment_id": part.get("body", {}).get("attachmentId"),
                    }
                    attachments.append(attachment_info)

            return attachments

        except Exception as e:
            self.logger.error(f"Error extracting attachments: {e}")
            return []

    def _extract_email_data(self, message):
        """Extract structured data from Gmail message"""
        try:
            # Extract headers
            headers = {}
            for header in message.get("payload", {}).get("headers", []):
                headers[header["name"].lower()] = header["value"]

            # Extract content
            content = self.get_email_content(message)

            # Extract attachments
            attachments = self.extract_attachments_info(message)

            # Build structured email data
            email_data = {
                "id": message.get("id"),
                "thread_id": message.get("threadId"),
                "labels": message.get("labelIds", []),
                "subject": headers.get("subject", "(No Subject)"),
                "sender": headers.get("from", "(Unknown)"),
                "recipients": self._parse_recipients(headers),
                "date": self._parse_date(headers.get("date")),
                "content": content,
                "attachments": attachments,
                "metadata": {
                    "importance": self._determine_importance(headers, message),
                    "is_unread": "UNREAD" in message.get("labelIds", []),
                    "has_attachments": len(attachments) > 0,
                    "size_estimate": message.get("sizeEstimate", 0),
                },
                "raw_headers": headers,
            }

            return email_data

        except Exception as e:
            self.logger.error(f"Error extracting email data: {e}")
            return None

    def _decode_body_data(self, body):
        """Decode base64 encoded body data"""
        try:
            data = body.get("data", "")
            if data:
                # Gmail API returns base64url encoded data
                decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                return decoded
            return ""
        except Exception as e:
            self.logger.error(f"Error decoding body data: {e}")
            return ""

    def _extract_multipart_content(self, payload):
        """Extract content from multipart email"""
        content = {"text": "", "html": "", "snippet": ""}

        try:
            parts = payload.get("parts", [])
            for part in parts:
                mime_type = part.get("mimeType", "")

                if mime_type == "text/plain":
                    content["text"] = self._decode_body_data(part.get("body", {}))
                elif mime_type == "text/html":
                    content["html"] = self._decode_body_data(part.get("body", {}))
                elif mime_type.startswith("multipart/"):
                    # Recursive handling of nested multipart
                    nested_content = self._extract_multipart_content(part)
                    if nested_content["text"]:
                        content["text"] = nested_content["text"]
                    if nested_content["html"]:
                        content["html"] = nested_content["html"]

            # Convert HTML to text if we only have HTML
            if content["html"] and not content["text"]:
                content["text"] = self._html_to_text(content["html"])

        except Exception as e:
            self.logger.error(f"Error extracting multipart content: {e}")

        return content

    def _html_to_text(self, html_content):
        """Convert HTML content to plain text"""
        try:
            # Simple HTML to text conversion
            # In a real implementation, you might want to use BeautifulSoup
            import re

            # Remove HTML tags
            text = re.sub("<[^<]+?>", "", html_content)

            # Clean up whitespace
            text = re.sub(r"\s+", " ", text)
            text = text.strip()

            return text

        except Exception as e:
            self.logger.error(f"Error converting HTML to text: {e}")
            return html_content

    def _parse_recipients(self, headers):
        """Parse recipient information from headers"""
        recipients = []

        # Check 'to', 'cc', 'bcc' headers
        for field in ["to", "cc", "bcc"]:
            value = headers.get(field, "")
            if value:
                # Simple parsing - in reality you'd want more sophisticated parsing
                recipients.extend([addr.strip() for addr in value.split(",") if addr.strip()])

        return recipients

    def _parse_date(self, date_str):
        """Parse email date string to datetime object"""
        if not date_str:
            return None

        try:
            # This is a simplified parser - you might want to use dateutil.parser
            from email.utils import parsedate_to_datetime

            return parsedate_to_datetime(date_str)
        except Exception as e:
            self.logger.error(f"Error parsing date '{date_str}': {e}")
            return None

    def _determine_importance(self, headers, message):
        """Determine email importance based on headers and labels"""
        # Check for importance headers
        importance = headers.get("importance", "").lower()
        priority = headers.get("x-priority", "")

        if importance in ["high", "urgent"] or priority in ["1", "2"]:
            return "high"
        elif importance in ["low"] or priority in ["4", "5"]:
            return "low"
        else:
            return "normal"


# Convenience function to maintain backward compatibility
def create_gmail_reader(service=None, logger=None):
    """
    Create a GmailReader instance with optional service and logger

    Args:
        service: Gmail API service (will create one if not provided)
        logger: Optional logger

    Returns:
        GmailReader instance
    """
    if service is None:
        from .gmail_client import get_gmail_service

        service = get_gmail_service()

    return GmailReader(service, logger)
