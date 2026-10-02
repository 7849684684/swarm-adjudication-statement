"""Record adapter for the AI Village dataset (AI Digest, aidigestorg/ai-village).

The independent record is what the computer did: each computer-use turn's executed action,
its tool output and error, its server timestamp, and its screenshot. The agents' own
messages and reasoning (agent_messages) are left out of the searchable text, because the
agents wrote them. The chat log is kept as a separate record of what was said, not of
what was done.

extract() streams the 2.5 GB turns file once and writes one episode's turns to a small
gzip, so search and fetch never touch the big file again.
"""
import gzip
import heapq
import json
import math
import re
import tarfile
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

from .records_swarmtraces import query_terms, tokens, K1, B


def extract(src_dir, out_path, start, end):
    src = Path(src_dir)
    agents = {a["id"]: a for a in map(json.loads, gzip.open(src / "agents.jsonl.gz", "rt"))}
    sess = {s["id"]: s for s in map(json.loads, gzip.open(src / "computer_use_sessions.jsonl.gz", "rt"))}
    d0, d1 = date.fromisoformat(start[:10]), date.fromisoformat(end[:10])
    # Cheap substring prefilter on the day strings, then an exact check on created_at.
    days = [f'"{d0 + timedelta(i)} ' for i in range((d1 - d0).days + 1)]
    n = 0
    with gzip.open(out_path, "wt", encoding="utf-8") as out:
        for line in gzip.open(src / "computer_use_turns.jsonl.gz", "rt", encoding="utf-8"):
            if not any(d in line for d in days):
                continue
            t = json.loads(line)
            if not (start <= t["created_at"] <= end):
                continue
            s = sess.get(t["session_id"])
            agent = agents.get(s["agent_id"], {}) if s else {}
            out.write(json.dumps({
                "id": t["id"], "session_id": t["session_id"], "created_at": t["created_at"],
                "agent": agent.get("name"), "model": agent.get("model_string"),
                "action": t.get("agent_action"), "output": (t.get("output") or "")[:4000],
                "error": (t.get("error") or "")[:1000], "redacted": t.get("screenshot_is_redacted"),
            }) + "\n")
            n += 1
    return n


def rows(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def record_text(r):
    a = r.get("action") or {}
    return " ".join(str(v) for v in a.values()) + " " + (r.get("output") or "") + " " + (r.get("error") or "")


def search_many(path, queries, k=8):
    qterms = {q: query_terms(t) for q, t in queries.items()}
    vocab = set().union(*qterms.values())
    n, total, df = 0, 0, Counter()
    for r in rows(path):
        toks = tokens(record_text(r))
        n += 1
        total += len(toks)
        df.update(vocab.intersection(toks))
    avgdl = total / max(n, 1)
    idf = {t: math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5)) for t in vocab}
    heaps = {q: [] for q in queries}
    for r in rows(path):
        toks = tokens(record_text(r))
        tf = Counter(t for t in toks if t in vocab)
        if not tf:
            continue
        dl = len(toks)
        for q, terms in qterms.items():
            s = sum(idf[t] * tf[t] * (K1 + 1) / (tf[t] + K1 * (1 - B + B * dl / avgdl))
                    for t in terms if t in tf)
            if s > 0:
                item = (s, r["id"], f"{r['id'][:8]} {r['created_at'][:16]} UTC {r.get('agent')}")
                if len(heaps[q]) < k:
                    heapq.heappush(heaps[q], item)
                elif s > heaps[q][0][0]:
                    heapq.heapreplace(heaps[q], item)
    return {q: sorted(h, reverse=True) for q, h in heaps.items()}, {"records": n, "df": dict(df)}


def fetch(path, ids, limit=700):
    want, out = set(ids), {}
    for r in rows(path):
        if r["id"] in want:
            text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", record_text(r))
            out[r["id"]] = {"kind": f"computer-use turn by {r.get('agent')} at {r['created_at'][:19]} UTC",
                            "text": text[:limit], "created_at": r["created_at"]}
            if len(out) == len(want):
                break
    return out


_TARS = {}


def screenshot(tar_dir, turn_id, created_at_utc):
    """The PNG bytes for one turn, or None. Tars are named by the Pacific date of created_at."""
    utc = datetime.fromisoformat(created_at_utc[:19]).replace(tzinfo=timezone.utc)
    day = utc.astimezone(ZoneInfo("America/Los_Angeles")).date().isoformat()
    tp = Path(tar_dir) / f"{day}.tar"
    if not tp.exists():
        return None
    if tp not in _TARS:
        tf = tarfile.open(tp)
        _TARS[tp] = (tf, set(tf.getnames()))
    tf, names = _TARS[tp]
    name = f"{turn_id}.png"
    return tf.extractfile(name).read() if name in names else None
