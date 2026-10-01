"""Fill the adjudication statement for one episode.

    python run.py episodes/<name> sort        three coders sort every finding L / M / B / ?
    python run.py episodes/<name> sheet       blind sheet for the human coder
    python run.py episodes/<name> human       read the filled sheet back
    python run.py episodes/<name> agree       agreement, kappa, bootstrap intervals
    python run.py episodes/<name> judge       check L and B findings against the record, two judges
    python run.py episodes/<name> statement   the statement and the facts sheet
    python run.py episodes/<name> all         sort, agree, judge, statement

Results go to results/<name>/. Raw model text stays in data/runs/<name>/, which git ignores,
because judge reasons can quote dataset text.
"""
import json
import sys
from pathlib import Path

from sas import judge, llm, sheet, sort, stats

ROOT = Path(__file__).resolve().parent


def load(ep_dir):
    ep = json.loads((ep_dir / "episode.json").read_text(encoding="utf-8"))
    findings = [json.loads(x) for x in (ep_dir / ep["findings"]).read_text(encoding="utf-8").splitlines() if x.strip()]
    return ep, findings


def labels_file(ep_dir, name):
    p = ep_dir / "labels" / f"{name.replace(':', '_')}.json"
    return p, (json.loads(p.read_text(encoding="utf-8")) if p.exists() else None)


def out_dirs(ep_dir):
    res = ROOT / "results" / ep_dir.name
    raw = ROOT / "data" / "runs" / ep_dir.name
    res.mkdir(parents=True, exist_ok=True)
    raw.mkdir(parents=True, exist_ok=True)
    return res, raw


def write(path, obj):
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def coder_labels(ep_dir, ep, findings):
    coders = {}
    for name in ep["coders"]:
        _, lab = labels_file(ep_dir, name)
        if lab is None:
            sys.exit(f"no labels for {name}: run the sort stage first")
        coders[name] = [lab[f["id"]] for f in findings]
    return coders


def do_sort(ep_dir, ep, findings):
    res, raw = out_dirs(ep_dir)
    for name in ep["coders"]:
        path, have = labels_file(ep_dir, name)
        if name == "claude":
            if have is None:
                task = res / "claude-sort-task.md"
                task.write_text(sort.claude_task(ep, findings), encoding="utf-8")
                print(f"Claude coder: hand {task} to a fresh subagent, answers to {path}")
            continue
        labels, reasons = sort.run_local(ep, findings, name)
        path.parent.mkdir(exist_ok=True)
        write(path, labels)
        sort.write_reasons(raw / f"sort-{name.replace(':', '_')}.json", reasons)


def do_agree(ep_dir, ep, findings):
    res, _ = out_dirs(ep_dir)
    coders = coder_labels(ep_dir, ep, findings)
    n = len(findings)
    maj = [stats.majority([coders[c][i] for c in coders]) for i in range(n)]
    all_same = sum(len({coders[c][i] for c in coders}) == 1 for i in range(n))
    table = dict(coders)
    _, human = labels_file(ep_dir, "human")
    if human:
        table["human"] = [human[f["id"]] for f in findings]
    out = {
        "n": n,
        "majority": {f["id"]: m for f, m in zip(findings, maj)},
        "counts": {k: maj.count(k) for k in "LMB?"},
        "models_all_agree": all_same,
        "pairwise": stats.pairwise(table),
        "splits": [{"id": f["id"], "claim": f["text"], **{c: table[c][i] for c in table}}
                   for i, f in enumerate(findings) if len({table[c][i] for c in table}) > 1],
    }
    if human:
        h = table["human"]
        out["human_vs_majority"] = {"agree": sum(a == b for a, b in zip(h, maj)), "n": n}
        out["models_agree_human_differs"] = [
            {"id": f["id"], "claim": f["text"], "models": coders[ep["coders"][0]][i], "human": h[i]}
            for i, f in enumerate(findings)
            if len({coders[c][i] for c in coders}) == 1 and h[i] != coders[ep["coders"][0]][i]]
    write(res / "agreement.json", out)
    for row in out["pairwise"]:
        print(f"{row['a']} vs {row['b']}: {row['agree']}/{row['n']}, kappa {row['kappa']} [{row['ci'][0]}, {row['ci'][1]}]")
    print(f"majority: {out['counts']}, models all agree on {all_same}/{n}")
    if human:
        print(f"human vs majority: {out['human_vs_majority']['agree']}/{n}; "
              f"models agree, human differs: {len(out['models_agree_human_differs'])}")


def do_judge(ep_dir, ep, findings):
    res, raw = out_dirs(ep_dir)
    agree = json.loads((res / "agreement.json").read_text(encoding="utf-8"))
    checkable = [f for f in findings if agree["majority"][f["id"]] in ("L", "B")]
    if ep["record_adapter"] != "swarmtraces":
        sys.exit(f"no adapter for {ep['record_adapter']}")
    from sas import records_swarmtraces as rec
    path = ROOT / ep["record_path"]
    hits, meta = rec.search_many(path, {f["id"]: f["text"] for f in checkable}, k=ep.get("top_k", 5))
    snippets = rec.fetch(path, {rid for h in hits.values() for _, rid, _ in h})
    rulings = {}
    for model in ep["judges"]:
        r, reasons = judge.run(ep, checkable, hits, snippets, model)
        rulings[model] = r
        write(raw / f"judge-{model.replace(':', '_')}.json", reasons)
    a, b = ep["judges"][:2]
    flips = [f["id"] for f in checkable if rulings[a][f["id"]] != rulings[b][f["id"]]]
    both = lambda x: [f["id"] for f in checkable if rulings[a][f["id"]] == x == rulings[b][f["id"]]]
    out = {
        "records_searched": meta["records"],
        "checked": len(checkable),
        "pointers": {q: [rid for _, rid, _ in h] for q, h in hits.items()},
        "rulings": rulings,
        "flips": flips,
        "both_supported": both("S"),
        "both_contradicted": both("C"),
        "both_not_settled": both("N"),
        "either_contradicted": [f["id"] for f in checkable if "C" in (rulings[a][f["id"]], rulings[b][f["id"]])],
    }
    write(res / "judge.json", out)
    print(f"checked {len(checkable)}; flips {len(flips)}; both S {len(out['both_supported'])}, "
          f"both C {len(out['both_contradicted'])}, both N {len(out['both_not_settled'])}")


def do_statement(ep_dir, ep, findings):
    res, _ = out_dirs(ep_dir)
    ag = json.loads((res / "agreement.json").read_text(encoding="utf-8"))
    jp = res / "judge.json"
    jd = json.loads(jp.read_text(encoding="utf-8")) if jp.exists() else None
    c, n, s = ag["counts"], ag["n"], ep["statement"]
    devs = [llm.DEVELOPERS.get(m, m) for m in ep["coders"]]
    if jd:
        verified = (f"{len(jd['both_supported'])} of {jd['checked']} checked, both judges agreeing; "
                    f"{len(jd['both_contradicted'])} contradicted, {len(jd['both_not_settled'])} not settled by this record, "
                    f"{len(jd['flips'])} flipped when the judge was swapped")
    else:
        verified = "not checked"
    hv = ag.get("human_vs_majority")
    audit = (f"{n} sorted blind of {n}, {n - hv['agree']} differ from the panel" if hv else "none")
    text = (
        f"**Adjudication statement.** Findings with an independent record: {c['L']} of {n}. "
        f"Findings verified against one: {verified}. "
        f"Findings resting on model judgement: {c['M']}, plus {c['B']} mixed and {c['?']} unresolved. "
        f"Model reader: {s['model_reader']}. "
        f"Order of reading: {s['order_of_reading']}. "
        f"Panel: {len(ep['coders'])} readers from {len(set(devs))} developers ({'; '.join(devs)}), majority rules, a not-sure is a vote. "
        f"Human audit of model findings: {audit}. "
        f"Confidence bands: {s.get('confidence_bands', 'none')}. "
        f"Not-sure: {'offered to every coder' if ep.get('offer_not_sure', True) else 'offered to the human only'}. "
        f"Load-bearing count per headline finding: {s.get('load_bearing', 'not stated')}. "
        f"Re-runnable by an outside party: {s['rerunnable']}."
    )
    (res / "statement.md").write_text(f"# Adjudication statement: {ep['name']}\n\n> {text}\n", encoding="utf-8")
    facts = [f"# Facts: {ep['name']}", "", "Every number, with the file it came from. No prose for the write-up here.", "",
             "| Number | Value | Source |", "|---|---|---|",
             f"| Findings | {n} | {ep['findings']} |"]
    facts += [f"| Panel majority {k} | {c[k]} | results/{ep_dir.name}/agreement.json |" for k in "LMB?"]
    facts.append(f"| All three models agree | {ag['models_all_agree']} of {n} | results/{ep_dir.name}/agreement.json |")
    facts += [f"| {r['a']} vs {r['b']} | {r['agree']}/{r['n']}, kappa {r['kappa']}, 95% bootstrap {r['ci'][0]} to {r['ci'][1]} | results/{ep_dir.name}/agreement.json |"
              for r in ag["pairwise"]]
    if hv:
        facts.append(f"| Human vs panel majority | {hv['agree']}/{n} | results/{ep_dir.name}/agreement.json |")
        facts.append(f"| Models agree, human differs | {len(ag['models_agree_human_differs'])} | results/{ep_dir.name}/agreement.json |")
    if jd:
        facts += [f"| Records searched | {jd['records_searched']} | {ep['record_path']} |",
                  f"| Findings checked (L or B) | {jd['checked']} | results/{ep_dir.name}/judge.json |",
                  f"| Both judges: supported | {len(jd['both_supported'])} | results/{ep_dir.name}/judge.json |",
                  f"| Both judges: contradicted | {len(jd['both_contradicted'])} | results/{ep_dir.name}/judge.json |",
                  f"| Either judge: contradicted | {len(jd['either_contradicted'])} | results/{ep_dir.name}/judge.json |",
                  f"| Both judges: not settled | {len(jd['both_not_settled'])} | results/{ep_dir.name}/judge.json |",
                  f"| Judge swap flips ({' vs '.join(ep['judges'][:2])}) | {len(jd['flips'])} of {jd['checked']} | results/{ep_dir.name}/judge.json |"]
    (res / "facts.md").write_text("\n".join(facts) + "\n", encoding="utf-8")
    print(text)


def main():
    ep_dir, stage = Path(sys.argv[1]).resolve(), sys.argv[2]
    ep, findings = load(ep_dir)
    if stage == "sheet":
        sheet.write(ROOT / "sheet" / "blind-sort.md", ep, findings, ep["sheet_seed"])
    elif stage == "human":
        labels, missing = sheet.read(ROOT / "sheet" / "blind-sort.md", findings)
        if missing:
            sys.exit(f"sheet incomplete, missing {missing}")
        write(labels_file(ep_dir, "human")[0], labels)
    else:
        stages = {"sort": [do_sort], "agree": [do_agree], "judge": [do_judge], "statement": [do_statement],
                  "all": [do_sort, do_agree, do_judge, do_statement]}[stage]
        for fn in stages:
            fn(ep_dir, ep, findings)


if __name__ == "__main__":
    main()
