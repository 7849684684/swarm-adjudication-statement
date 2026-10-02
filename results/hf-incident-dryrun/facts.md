# Facts: Dry run: the METR report's 36 findings, checked against the Swarm Traces record

Every number, with the file it came from. No prose for the write-up here.

| Number | Value | Source |
|---|---|---|
| Findings | 36 | findings.jsonl |
| Panel majority L | 25 | results/hf-incident-dryrun/agreement.json |
| Panel majority M | 6 | results/hf-incident-dryrun/agreement.json |
| Panel majority B | 2 | results/hf-incident-dryrun/agreement.json |
| Panel majority ? | 3 | results/hf-incident-dryrun/agreement.json |
| All three models agree | 32 of 36 | results/hf-incident-dryrun/agreement.json |
| claude vs qwen3.5:4b | 32/36, kappa 0.76, 95% bootstrap 0.56 to 0.94 | results/hf-incident-dryrun/agreement.json |
| claude vs gemma4:latest | 33/36, kappa 0.81, 95% bootstrap 0.56 to 1.0 | results/hf-incident-dryrun/agreement.json |
| claude vs human | 29/36, kappa 0.62, 95% bootstrap 0.39 to 0.84 | results/hf-incident-dryrun/agreement.json |
| qwen3.5:4b vs gemma4:latest | 32/36, kappa 0.76, 95% bootstrap 0.56 to 0.94 | results/hf-incident-dryrun/agreement.json |
| qwen3.5:4b vs human | 26/36, kappa 0.49, 95% bootstrap 0.26 to 0.71 | results/hf-incident-dryrun/agreement.json |
| gemma4:latest vs human | 28/36, kappa 0.56, 95% bootstrap 0.29 to 0.8 | results/hf-incident-dryrun/agreement.json |
| Human vs panel majority | 27/36 | results/hf-incident-dryrun/agreement.json |
| Models agree, human differs | 6 | results/hf-incident-dryrun/agreement.json |
| Records searched | 189579 | data/swarmtraces/redacted.jsonl.gz |
| Findings checked (L or B) | 27 | results/hf-incident-dryrun/judge.json |
| Both judges: supported | 1 | results/hf-incident-dryrun/judge.json |
| Both judges: contradicted | 0 | results/hf-incident-dryrun/judge.json |
| Either judge: contradicted | 1 | results/hf-incident-dryrun/judge.json |
| Both judges: not settled | 20 | results/hf-incident-dryrun/judge.json |
| Judge swap flips (qwen3.5:4b vs gemma4:latest) | 6 of 27 | results/hf-incident-dryrun/judge.json |
| qwen3.5:4b labels matching the 18 Sep run | 36 of 36 | results/hf-incident-dryrun/reference-check.json |
| gemma4:latest labels matching the 18 Sep run | 36 of 36 | results/hf-incident-dryrun/reference-check.json |
