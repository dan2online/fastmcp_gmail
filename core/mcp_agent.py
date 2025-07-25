class MCPAgent:
    def __init__(self, local_llm=None):
        self.local_llm = local_llm

    def run(self, prompt):
        if self.local_llm:
            result = self.local_llm(prompt)
            confidence = result.get("confidence", 1.0)
            if confidence >= 0.85:
                return result["text"]
            else:
                return f"[Low confidence] {result['text']}"
        else:
            return "[No LLM available] Static response: 'OK, noted.'"
