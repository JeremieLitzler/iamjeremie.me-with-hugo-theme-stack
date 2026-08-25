---
title: "Don’t Design the Skill Too Early—Use What You’ve Done to Craft One."
description: "Three brainstorming sessions had already converged on the same working pattern. Extracting a Claude Code skill from them beat designing one from scratch."
image: 2026-08-28-a-skilled-blacksmith-working-in-his-rustic-workshop.jpg
imageAlt: A skilled blacksmith working in his rustic workshop, crafting metal with traditional tools.
date: 2026-08-28
categories:
  - Artificial Intelligence
tags:
  - Claude Code
  - Documentation
---

I didn’t set out to design the skill I’ll be talking about today when [I replaced Claude.ai](../i-replaced-claude-ai/index.md). It came a few months later, after working on three distinct topics filled with context, data and prompts, I noticed what they had in common..

That turned out to become a skill because I noticed that I was using a pattern I could reuse.

Let’s review the steps to build it.

## Three Projects, One Method

Over a few weeks, three unrelated projects had grown and matured in my Claude archive: sizing a solar installation with battery storage at home, replacing an Amazon Seller Central integration for a small book shop, and working out how mobile push notifications could reach an app I was working on for a client.

Nothing connected them except that each had needed research, several rounds of refinement, and a set of decisions at the end.

Opening them side by side, the same skeleton appeared in all three:

|                 | Solar project                          | Book website                 | Push notifications                        |
| --------------- | -------------------------------------- | ---------------------------- | ----------------------------------------- |
| Context         | `README.md` with plans and load curves | folded into the prompt       | a raw meeting transcript                  |
| Ask             | `PROMPT.md`                            | `INITIAL-PROMPT.md`          | —                                         |
| Deliverable     | `PLAN.md` v7, with a correction log    | `PLAN.md`, marked “Draft v1” | `SYNTHESE-ET-QUESTIONS.md`                |
| Feedback        | ’FEEDBACK-PLAN-v1’ through ’v7’        | —                            | `FEEDBACK-SYNTHESE-v1.md`                 |
| Reproducibility | `analyse/*.py` plus their CSV outputs  | —                            | diagrams and a sourced references section |

I didn’t plan for it.

It emerged because I organized the way I used Claude Code when prompting it.Anthropic’s own guidance states that this moment marks the ideal time to reach for a skill: “[As you work on a task with Claude, ask Claude to capture its successful approaches and common mistakes into reusable context and code within a skill.””](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

The alternative—sitting down to design the ideal brainstorming workflow—would have produced something that wasn’t as ready-to-use as my first draft of this skill. We would have invented the parts we thought mattered instead of keeping the parts that had already survived seven rounds of being wrong.

## I Asked Where the Examples Disagreed

My three examples thatagreed with mee told me what towriten. But as you see above, they also disagree and that tells you what to ask about.

They disagreed on four points, and each one changed the shape of the skill:

- where the context lives and how it’s organized,
- how the deliverable should be versioned,
- what the files should be called (`README.md` vs. `INITIAL-PROMPT.md`),
- and which companion documents were part of the flow.

Rather than picking silently, we put the four questions up front and let the answers drive the build.

I defended the versioning answer hardest. The solar plan is a single `PLAN.md`, rewritten in place at every round, carrying a section called _Historique des corrections_ that reads like this:

```plaintext
v3: the module price was overestimated by ~75%; the claim that "the battery never pays for itself" was false, for lack of comparing against having no battery at all.
```

That log records what went **wrong**, not just the additions. Keeping `PLAN-v1.md`, `PLAN-v2.md` and so on would have preserved the same text with none of the meaning—`git` already holds the old words. What `git` can’t tell you which of yesterday’s conclusions you should stop trusting.

## The Rules Were the Real Payload

We needed to capture the habits that made those three sessions produce something trustworthy:

- Never compute in the chat. That’s something I’ve come to avoid early on because I need to understand the figures AI throws at me, not just _believe they’re true_. Any number that reaches the deliverable comes from a script because arithmetic that happens in prose can’t be rerun when an input changes at v5. Since you provide the data, you can check the soundness of the output from the script.
- Claims need a reliable source to hold added value. Collect them in a “sources” section and quote them where it matters.
- Split questions by audience simplifies follow up. On a large brainstorming, you know your audience and having a question section per audience makes easier to know what to act on. For technical feasibility, product arbitration and compliance sign-off are three distinct readers, and mixing them produces a list nobody can act on.

## Conclusion

Anthropic’s guidance for building skills recommends creating evaluations before writing extensive documentation so that a skill [“solves real problems rather than documenting imagined ones”](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). Therefore, you iterate on observed behavior rather than assumptions. Working on these three sessions constitutes a budget-friendly way to get most of that for free: _they’re_ the evaluations, already run, with their failures already recorded.

The skill we ended up with argues that a plan has value only if it records the journey to a set of decisions and choices. Its history makes the case better than its text does. Don’t design the skill too early. First, perform work yourself alongside the LLM, then, when you notice a repeated pattern, evaluate if a skill is waiting to emerge.

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by ΘSWΛLD (`https://www.pexels.com/photo/blacksmith-at-work-in-rustic-workshop-34116082/`)
