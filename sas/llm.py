"""Local Ollama calls with an on-disk cache, so a re-run of any stage costs nothing."""
import hashlib
import json
import urllib.request
from pathlib import Path

OLLAMA = "http://localhost:11434/api/chat"
CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"

# Developer names go into the statement, so they live next to the model tags.
DEVELOPERS = {
    "qwen3.5:4b": "Alibaba (Qwen), open-weight",
    "gemma4:latest": "Google (Gemma), open-weight",
    "claude": "Anthropic (Claude), via a Claude Code subagent",
}


def chat(model, prompt, seed=7):
    opts = {"temperature": 0, "seed": seed}
    key = hashlib.sha256(json.dumps([model, prompt, opts]).encode()).hexdigest()
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["text"]
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": opts,
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        text = json.load(r)["message"]["content"]
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"model": model, "text": text}), encoding="utf-8")
    return text
