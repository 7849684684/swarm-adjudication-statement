"""A count from the record for findings that state how many emails an agent sent.

The rule: count the email bodies an agent typed (a type action, or an xdotool type command)
whose first lines open with a salutation ("Dear", "Hi" or "Hello" and a capitalised name),
per agent per Pacific day. This counts composed bodies, not sends. Retries and drafts push
it up, and a body without a salutation is missed. A gap between it and the summary says
"check the screenshots", not "the summary is wrong".
"""
import gzip
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

SAL = re.compile(r"(?:^|[\"'\n])\s*(Dear|Hi|Hello)\s+[A-Z][\w.-]*[ ,]", re.M)
PT = ZoneInfo("America/Los_Angeles")


def pt_day(created_at):
    return datetime.fromisoformat(created_at[:19]).replace(tzinfo=timezone.utc).astimezone(PT).date().isoformat()


def typed_bodies(path):
    counts = defaultdict(Counter)
    for line in gzip.open(path, "rt", encoding="utf-8"):
        r = json.loads(line)
        a = r.get("action") or {}
        txt = str(a.get("text") or "") if a.get("action") == "type" else str(a.get("command") or "")
        if SAL.search(txt[:400]):
            counts[r["agent"]][pt_day(r["created_at"])] += 1
    return counts


def check(path, checks):
    """checks: [{id, agent, day, claimed, scope: 'day' | 'to_end_of_day'}]"""
    counts = typed_bodies(path)
    out = []
    for c in checks:
        days = counts.get(c["agent"], {})
        n = days.get(c["day"], 0) if c["scope"] == "day" else sum(v for d, v in days.items() if d <= c["day"])
        out.append({**c, "typed_bodies": n})
    return out, {a: dict(sorted(d.items())) for a, d in counts.items()}
