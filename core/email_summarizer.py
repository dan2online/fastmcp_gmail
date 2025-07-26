import os
import json
from datetime import datetime
from pathlib import Path
from core.gmail_client import get_gmail_service
from core.llm_cache import cached_llm
from core.ollama_llm import ollama_llm_streaming

# Use cache directory for cache files
CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "email_summary_cache.json"


def load_cache():
    return json.load(open(CACHE_FILE)) if CACHE_FILE.exists() else {}


def save_cache(cache):
    # Ensure parent directory exists
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def fetch_unread_messages():
    service = get_gmail_service()
    result = service.users().messages().list(userId="me", q="is:unread", maxResults=10).execute()
    return result.get("messages", [])


def fetch_email_content(service, msg_id):
    msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
    subject = headers.get("Subject", "(No Subject)")
    sender = headers.get("From", "(Unknown)")
    snippet = msg.get("snippet", "")
    return subject, sender, snippet


def summarize_emails():
    cache = load_cache()
    service = get_gmail_service()
    messages = fetch_unread_messages()
    summaries = []
    for msg in messages:
        msg_id = msg["id"]
        if msg_id in cache:
            continue
        subject, sender, snippet = fetch_email_content(service, msg_id)
        prompt = f"Summarize this email clearly in 1 sentence, then extract 3 keywords:\nFrom: {sender}\nSubject: {subject}\n\n{snippet}"
        result = cached_llm(prompt, ollama_llm_streaming)
        cache[msg_id] = {"subject": subject, "summary": result["text"]}
        summaries.append((subject, result["text"]))
    save_cache(cache)
    return summaries
