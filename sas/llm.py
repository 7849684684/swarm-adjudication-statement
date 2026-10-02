"""Local Ollama calls with an on-disk cache, so a re-run of any stage costs nothing."""
import base64
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


def chat(model, prompt, seed=7, images=None, think=None):
    """images: list of PNG bytes. think: None leaves the model default, False turns reasoning off."""
    opts = {"temperature": 0, "seed": seed}
    imgs = [base64.b64encode(b).decode() for b in (images or [])]
    key_parts = [model, prompt, opts, [hashlib.sha256(b).hexdigest() for b in (images or [])], think]
    # Old cache entries were keyed without the image and think parts, so keep that key for plain calls.
    key_src = [model, prompt, opts] if not imgs and think is None else key_parts
    key = hashlib.sha256(json.dumps(key_src).encode()).hexdigest()
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["text"]
    msg = {"role": "user", "content": prompt}
    if imgs:
        msg["images"] = imgs
    body = {"model": model, "messages": [msg], "stream": False, "options": opts}
    if think is not None:
        body["think"] = think
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        text = json.load(r)["message"]["content"]
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"model": model, "text": text}), encoding="utf-8")
    return text
