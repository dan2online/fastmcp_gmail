import json
from pathlib import Path
from core.llm_log import log_prompt_response

CACHE_FILE = Path("llm_cache.json")

def load_cache():
    return json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}

def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def cached_llm(prompt, llm_func):
    cache = load_cache()
    if prompt in cache:
        print("🧠 Using cached response.")
        return cache[prompt]
    result = llm_func(prompt)
    cache[prompt] = result
    save_cache(cache)
    log_prompt_response(prompt, result["text"])
    return result
