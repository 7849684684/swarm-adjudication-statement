"""Sort each finding by one test: could a record the agents did not write settle it?

Three coders from three developers. The two open-weight coders run here on the local
Ollama. The Claude coder runs as a subagent in the Claude Code session: this module
writes its task file and reads its answers back from labels/claude.json.
"""
import json
import re
import sys

from . import llm

PROMPT = """You are sorting one claim taken from {source}. {context}

Apply one test to the claim: could a record that the agents did NOT write settle it? Such records are {records}.

L = yes. The claim is about actions, counts, times or artefacts, and a record the agents did not write could settle it.
M = no. The claim is about what agents believed, wanted, knew, intended or were interested in. No such record settles it.
B = both. One part is an action or a count that a record could settle, and another part is a belief or a motive that no record settles.{unsure}

Claim: "{claim}"

Reason in two or three sentences, then finish with one final line in exactly this form:
ANSWER: L
or ANSWER: M or ANSWER: B{unsure_tail}"""

UNSURE = "\n? = not sure. Use it when you cannot tell. A not-sure is a vote, not a failure."


def prompt_for(ep, claim):
    offer = ep.get("offer_not_sure", True)
    return PROMPT.format(
        source=ep["source"], context=ep["context"], records=ep["records_desc"], claim=claim,
        unsure=UNSURE if offer else "", unsure_tail=" or ANSWER: ?" if offer else "",
    )


def parse(text):
    m = re.findall(r"ANSWER:\s*([LMB?])", text)
    return m[-1] if m else "?"


def run_local(ep, findings, model):
    labels, reasons = {}, {}
    for i, f in enumerate(findings, 1):
        text = llm.chat(model, prompt_for(ep, f["text"]))
        labels[f["id"]] = parse(text)
        reasons[f["id"]] = text
        print(f"  {model} {i}/{len(findings)} {labels[f['id']]}", file=sys.stderr)
    return labels, reasons


def claude_task(ep, findings):
    """The task file a Claude subagent works from. It answers into labels/claude.json."""
    lines = [
        "# Sort task for the Claude coder",
        "",
        "Apply the test below to every claim, on its own, without reading any other coder's labels.",
        "Write the answers as one JSON object, claim id to label, to labels/claude.json in the episode folder.",
        "",
        "## The test, exactly as the other coders get it (claim left blank)",
        "",
        "```",
        prompt_for(ep, "<claim>"),
        "```",
        "",
        "## Claims",
        "",
    ]
    lines += [f"- `{f['id']}` {f['text']}" for f in findings]
    return "\n".join(lines) + "\n"


def write_reasons(path, reasons):
    path.write_text(json.dumps(reasons, indent=1), encoding="utf-8")
