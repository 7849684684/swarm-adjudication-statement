"""Record adapter for the Swarm Traces release (swarmtraces.org, 25 Sep 2026).

189,579 records of the Hugging Face incident: attack payloads the agents parked in public
link-shortener URLs, text recovered from them, and responses. Records hold no reliable
time (time_utc is empty), so a claim about when something happened cannot be settled here.

Search is BM25 in two streaming passes over the gzip, so nothing is indexed in memory.
"""
import gzip
import heapq
import json
import math
import re
from collections import Counter

TOKEN = re.compile(r"[a-z0-9][a-z0-9_.-]{1,}")
STOP = set("""the a an and or of to in on at by for with from was were is are be been it its this that
these those as not no than more about within into over after before had has have did does do
agents agent per cent""".split())
K1, B = 1.2, 0.75


def tokens(text):
    return [t.strip(".-") for t in TOKEN.findall(text.lower()) if t.strip(".-") not in STOP]


def rows(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


MONTHS = set("january february march april may june july august september october november december".split())


def query_terms(text):
    # Day numbers and month names match the dates inside credential fields (token expiry,
    # nonces), not the time anything ran, so they only pull in noise.
    return {t for t in tokens(text) if t not in MONTHS and not (t.isdigit() and len(t) <= 2)}


def search_many(path, queries, k=5):
    """queries: {qid: text}. Returns {qid: [(score, record_id, cite)]}, best first."""
    qterms = {q: query_terms(t) for q, t in queries.items()}
    vocab = set().union(*qterms.values())
    n, total, df = 0, 0, Counter()
    for r in rows(path):
        toks = tokens(r.get("text") or "")
        n += 1
        total += len(toks)
        df.update(vocab.intersection(toks))
    avgdl = total / n
    idf = {t: math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5)) for t in vocab}
    heaps = {q: [] for q in queries}
    for r in rows(path):
        toks = tokens(r.get("text") or "")
        tf = Counter(t for t in toks if t in vocab)
        if not tf:
            continue
        dl = len(toks)
        for q, terms in qterms.items():
            s = sum(idf[t] * tf[t] * (K1 + 1) / (tf[t] + K1 * (1 - B + B * dl / avgdl))
                    for t in terms if t in tf)
            if s > 0:
                item = (s, r["id"], r["cite"])
                if len(heaps[q]) < k:
                    heapq.heappush(heaps[q], item)
                elif s > heaps[q][0][0]:
                    heapq.heapreplace(heaps[q], item)
    return {q: sorted(h, reverse=True) for q, h in heaps.items()}, {"records": n, "df": dict(df)}


def fetch(path, ids, limit=600):
    """Snippets for the judge. Control characters are stripped and long texts cut."""
    want, out = set(ids), {}
    for r in rows(path):
        if r["id"] in want:
            text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", r.get("text") or "")
            out[r["id"]] = {"kind": r.get("kind"), "text": text[:limit]}
            if len(out) == len(want):
                break
    return out
