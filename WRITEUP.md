# The summary kept the agents' scorecard
*Drafted with Claude Code (Claude Opus 5.5) from the results in this repo, at Dan Epstein's request. Every number comes from `results/kindness/`.*

*Dan Epstein, The Long Game Project. AI Village swarm hackathon, 5 October 2026.*

When a model reads agent traces for an investigation, the report rarely says how far to trust that reader. Three things would tell you: who wrote the record the model read, whether each claim is about an action or a mind, and whether a second reader from another lab agrees.

Last month I published a one-paragraph standard for reporting those three things, the [adjudication statement](https://www.longgameproject.org/standards/adjudication-statement). For this hackathon I built a tool that fills it in, and ran it on one week of the AI Village.

## One week, one model reader, and a record it never saw

The AI Village is AI Digest's long-running experiment: AI agents, each with its own computer, sharing a group chat and working towards a goal the staff set. The goal for 22 to 26 December 2025 was "Do random acts of kindness!" Ten agents from Anthropic, OpenAI, Google and DeepSeek emailed real software developers to thank them. By AI Digest's account, complaints followed, and on 26 December the staff banned unsolicited email.

The model reader is AI Digest's own summary of the week, which Claude Sonnet 4.5 wrote from the chat and event logs. It never saw inside the agents' computer sessions. I split the summary into 40 claims.

The independent record is the part the agents did not narrate: 26,570 computer-use turns (actions, tool output, errors, server timestamps) and a screenshot after every action.

## Three sorters, one human, two judges

- A panel of three models from three labs (Claude, Qwen and Gemma) sorts each claim. L: the logs, a record the agents did not write, could settle it. M: it is about what an agent believed or wanted. B: both. ?: not sure.
- I sort the same 40 claims blind. The tool scores how often we agree, with Cohen's kappa and a bootstrap interval.
- Two judges, the vision models qwen3.5 and gemma4, each rule on every L claim against the turns and screenshots: supported, contradicted or not settled. A flip is a claim where the two judges rule differently, so the answer depends on which judge you ask.
- For email counts, a typed email counts as sent only when both vision models see Gmail's "Message sent" notice in the screenshot.

Qwen and Gemma run on one 8 GB gaming GPU, and Claude's parts ran inside Claude Code, so there were no metered API calls (which is also why the judges are small).

## The sort matched September, and the judges believed the agents

Claude and I gave the same answer on 34 of 40 claims (kappa 0.61, 95% interval 0.32 to 0.85). Gemma agreed with me on 33 (0.57), Qwen on 27 (0.36). In September, on the 36 findings of METR and Redwood's report on the OpenAI agents in the Hugging Face incident, Claude and I scored 0.62. A second dataset gave nearly the same figure, though both intervals are wide.

Where Claude and I split, it was mostly on claims about what an agent said. Take "Claude Haiku announced on 22 December that all nine teammates had been appreciated." The chat log records the announcement, and all three models marked it L. I marked it M. The line between what an agent said and what it believed is where the sort rule is weakest.

The judges did much worse. Of the 32 L claims, they split on 11. They agreed on 21, and 15 of those were "not settled", which leaves six firm rulings. I had Claude Opus 5.5 check those six against the record, naming the turn or screenshot behind every verdict. Two hold, one holds in part, and three do not.

Where the judges went wrong, it was mostly by taking an agent's own words as the record: one agent's tracking file, one agent's running tally, the agents' own messages. Once they cited turns that had nothing to do with the claim.

So I labelled every line by who wrote it, the computer or the agent, and told the judges the difference. Rulings that both judges called supported fell from 9 to 5. The habit stayed. Small local judges can sort the pile, but a person has to check every ruling they make.

## Who kept the score? The agents did

**The summary's email counts are the agents' own end-of-day chat tallies, passed on.**

The summary says Claude Opus had sent "eleven thank-you emails to developers" by the end of 22 December. Opus did post "11 emails SENT & VERIFIED" in chat that afternoon. The screenshots show 10 sends with the notice on screen. Seven are thank-yous to developers. The other three are replies: one to another agent, one to a member of the public who asked about an optimiser, and one to a member of the public who suggested a maintainer to thank. At 12:44 Pacific, Opus counted its own emails as five to maintainers plus replies. The two maintainer emails it sent after that make seven.

Where an agent counted one kind of email, the number held. Claude Haiku's 24 by 22 December is 24 recipients (25 sends, one a resend). Its 31 emails on 23 December match 31 confirmed sends. The summary does not say that 9 of Haiku's first 24 recipients were other AI agents in the village.

The times drift too. The summary puts Opus's first email at 11:22 Pacific. That is when Opus announced it in chat. The screenshot shows it sent at 11:13.

The vision models failed as judges, so why trust them here? The question is narrow: is a "Message sent" box on the screen, yes or no. Both models must say yes, and every evidence screenshot opened in the check shows the box.

A reader that works from the agents' words inherits their scorekeeping.

## The filled statement

This is the tool's output, before the check of the six rulings. Its "5 verified" means both judges said supported. On checking, two of those five hold and one holds in part, and the one contradiction does not stand. A "coder" is any sorter, model or human. My blind sort judged what kind of claim each one is. The judges and the check judge whether it is true.

> **Adjudication statement.** Findings with an independent record: 32 of 40. Findings verified against one: 5 of 32 checked, both judges agreeing; 1 contradicted, 15 not settled by this record, 11 flipped when the judge was swapped. Findings resting on model judgement: 7, plus 0 mixed and 1 unresolved. Model reader: Claude Sonnet 4.5, developer Anthropic, writing about agents from Anthropic, OpenAI, Google and DeepSeek; it did not see inside the computer-use sessions. Order of reading: chat and events only, never the computer-use sessions (dataset schema). Panel: 3 readers from 3 developers (Anthropic (Claude), via a Claude Code subagent; Alibaba (Qwen), open-weight; Google (Gemma), open-weight), majority rules, a not-sure is a vote. Human audit of model findings: 40 sorted blind of 40, 6 differ from the panel. Confidence bands: none. Not-sure: offered to every coder. Load-bearing count per headline finding: not stated. Re-runnable by an outside party: yes, because the dataset is available from AI Digest on request and the coders and judges are in this repo.

## So how far should you trust the summary?

On what the agents did, about as far as you trust the agents' own chat. Its counts are their tallies, and its times are their announcements. On what they meant, 7 of its 40 claims rest on model judgement alone, and nothing in the record can settle them. The summary does not say either thing. The statement does.

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
