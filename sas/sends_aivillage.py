"""Confirmed sends: a typed email body followed by Gmail's "Message sent" notice on screen.

For each body counted by counts_aivillage (same salutation rule), look at the same agent's
next turns, up to WINDOW or its next typed body, and ask a vision model whether the
screenshot shows the notice. The first model to say yes is confirmed by a second model from
another developer. A body counts as sent only when both say yes on the same screenshot.
This misses sends with no salutation and sends whose notice fell outside the window, so it
is a lower bound.
"""
import json
import sys
from collections import defaultdict

from . import llm
from .counts_aivillage import SAL, pt_day
from .records_aivillage import rows, screenshot

WINDOW = 10
Q = ("This is a screenshot of an AI agent's computer. Is there a small Gmail notice that says "
     "\"Message sent\" anywhere on the screen? Answer with one word: YES or NO.")


def is_body(r):
    a = r.get("action") or {}
    txt = str(a.get("text") or "") if a.get("action") == "type" else str(a.get("command") or "")
    return bool(SAL.search(txt[:400]))


def yes(model, png):
    return llm.chat(model, Q, images=[png], think=False).strip().upper().startswith("YES")


def check(path, tar_dir, checks, first="qwen3.5:4b", second="gemma4:latest"):
    want = {(c["agent"], c["day"], c["scope"]) for c in checks}
    agents = {c["agent"] for c in checks}
    turns = defaultdict(list)
    for r in rows(path):
        if r["agent"] in agents:
            turns[r["agent"]].append(r)
    for a in turns:
        turns[a].sort(key=lambda r: r["created_at"])
    out = []
    for c in checks:
        seq = turns[c["agent"]]
        in_scope = (lambda d: d == c["day"]) if c["scope"] == "day" else (lambda d: d <= c["day"])
        bodies, sent, evidence = 0, 0, []
        for i, r in enumerate(seq):
            if not (is_body(r) and in_scope(pt_day(r["created_at"]))):
                continue
            bodies += 1
            for nxt in seq[i + 1:i + 1 + WINDOW]:
                if is_body(nxt):
                    break
                png = screenshot(tar_dir, nxt["id"], nxt["created_at"])
                if png and yes(first, png):
                    if yes(second, png):
                        sent += 1
                        evidence.append(nxt["id"])
                    break
            print(f"  {c['id']} body {bodies}: sent so far {sent}", file=sys.stderr)
        out.append({**c, "typed_bodies": bodies, "confirmed_sends": sent, "evidence_turns": evidence})
    return out
