"""Agreement between coders: raw agreement, Cohen's kappa, and a bootstrap interval.

The bootstrap resamples claims, the unit that was coded. With 20 to 40 claims the
interval is wide, and it should be reported that way.
"""
import random
from collections import Counter

DRAWS = 10000
SEED = 20261004


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    k = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return po, k


def kappa_interval(a, b, draws=DRAWS, seed=SEED):
    rng = random.Random(seed)
    n = len(a)
    ks = []
    for _ in range(draws):
        idx = [rng.randrange(n) for _ in range(n)]
        aa, bb = [a[i] for i in idx], [b[i] for i in idx]
        # A resample where both coders used one label everywhere has no defined kappa.
        if len(set(aa) | set(bb)) == 1:
            continue
        ks.append(kappa(aa, bb)[1])
    ks.sort()
    return ks[int(0.025 * len(ks))], ks[int(0.975 * len(ks)) - 1]


def majority(labels):
    """Majority of the coders. Not-sure counts as a vote, so two not-sures make the claim unresolved."""
    c = Counter(labels)
    top, n = c.most_common(1)[0]
    if n * 2 <= len(labels):
        return "?"
    return top


def pairwise(coders):
    """coders: {name: [labels in claim order]} -> list of rows."""
    names = list(coders)
    rows = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            po, k = kappa(coders[a], coders[b])
            lo, hi = kappa_interval(coders[a], coders[b])
            n = len(coders[a])
            rows.append({"a": a, "b": b, "agree": round(po * n), "n": n,
                         "kappa": round(k, 2), "ci": [round(lo, 2), round(hi, 2)]})
    return rows
