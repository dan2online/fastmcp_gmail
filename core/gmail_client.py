import os
import os.path
import logging
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from base64 import urlsafe_b64decode
from email import message_from_bytes

# Setup logging
logger = logging.getLogger(__name__)


def get_config_directory():
    """Get the FastMCP Gmail configuration directory"""
    home_dir = Path.home()
    config_dir = home_dir / ".local" / "fastmcp_gmail"

    # Create directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Config directory: {config_dir}")

    return config_dir


def find_config_file(filename, fallback_local=True):
    """
    Find configuration file in order of preference:
    1. User config directory (~/.local/fastmcp_gmail/)
    2. Current project directory (if fallback_local=True)
    """
    config_dir = get_config_directory()
    config_file = config_dir / filename

    # Check user config directory first
    if config_file.exists():
        logger.debug(f"Using config file from user directory: {config_file}")
        return str(config_file)

    # Fallback to local project directory
    if fallback_local and os.path.exists(filename):
        logger.debug(f"Using config file from project directory: {filename}")
        return filename

    # Return user config path (for creation)
    logger.debug(f"Config file not found, will use: {config_file}")
    return str(config_file)


# Load environment variables
def load_env_config():
    """Load configuration from environment variables or .env files"""
    config = {}

    # Try to load from user config directory first
    config_dir = get_config_directory()
    user_env_file = config_dir / "fastmcp_gmail.env"

    # Try local .env.local as fallback
    local_env_file = ".env.local"

    env_files = [str(user_env_file), local_env_file]

    for env_file in env_files:
        if os.path.exists(env_file):
            try:
                logger.debug(f"Loading environment from: {env_file}")
                with open(env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            # Only set if not already in environment
                            if key.strip() not in os.environ:
                                os.environ[key.strip()] = value.strip()
                break  # Use first found file
            except Exception as e:
                logger.warning(f"Could not load {env_file}: {e}")

    # Configuration with defaults, using smart file resolution
    config["credentials_file"] = find_config_file(
        os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
    )
    config["token_file"] = find_config_file(os.getenv("GMAIL_TOKEN_FILE", "token.json"))
    config["scopes"] = os.getenv(
        "GMAIL_SCOPES", "https://www.googleapis.com/auth/gmail.modify"
    ).split(",")

    return config


# Load configuration
ENV_CONFIG = load_env_config()
SCOPES = ENV_CONFIG["scopes"]


def get_gmail_service():
    """
    Get authenticated Gmail service with environment configuration support
    """
    try:
        credentials_file = ENV_CONFIG["credentials_file"]
        token_file = ENV_CONFIG["token_file"]

        # Check if credentials file exists
        if not os.path.exists(credentials_file):
            raise FileNotFoundError(
                f"Gmail credentials file '{credentials_file}' not found. "
                f"Please follow GMAIL_SETUP.md for setup instructions."
            )

        creds = None

        # Load existing token if available
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
                logger.debug(f"Loaded existing credentials from {token_file}")
            except Exception as e:
                logger.warning(f"Could not load token file {token_file}: {e}")
                # Remove corrupted token file
                try:
                    os.remove(token_file)
                except:
                    pass

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    logger.info("Refreshing expired credentials...")
                    creds.refresh(Request())
                    logger.info("Credentials refreshed successfully")
                except Exception as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    creds = None

            if not creds:
                logger.info("Starting OAuth flow for new credentials...")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    logger.info("OAuth flow completed successfully")
                except Exception as e:
                    logger.error(f"OAuth flow failed: {e}")
                    raise Exception(
                        f"Failed to authenticate with Gmail API. "
                        f"Please check your credentials file and internet connection. Error: {e}"
                    )

            # Save credentials
            try:
                with open(token_file, "w") as token:
                    token.write(creds.to_json())
                logger.debug(f"Saved credentials to {token_file}")
            except Exception as e:
                logger.warning(f"Could not save token file: {e}")

        # Build and return service
        service = build("gmail", "v1", credentials=creds)
        logger.info("Gmail service initialized successfully")
        return service

    except Exception as e:
        logger.error(f"Failed to initialize Gmail service: {e}")
        raise


def get_latest_email():
    """
    Get the latest email with enhanced error handling
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=1).execute()
        messages = results.get("messages", [])

        if not messages:
            logger.info("No messages found in mailbox")
            return None

        msg_id = messages[0]["id"]
        logger.debug(f"Fetching latest email with ID: {msg_id}")

        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="raw")
            .execute()
        )
        raw_data = urlsafe_b64decode(msg["raw"].encode("ASCII"))
        mime_msg = message_from_bytes(raw_data)

        subject = mime_msg.get("Subject", "(No Subject)")
        sender = mime_msg.get("From", "(Unknown)")

        # Get email body
        body = mime_msg.get_payload(decode=True)
        if body is None and mime_msg.is_multipart():
            for part in mime_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    break

        if body:
            body = body.decode(errors="ignore")
        else:
            body = ""

        logger.info(f"Successfully retrieved email: {subject[:50]}...")
        return subject.strip(), sender.strip(), body.strip()

    except Exception as e:
        logger.error(f"Failed to get latest email: {e}")
        raise


def test_gmail_connection():
    """
    Test Gmail API connection and authentication
    """
    try:
        logger.info("Testing Gmail API connection...")
        service = get_gmail_service()

        # Test basic API call
        profile = service.users().getProfile(userId="me").execute()
        email_address = profile.get("emailAddress", "unknown")
        total_messages = profile.get("messagesTotal", 0)

        logger.info(f"Successfully connected to Gmail for: {email_address}")
        logger.info(f"Total messages in mailbox: {total_messages}")

        # Test reading emails
        results = service.users().messages().list(userId="me", maxResults=1).execute()
        messages = results.get("messages", [])

        if messages:
            logger.info("Successfully accessed email list")
            return True, f"Connected to {email_address} with {total_messages} messages"
        else:
            logger.warning("No messages found in mailbox")
            return True, f"Connected to {email_address} but no messages found"

    except Exception as e:
        logger.error(f"Gmail connection test failed: {e}")
        return False, str(e)
    if not messages:
        return None
    msg = (
        service.users()
        .messages()
        .get(userId="me", id=messages[0]["id"], format="raw")
        .execute()
    )
    raw_data = urlsafe_b64decode(msg["raw"].encode("ASCII"))
    mime_msg = message_from_bytes(raw_data)
    subject = mime_msg.get("Subject", "(No Subject)")
    sender = mime_msg.get("From", "(Unknown)")
    body = mime_msg.get_payload(decode=True)
    if body is None and mime_msg.is_multipart():
        body = mime_msg.get_payload(0).get_payload(decode=True)
    body = body.decode(errors="ignore") if body else ""
    return subject.strip(), sender.strip(), body.strip()
