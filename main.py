from core.mcp_agent import MCPAgent
from core.ollama_llm import ollama_llm_streaming
from core.llm_cache import cached_llm
from core.gmail_client import get_latest_email

def main():
    agent = MCPAgent(local_llm=lambda p: cached_llm(p, ollama_llm_streaming))
    email = get_latest_email()
    if email is None:
        print("📭 No emails found.")
        return
    subject, sender, body = email
    print(f"📧 Email from {sender}, subject: {subject}\n\n{body[:300]}...\n")
    prompt = f"Write a professional reply to this email from {sender} with subject '{subject}':\n\n{body}"
    response = agent.run(prompt)
    print(f"🤖 Response:\n{response}")
