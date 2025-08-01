import json
from pathlib import Path
from core.llm_log import log_prompt_response

# Use cache directory for cache files
CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "llm_cache.json"


def load_cache():
    return json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}


def save_cache(cache):
    # Ensure parent directory exists
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
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
