from datetime import datetime
from pathlib import Path

# Use logs directory for log files
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "llm_log.md"


def log_prompt_response(prompt, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"### 🕒 {timestamp}\n\n**Prompt:**\n```\n{prompt}\n```\n\n**Response:**\n```\n{response}\n```\n\n---\n"

    # Ensure parent directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(entry + LOG_FILE.read_text() if LOG_FILE.exists() else entry)
