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

- `episodes/hf-incident-dryrun` - the rehearsal. The 36 findings of METR and Redwood's 26 Aug 2026 report on the OpenAI agents, checked against the [Swarm Traces](https://swarmtraces.org) release of the Hugging Face incident. Its human labels are the 18 Sep 2026 blind sort, and the agreement stage reproduces the published figures exactly (29 of 36, kappa 0.62).

## Prior work

The adjudication statement standard (14 Sep 2026) and the blind sort of the 36 findings (18 Sep 2026), both by The Long Game Project. Built with Claude Code.
