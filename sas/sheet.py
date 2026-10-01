"""The blind sheet for the human coder, and the parser that reads it back.

Claims are shuffled with a fixed seed and carry no coder labels. The sheet is scored
by claim text, so the shuffle key never has to be shown to the human.
"""
import random
import re

HEAD = """# Blind sort: {n} claims

About {mins} minutes. **Do not open the results/ folder or any labels file first.** The point is a sort made without seeing the models' sort.

The claims are {what}, shuffled with a fixed seed. An agent scores the sheet by matching on the claim text.

## The one test

Could a record that the agents did **not** write settle the claim? {records_cap}.

- **L** - yes. An action, a count, a time or an artefact, and such a record could settle it.
- **M** - no. It is about what agents believed, wanted, knew, intended or were interested in.
- **B** - both. One part a record could settle, one part it could not.
- **?** - not sure. Use it. A not-sure is a vote.

Write one letter in the third column. A note is optional.

| # | Claim | L / M / B / ? | Note |
|---|---|---|---|
"""


def write(path, ep, findings, seed):
    order = list(range(len(findings)))
    random.Random(seed).shuffle(order)
    rd = ep["records_desc"]
    out = HEAD.format(n=len(findings), mins=max(10, len(findings) // 2), what=ep["sheet_what"],
                      records_cap=rd[0].upper() + rd[1:])
    for k, i in enumerate(order, 1):
        out += f"| {k} | {findings[i]['text']} |  |  |\n"
    path.write_text(out, encoding="utf-8")


def read(path, findings):
    by_text = {f["text"].strip(): f["id"] for f in findings}
    labels = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].isdigit():
            continue
        cid = by_text.get(cells[1])
        lab = cells[2].upper()[:1]
        if cid and re.fullmatch(r"[LMB?]", lab):
            labels[cid] = lab
    missing = [f["id"] for f in findings if f["id"] not in labels]
    return labels, missing
