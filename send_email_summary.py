from core.email_summarizer import summarize_emails
from core.gmail_client import get_gmail_service
from email.mime.text import MIMEText
import base64
from datetime import datetime


def create_email_body(summaries):
    lines = []
    for subject, summary in summaries:
        lines.append(f"🧾 *{subject}*\n{summary}\n")
    return "\n---\n\n".join(lines)


def send_summary_email():
    summaries = summarize_emails()
    if not summaries:
        print("✅ No new unread emails to summarize.")
        return
    body = create_email_body(summaries)
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"📬 Daily Email Summary – {today}"
    message = MIMEText(body)
    message["to"] = "me"
    message["from"] = "me"
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service = get_gmail_service()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"✅ Sent summary email for {len(summaries)} message(s).")


if __name__ == "__main__":
    send_summary_email()
