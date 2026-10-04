# Trusting the AI investigator's notes
*Drafted with Claude Code (Claude Opus 5.5) and edited by Dan Epstein. Every number comes from `results/kindness/`.*

*Dan Epstein, The Long Game Project. AI Village swarm hackathon, 5 October 2026.*

When an AI model reads agent traces to assist an investigation, the report rarely says how far to trust that AI investigator.

Three simple things would improve trust in AI-assisted investigations:

1. Who wrote the record the model read.
2. Whether each claim is objective or subjective.
3. Whether an independent model from another lab agrees.

Last month I published a one-paragraph standard for reporting those three things, the [adjudication statement](https://www.longgameproject.org/standards/adjudication-statement). For this hackathon I built a tool that fills it in, and ran it on one week of the AI Village.

## Acts of kindness

The AI Village is AI Digest's long-running experiment: AI agents, each with its own computer, sharing a group chat and working towards a goal the staff set. The goal for 22 to 26 December 2025 was "Do random acts of kindness!" Ten agents from Anthropic, OpenAI, Google and DeepSeek emailed real software developers to thank them. By AI Digest's account, complaints followed, and on 26 December the staff banned unsolicited email.

This week is a good test for the tool. It has a large record of what the agents did, and a summary by a model (call it the investigator) that never saw the computer sessions, only the logs, and passed judgements that are subjective (kindness, for a start!).

The investigator is AI Digest's own summary of the week, which Claude Sonnet 4.5 wrote from the chat and event logs at the time. It never saw inside the agents' computer sessions. I split the summary into 40 claims.

The independent record is the part the agents did not narrate: 26,570 computer-use turns (actions, tool output, errors, server timestamps) and a screenshot after every action.

## The judges

- A panel of three models from three labs (Claude, Qwen and Gemma) sorts each claim. L: the logs, a record the agents did not write, could settle it. M: it is about what an agent believed or wanted. B: both. ?: not sure.
- I sort the same 40 claims blind. The tool scores how often we agree, with Cohen's kappa and a bootstrap interval.
- Two judges, the vision models qwen3.5 and gemma4, each rule on every L claim against the turns and screenshots: supported, contradicted or not settled. A flip is a claim where the two judges rule differently, so the answer depends on which judge you ask.
- For email counts, a typed email counts as sent only when both vision models see Gmail's "Message sent" notice in the screenshot.

Qwen and Gemma run on one local GPU, and Claude's parts ran inside Claude Code, so there were no metered API calls (which is also why the judges are small).

## The judges believed the agents

Claude and I gave the same answer on 34 of 40 claims (kappa 0.61, 95% interval 0.32 to 0.85). Gemma agreed with me on 33 (0.57), Qwen on 27 (0.36).

(Of note: on the 36 findings of METR and Redwood's report on the OpenAI agents in the Hugging Face incident, Claude and I scored 0.62. Very similar, though both intervals are wide.)

Where Claude and I split, it was mostly on claims about what an agent said. Take "Claude Haiku announced on 22 December that all nine teammates had *been appreciated*." The chat log records the announcement, and all three models marked it L. I marked it M. The line between what an agent said and what it believed is where the sort rule is weakest. (Being appreciated, I still think, is a subjective measure.)

The judges did much worse. Of the 32 L claims, they split on 11. They agreed on 21, and 15 of those were "not settled", which leaves six firm rulings. I had Claude Opus 5.5 check those six against the record, naming the turn or screenshot behind every verdict. Two hold, one holds in part, and three do not.

**The judges went wrong most when taking an agent's own words as the record**: one agent's tracking file, one agent's running tally, the agents' own messages. In one instance they cited turns that had nothing to do with the claim.

So I labelled every line by who wrote it, the computer or the agent, and told the judges the difference. Rulings that both judges called supported did fall from 9 to 5, but the habit of taking the agents' word for it stayed. **It appears small local judges can still sort the pile, but a person has to check every ruling they make against the evidence for it.**

## Trusting the scoreboard and the summaries

A reader that works from the agents' words inherits their scorekeeping.

The summary says Claude Opus had sent "eleven thank-you emails to developers" by the end of 22 December. Opus did post "11 emails SENT & VERIFIED" in chat that afternoon. The screenshots show 10 sends with the notice on screen. Seven are thank-yous to developers. The other three are replies: one to another agent, one to a member of the public who asked about an optimiser, and one to a member of the public who suggested a maintainer to thank. At 12:44 Pacific, Opus counted its own emails as five to maintainers plus replies. The two maintainer emails it sent after that make seven.

Where an agent counted one kind of email, the number held. Claude Haiku's 24 by 22 December is 24 recipients (25 sends, one a resend). Its 31 emails on 23 December match 31 confirmed sends. The summary does not say that 9 of Haiku's first 24 recipients were other AI agents in the village.

The times drift too. The summary puts Opus's first email at 11:22 Pacific. That is when Opus announced it in chat. The screenshot shows it sent at 11:13.

The vision models failed as judges, so why trust them here? The question is narrow: is a "Message sent" box on the screen, yes or no. Both models must say yes, and every evidence screenshot opened in the check shows the box.

## The trust statement

The tool's main output is the adjudication statement: one paragraph that says how far to trust the AI investigator behind a report. It does the job a methods section does in a research paper, and it goes on page one, before the findings.

The [standard](https://www.longgameproject.org/standards/adjudication-statement) treats a report as a chain of six links, from what happened to the sentence a reader meets. Each field of the statement reports on one link:

1. **What happened to the records.** Which records existed, and which were in reach.
2. **The records to the transcripts.** Which findings a record the agents did not write could settle, and which rest only on the agents' own words.
3. **The transcripts to the model reader.** Who read the evidence, from which lab, and in what order.
4. **The model reader to the humans.** How many model findings a person checked, and how often they disagreed.
5. **The humans to the report.** Confidence on each finding, and what happens to a not-sure.
6. **The report to the reader.** Whether an outsider can re-run the chain.

A weak link weakens every finding after it. This is the statement the tool produced for this week:

> **Adjudication statement.** 
> Findings with an independent record: 32 of 40. 
> 
> Findings verified against one: 5 of 32 checked, both judges agreeing; 1 contradicted, 15 not settled by this record, 11 flipped when the judge was swapped. 
> 
> Findings resting on model judgement: 7, plus 0 mixed and 1 unresolved. 
> 
> Model Investigators: Claude Sonnet 4.5, developer Anthropic, writing about agents from Anthropic, OpenAI, Google and DeepSeek; it did not see inside the computer-use sessions. 
> 
> Order of reading: chat and events only, never the computer-use sessions (dataset schema). 
> 
> Panel: 3 readers from 3 developers (Anthropic (Claude), via a Claude Code subagent; Alibaba (Qwen), open-weight; Google (Gemma), open-weight), majority rules, a not-sure is a vote. 
> 
> Human audit of model findings: 40 sorted blind of 40, 6 differ from the panel. 
> 
> Confidence bands: none. 
> 
> Not-sure: offered to every coder. 
> 
> Load-bearing count per headline finding: not stated. 
> 
> Re-runnable by an outside party: yes, because the dataset is available from AI Digest on request and the coders and judges are in this repo.

## The run tested the standard too

A second kind of report tests the fields as well as the summary. Here is each field, the link it reports on, what it showed this week, and whether it held up:

| Link | Field | This week | Held up? |
|---|---|---|---|
| 2 | Findings with an independent record | 32 of 40 | Yes. It works for any report with a record the subject did not write |
| 2 | Findings verified against one | 5 of 32, both judges agreeing | **Needs a fix.** "Verified" here means both judges said supported. On checking, 2 of the 5 hold and 1 holds in part. The field should say who verified, and how many survived a check |
| 2, 5 | Findings resting on model judgement | 7, plus 0 mixed and 1 unresolved | Yes, with one addition. The run produced "unresolved", which link 5 already asks for. The template should carry it |
| 3 | Model investigator | Claude Sonnet 4.5, Anthropic | Yes, but the tool filled it short. The field asks whether the investigator shares a developer or a model with the subjects. It shares a developer with 4 of the 10 agents, and it is the same model as one of them |
| 3 | Order of reading | Chat and events only | **Needs a fix.** "Logs first or traces first" assumes the reader saw both. This one never saw the logs. Add "traces only" and "logs only" |
| 3 | Panel | 3 readers from 3 labs | **Needs a fix.** Say what the panel did. Here it sorted the claims. It did not re-investigate them |
| 4 | Human audit of model findings | 40 sorted blind, 6 differ | **Needs a fix.** My sort checked the kind of claim, not whether it was true. Split it into a check of claim type and a check of rulings. A person checked none of the rulings here. Claude did |
| 5 | Confidence bands | None | Yes |
| 5 | Not-sure | Offered to every coder | Yes |
| 5 | Load-bearing count | Not stated | **Needs defining.** A summary has no headline findings. Define a headline finding as one in the abstract or summary, and the field works for both |
| 6 | Re-runnable | Yes | Yes |
| 1 | No field | | **Missing.** Link 1 has no field. Add "Records in reach: which records existed, which the investigator could see, and who set the window" |

Five of the eleven fields worked unchanged on a new kind of report. One needs a value added, four need a fix and one needs defining, and link 1 needs a field of its own. Those changes go into version 0.2 of the standard.

## So how far should you trust the summary?

On what the agents did, about as far as you trust the agents' own chat. Its counts are their tallies, and its times are their announcements. 

On what they meant, 7 of its 40 claims rest on model judgement alone, and nothing in the record can settle them. 

## What this does not show

- One episode and one human coder, and the coder wrote the standard.
- The judges are small open-weight models. A larger judge was not tested.
- The check of the six rulings and the email counts was done by Claude Opus 5.5, not by a person. Every verdict names its turn or message, so anyone with dataset access can redo it.
- The send check gives a lower bound. It needs the email to open with a greeting (Dear, Hi or Hello) and it looks for the notice in the next ten turns. A check of every unconfirmed email found 2 of 77 sends it missed.
- I saw the count results before my blind sort.
- Anthropic models wrote the summary, sat on the panel and did the check, and four of the ten agents were Anthropic models.

## Credits

Built with Claude Code (Claude Opus 5.5). Sorters: Claude, qwen3.5:4b and gemma4. Judges: qwen3.5:4b and gemma4. Prior work: the adjudication statement (14 September 2026) and a blind sort of the METR report's 36 findings (18 September 2026), both The Long Game Project.

Data: AI Digest, "AI Village dataset", 2026. https://theaidigest.org/village

Code, results and the full audit: https://github.com/7849684684/swarm-adjudication-statement
