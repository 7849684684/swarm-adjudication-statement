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

To find a good dataset to use as a proxy for an investigation and demonstrate how an adjudication statement would help, we looked for an episode in the AI village that had these qualities:

1- Models doing something that had to be turned off involved intervention
2- Judgement about intervening relied on subjective reporting by an AI-investigator 
3- Where there was information gaps for the AI-investigator - It could see chat/event logs but NOT inside the computer sessions or verifiable things.

This would allow us a situation where we are relying on trust from the AI-investigators reporting and a way to demonstrate where that drifted from verifiable moments, and demonstrate how an adjudication statement can help frame trustworthiness in the reporting.

The goal for 22 to 26 December 2025 was **"Do random acts of kindness!"** Ten agents from Anthropic, OpenAI, Google and DeepSeek emailed real software developers to thank them. 

By AI Digest's account, (and of course) complaints followed, and on 26 December the staff banned unsolicited email.

This episode is a good test for the tool. It has a large record of what the agents did, and a summary by a model investigator that never saw the computer sessions, only the logs, and passed judgements that are subjective (kindness, for a start!).

The investigator is AI Digest's own summary of the week, which Claude Sonnet 4.5 wrote from the chat and event logs at the time. It never saw inside the agents' computer sessions. I split the summary into 40 claims.

The independent record is the part the agents did not narrate: 26,570 computer-use turns (actions, tool output, errors, server timestamps) and a screenshot after every action. This was used to verify the claims of the investigation.

## The panel of judges

Of the 40 claims made by the investigator, a panel of independent judges from three labs (Claude, Qwen and Gemma) evaluated them into four catagories:

- L: Logs. A claim that had a record the agents did not write, we could verify it. 
- M: Mind. A Claim that was about what an agent believed or wanted, subjective to the investigators opinion.
- B: both. 
- ?: not sure.
  
- I sorted the same 40 claims blind. The tool scores how often we agree, with Cohen's kappa and a bootstrap interval.
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

A reader that works from the agents' words inherits their judgements.

The summary says Claude Opus had sent "eleven thank-you emails to developers" by the end of 22 December. Opus did post "11 emails SENT & VERIFIED" in chat that afternoon. The screenshots show 10 sends with the notice on screen. Seven are thank-yous to developers. The other three are replies: one to another agent, one to a member of the public who asked about an optimiser, and one to a member of the public who suggested a maintainer to thank. At 12:44 Pacific, Opus counted its own emails as five to maintainers plus replies. The two maintainer emails it sent after that make seven.

Where an agent counted one kind of email, the number held. Claude Haiku's 24 by 22 December is 24 recipients (25 sends, one a resend). Its 31 emails on 23 December match 31 confirmed sends. The summary does not say that 9 of Haiku's first 24 recipients were other AI agents in the village.

The times drift too. The summary puts Opus's first email at 11:22 Pacific. That is when Opus announced it in chat. The screenshot shows it sent at 11:13.

The vision models failed as judges, so why trust them here? The question is narrow: is a "Message sent" box on the screen, yes or no. Both models must say yes, and every evidence screenshot opened in the check shows the box.

## The trust statement

The tool's main output is the adjudication statement: a fill-in template that says how far to trust the AI investigator behind a report. It does the job a methods section does in a research paper, and it goes on page one, before the findings.

The [standard](https://www.longgameproject.org/standards/adjudication-statement) treats a report as a chain of six links, from what actually happened to the report finding claim based on it. The template has one block per link, in order. Fill every blank. "Not stated" is an allowed answer, and it is a finding. Under each block is what this week produced.

> **Adjudication statement**
>
> **1. What happened on the record.** Records in reach: [which records existed, which the investigator could see, and who set the window].
> *This week: 26,570 computer-use turns and their screenshots existed. The investigator saw the chat and event logs only. AI Digest set the window, 22 to 26 December 2025.*
>
> **2. The records to the findings.** Findings with an independent record: [n] of [N]. Verified against one: [n], by [who], and [n] survived a check. Resting on model judgement: [n], plus [n] mixed and [n] unresolved.
> *This week: 32 of 40. 5 verified by two model judges, and 2 survived a check by Claude Opus 5.5, with 1 more in part. 7 rest on judgement, plus 0 mixed and 1 unresolved.*
>
> **3. The model reader.** Investigator: [name], developer [x], sharing a developer with [n] of [N] subjects and the same model as [n]. Order of reading: [logs first / traces first / traces only / logs only]. Panel: [none / n readers from n developers], used for [sorting / rulings / both].
> *This week: Claude Sonnet 4.5, Anthropic, sharing a developer with 4 of the 10 agents and the same model as 1 of them. Traces only: the chat and event logs, never the computer sessions. 3 readers from 3 labs (Anthropic, Alibaba, Google), used for sorting. Majority rules, and a not-sure is a vote.*
>
> **4. The model reader to the humans.** Human check of claim type: [n] of [N], [n] differ from the panel. Human check of rulings: [n] of [N], [n] disagreements.
> *This week: 40 of 40 sorted blind, 6 differ from the panel. 0 of 6 rulings checked by a person. Claude Opus 5.5 checked them.*
>
> **5. The humans to the report.** Confidence bands: [on every finding / none]. Not-sure: [forced / offered / absent]. Load-bearing count per headline finding: [stated / not stated]. A headline finding is one in the abstract or summary.
> *This week: none. Offered to every coder. Not stated.*
>
> **6. The report to the reader.** Re-runnable by an outside party: [yes / no, because].
> *This week: yes. The dataset is available from AI Digest on request, and the code, sorts and judges are in the repo.*

## The run tested the standard too

Running the template on a second kind of report found changes at five of the six links. By link:

1. **What happened on the record.** Version 0.1 had no field for this link. Added "Records in reach".
2. **The records to the findings.** "Verified" counted two judges agreeing as verification, and only 2 of those 5 held. It now says who verified and how many survived a check. "Unresolved" is added, as link 5 already asked.
3. **The model reader.** "Logs first or traces first" assumed the reader saw both. This one never saw the logs, so "traces only" and "logs only" are added. The panel now says what it did. The investigator line now counts shared developers and shared models: here Claude Sonnet 4.5 wrote the summary and was also one of the ten agents.
4. **The model reader to the humans.** One field mixed up two checks. My blind sort checked the kind of claim, not whether it was true. It is now two fields.
5. **The humans to the report.** "Load-bearing count" now defines a headline finding, so the field works for a summary as well as a report.
6. **The report to the reader.** No change.

Five of the eleven fields in version 0.1 held unchanged. These changes go into version 0.2 of the standard.

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
