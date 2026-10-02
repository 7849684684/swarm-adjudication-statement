# swarm-adjudication-statement

Fills the adjudication statement for one episode of agent activity. The statement is a one-page reporting standard for investigations where a model reads the evidence ([the standard](https://www.longgameproject.org/standards/adjudication-statement), The Long Game Project, 14 Sep 2026).

Given findings that a model reader wrote about what agents did, it:

1. Sorts every finding three times, by three readers from three developers, on one test: could a record the agents did not write settle it? L yes, M no (belief, intent, motive), B both, ? not sure.
2. Writes a blind sheet so a human can sort the same findings without seeing the models' labels, then scores agreement: raw agreement, Cohen's kappa and a bootstrap interval, plus the findings where the models agree and the human does not.
3. Checks each L and B finding against the independent record with two judges from two developers, and counts the flips when the judge is swapped and the findings the record contradicts.
4. Fills every field of the statement, and writes a facts sheet with every number and the file it came from.

## Run

Python 3, standard library only. The local readers need [Ollama](https://ollama.com) with `qwen3.5:4b` and `gemma4:latest`.

```bash
python run.py episodes/hf-incident-dryrun all
```

Stages one at a time: `sort`, `sheet`, `human` (reads the filled sheet back), `agree`, `judge`, `statement`. Results land in `results/<episode>/`. Raw model text and dataset copies stay in `data/`, which git ignores.

## Readers

| Reader | Developer | Where it runs |
|---|---|---|
| Claude | Anthropic | a Claude Code subagent, answers saved to `labels/claude.json` |
| qwen3.5:4b | Alibaba, open-weight | local Ollama |
| gemma4:latest | Google, open-weight | local Ollama |

Temperature 0 and a fixed seed, and every call is cached on disk, so a re-run reproduces the labels.

## Episodes

- `episodes/kindness` - the entry. AI Village, 22 to 26 December 2025, goal "Do random acts of kindness!". The findings under test are the 40 claims in AI Digest's goal summary for the week, written by Claude Sonnet 4.5 without seeing inside the computer-use sessions. The record is that week's 26,570 computer-use turns (actions, tool output, errors, server timestamps) and their screenshots. Findings that state an email count also get a count from the record (`sas/counts_aivillage.py`, rule in its docstring).
- `episodes/hf-incident-dryrun` - the rehearsal. The 36 findings of METR and Redwood's 26 Aug 2026 report on the OpenAI agents, checked against the [Swarm Traces](https://swarmtraces.org) release of the Hugging Face incident. Its human labels are the 18 Sep 2026 blind sort, and the agreement stage reproduces the published figures exactly (29 of 36, kappa 0.62).

## Data

The AI Village dataset is AI Digest's, released for research on request: AI Digest, "AI Village dataset", 2026. https://theaidigest.org/village. No dataset file is in this repo. `episodes/kindness/findings.jsonl` restates the claims of one summary that AI Digest also publishes on its site, with private individuals replaced by their role. Download it to `data/aivillage/` with the Hugging Face CLI after access is granted. The Swarm Traces release is at https://swarmtraces.org.

## Prior work

The adjudication statement standard (14 Sep 2026) and the blind sort of the 36 findings (18 Sep 2026), both by The Long Game Project. Built with Claude Code.
