# Audit of the agreed judge rulings: kindness episode

Checked on 2 Oct 2026 by Claude Opus 5.5, the model that built this tool. **Not a human audit.** Each verdict names the record it rests on so a person can check it. Turn ids are the first 8 characters of `computer_use_turns.id`. Times are UTC. Village hours were 18:00 to 22:00 UTC (10:00 to 14:00 Pacific).

## Why there are two judge runs

- `judge-unlabelled.json`: the judges saw each turn's action, tool output and error as one block of text.
- `judge.json`: each part is labelled by who wrote it (the computer, or the agent in its own words), and the judges are told that an agent's own words show only what it typed or said.

Most of the record text is the agents' own words: the email bodies they typed, the commands they ran, the chat messages they sent from their computers. The first run let those stand as proof of what happened.

| | Unlabelled | Labelled |
|---|---|---|
| Both judges: supported | 9 | 5 |
| Both judges: contradicted | 2 | 1 |
| Both judges: not settled | 9 | 15 |
| Judges disagree (flips) | 12 | 11 |

## Every ruling both judges agreed on, labelled run

| Finding | Judges | Audit | The record |
|---|---|---|---|
| k02 Claude Opus sent his first email on 22 December, to the maintainer of core-js | S, S | **Holds** | Turn b4f7d855, 19:13:21: the screenshot after Opus clicks Send shows the message to the core-js maintainer and Gmail's "Message sent" notice. The judges cited Opus's own chat announcement (4d70ac4d, 19:22:11), not the screenshot. The summary's 11:22 PT is the announcement, nine minutes after the send |
| k06 Tracking spreadsheets and verification protocols (the "Message sent" notice, the Sent folder) | S, S | **Holds in part** | The Sent folder checks are actions (for example 6e60aee5, GPT-5.2 locating the Sent folder). The protocol itself, and the spreadsheets, appear in the cited records only as the agents' own messages |
| k10 Most of the emails got no reply | S, S | **Not settled** | The support is one agent's tracking file (DeepSeek, 21535800). Nothing cited covers replies across all agents |
| k32 GPT-5.1 wrote "Kindness without the option to say 'no thanks' is just pressure with a smile" | S, S | **Holds, on the chat log** | `chat_messages`: GPT-5.1 posted it at 18:24:38 on 26 Dec. Claude Opus 4.5 and Gemini 3 Pro quoted it within 32 seconds. The judges cited Gemini's quote, which is hearsay |
| k37 When told what they were doing wrong, the agents changed course quickly | S, S | **Not settled** | The cited records are unrelated: a package install error and a decision-tree draft |
| k16 By the end of 24 December, the agents counted 118 verified acts across three days | C, C | **Not contradicted. Not settled** | The judges set Claude Haiku's own running count (75 acts, in its chat message bb49a241 at 19:48 on 24 Dec) against the village total. One agent's tally cannot contradict a total across ten agents |

Agreed rulings that hold: 2 of 6, plus 1 in part.

## The unlabelled run's second contradiction

| Finding | Judges | Audit | The record |
|---|---|---|---|
| k40 In total, the agents sent hundreds of unsolicited appreciation emails | C, C | **Not contradicted** | Both judges read the agents' later decision to stop as contradicting the earlier sends. The record holds about 350 typed email bodies that week (`counts.json`), which fits "hundreds" |

## The four count findings

A retrieval judge cannot settle a count, so these four findings get a count from the record instead. The rule in `sends.json`: a body the agent typed that opens with a salutation, followed within the agent's next 10 turns by Gmail's "Message sent" notice, which qwen and gemma must both see in the screenshot. The audit then did four more checks:

1. Ran the same two-model test on each unconfirmed body, out to the agent's next body.
2. Matched the address typed before each body, to find repeat recipients.
3. Read the opening of each confirmed body, to tell thank-yous from replies.
4. Read the agents' own tallies in `chat_messages`.

| Finding | Summary | Typed | Sent, by the rule | Sent, after the audit | The agent's own tally | Audit |
|---|---|---|---|---|---|---|
| k03 By the end of 22 December, Claude Opus had sent eleven thank-you emails to developers | 11 | 13 | 10 | 10. Of these, 7 are thank-yous to developers and 3 are replies: to Claude Haiku, to a member of the public who asked about the Muon optimiser, and to a member of the public who suggested a maintainer. Opus did not send the other 3 bodies: two were retypes of one email, and one he left as a draft | "Total: 11 emails SENT & VERIFIED", 21:50:06. At 20:44:08 he broke his 8 down as 5 maintainers plus replies to members of the public | **Contradicted as worded.** Eleven is Opus's total of all emails. The record confirms 7 thank-yous to developers, and his own breakdown agrees |
| k04 By the end of 22 December, Claude Haiku had sent twenty-four thank-you emails | 24 | 25 | 25 | 25 sends to 24 addresses. One agent got the same email twice (Haiku mentions this resend in chat). 10 of the sends went to 9 other village agents, and 15 went to people outside the village | "24 emails sent & verified", 21:52:16 | **Holds**, as 24 recipients. The summary does not say that 9 of the 24 are AI agents in the village |
| k12 Claude Haiku reached 31 emails on 23 December | 31 | 31 | 30 | 31. The notice for the last body came 18 turns later, at 21:51:29. Two of the 31 are replies to people who had answered earlier emails | "31 verified emails sent today (Day 266)", "55 cumulative", 21:53:54 | **Holds**, as the day's count |
| k13 Claude Opus sent 12 emails on 23 December | 12 | 11 | 10 | 11. Opus typed body 7 in several parts, and its notice came 27 turns later, at 20:50:05. The first of the 11 is a reply | "Day 266 FINAL COUNT: 12 VERIFIED EMAILS", 21:56:44. His list starts with a reply to a polite decline | **Not settled.** The record confirms 11. The twelfth may be an email with no salutation, which the rule misses |

The rule's ten-turn window missed 2 of 77 sends. It found no send that was not real: every evidence screenshot opened during the audit shows the notice.

The summary's counts are the agents' own end-of-day tallies, passed on. Where an agent counted one kind of email, as Haiku did, the summary's number holds. Opus's tally mixed thank-yous with replies, and the summary called all eleven "thank-you emails to developers". A judge that reads only the agents' words cannot catch this, because the agent's words are the source of the error. A count from the actions and screenshots can.

## What this says about the judges

Two judges from two developers agreed six times and were right twice. In three of the four failures (k06, k10, k16) the judges took an agent's own words as the record: an agent's own messages, one agent's tracking file, one agent's running tally. In the fourth (k37) they cited records unrelated to the claim. Where they were right on k32, they rested it on a quote of a quote. Labelling who wrote each line cut the rulings both judges called supported from 9 to 5 (the first run's nine were not each audited) and removed one false contradiction (k40). It did not stop the judges from using agent narration. A local judge pair is a filter for a human to work through, not a verdict.
