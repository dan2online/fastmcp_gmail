import subprocess

def ollama_llm_streaming(prompt: str):
    try:
        process = subprocess.Popen(["ollama", "run", "llama3", prompt],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        print("🤖 [Streaming response]: ", end="", flush=True)
        output = []
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(line.strip(), end=" ", flush=True)
            output.append(line.strip())
        print()
        return {"text": " ".join(output), "confidence": 0.9}
    except Exception as e:
        return {"text": f"[Ollama error: {e}]", "confidence": 0.0}
