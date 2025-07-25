from datetime import datetime
from pathlib import Path

LOG_FILE = Path("llm_log.md")

def log_prompt_response(prompt, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"### 🕒 {timestamp}\n\n**Prompt:**\n```\n{prompt}\n```\n\n**Response:**\n```\n{response}\n```\n\n---\n"
    LOG_FILE.write_text(entry + LOG_FILE.read_text() if LOG_FILE.exists() else entry)
