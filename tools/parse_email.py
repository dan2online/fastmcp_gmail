from email import message_from_string

def extract_subject_and_sender(raw_email: str):
    msg = message_from_string(raw_email)
    subject = msg.get("Subject", "")
    sender = msg.get("From", "")
    return {"subject": subject, "sender": sender}
