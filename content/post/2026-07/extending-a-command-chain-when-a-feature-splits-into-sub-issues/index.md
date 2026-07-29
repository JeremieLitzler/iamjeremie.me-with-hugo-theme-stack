---
title: "Extending The Command Chain When A Feature Splits Into Sub-Issues"
description: "A large feature broken into GitHub sub-issues doesn't fit the same worktree-per-issue assumption my `jli-*` command chain was built on. Here's what I had to add to make it work."
image: /images/2026-03-09-white-robot-looking-at-the-camera.jpg
imageAlt: White robot looking at the camera
date: 2026-07-29
categories:
  - Artificial Intelligence
tags:
  - Git
  - Claude Code
hasMermaid: true
---

I promised at the end of my last article that I’d come back once I hit a large feature with the new `jli-` command chain. That happened last week, on my “Coup de Pompe” app, and it turned out to need more than a passing tweak.

In [issue #64](https://github.com/JeremieLitzler/french-gas-stations-scraper/issues/64) of my favorite French gas station scrapers, I had started with the specifications (business, security and tests) using the old agent pipeline and left an opened PR for a couple of months, being busy on other things until the start of July.

When I returned to it, I reviewed the PR, made about 40 comments to specifications. Then, I realized my chain of commands didn’t support specification review nor a feature with multiple sub-issues with a logic of implementation that required tackling some before others.

So what had to change in my chain of commands is the topic of today’s article.

## When the Worktree Already Exists

I built `/jli-sets-up` around one assumption: an issue number turns into a _new_ branch from `origin/develop`. Issue #64 broke that assumption immediately. It already had a branch, `feat/github-repo-preferences`, containing the specifications written two months back, and an open PR, #87. So instead of creating anything new, I attached a worktree to the existing branch.

That detour surfaced a variant of a bug I’d already fixed once, in a different project. This machine’s layout puts the bare repo, `french-gas-stations-scraper.git`, as a **sibling** of its worktrees under a shared `E:/Git/GitHub` parent, rather than nested inside one. The pipeline scripts here still assumed the bare repo was the worktree’s parent, so they failed the same way the `SocialMediaPublisherApp` scripts once did. I worked around it for now with direct git commands against the bare repo, but it’s a reminder that a fix in one repo’s scripts doesn’t travel to another repo on its own.

I won’t make the command repository agonistic right now because I’ll be using the chain on a repository whose main programming language varies from a repository to another (JavaScript, Python, C#, etc.). But the commands will very likely go into my dotfiles repository inside the `.claude` profile-level files.

## A Command for Reviewing Specs After the Fact

So the specifications were reviewed on the PR and therefore, the files needed an update. So I added a new command `/jli-reviews-specs`, a command that reads PR feedback, whether it’s comments, reviews, or inline notes, and amends the spec-phase artifacts. When there’s no PR to read from, it can pull the same kind of feedback straight from direct chat instead, and it can recreate the feature worktree on the PR branch if that worktree no longer exists locally.

I started with a narrower, singular version of this command, then broadened it once I realized a spec change rarely stays contained to one document. Business specs, security specs, test specs, and ADRs all need to stay coherent with each other, so the command checks across all four rather than patching just the one a reviewer happened to comment on. It runs from the feature worktree, the same as everything else in the chain.

Of course, to update the specifications, the `/jli-writes-specs`, `/jli-verifies-security` and `/jli-writes-tests-spec` commands were slightly tweaked to not only look at the `README.md` defining the feature, but also the specification review file the new command had written. By being aware of the review file, the commands could update the specifications according to the items to deal with.

## Specifications Are Merged, Now What?

That review command exposed a gap in `/jli-sets-up` itself: what do you do once you wrote and merged specifications, and you’re ready to resume implementation? The old version only knew how to start from scratch. So I split it into two modes:

- Mode A is the original path: an issue number goes in, a new worktree and task folder come out, and the chain moves straight to `/jli-writes-spec`.
- Mode B starts from a validated specification artifact and expects an issue ID that is a sub-issue of the original “specifications” issue. It creates a fresh worktree from `origin/develop`, brings the already-merged specs along into it, and resumes the chain at whichever phase hasn’t run yet.

However, that second mode needs to know what is the clean way back into the implementation phase.

## The Large Feature: Sub-Issues

This is the part I said I’d write about. Some features are big enough that you need to split them into GitHub sub-issues, each with its own title and its own scope, but sharing one parent issue that dealt with the specifications. The chain had no concept of that at all, so `/jli-sets-up` now detects it in Mode B. If an issue’s title contains “Sub-Issue,” or its body contains “Part of #XX,”, where `XX` is the specifications issue, setup switches to a sub-issue variant.

The trickiest call was what to name the branch and worktree. My first instinct was to encode the parent issue into the slug, something like `issue-64-sub-42-github-repo-preferences-oauth`. That could fail on Windows path-length limits the moment you’re several folders deep into a worktree. So the slug for a sub-issue is just the sub-issue’s own summary, on its own, without the parent baked in.

After the naming was settled, the folder layout needed the same split. Specifications are shared work: they live once, at the parent, in the `issue-<id>-<slug>/` folder. But the outputs of implementation, the technical specifications, review results, and test results differ per sub-issue, so I decided they’d go into a `sub-issue-<n>/` subfolder underneath the parent.

Six of the implementation-phase commands needed to know about that split: `jli-codes`, `jli-reviews-code`, `jli-writes-tests`, `jli-runs-tests`, `jli-commits`, and `jli-ships`. Each got the same rule added: read the shared specs from the parent folder, write your own outputs to whichever folder you were given, and parse the id out of either an `issue-<id>-<slug>` or `sub-issue-<id>` path.

The additional rule was about thirteen lines per command, then condensed it down to five once the pattern was clear. I was tempted to pull it into a shared skill instead of repeating it six times. But that would have broken the one invariant the whole redesign exists to protect: every command has to stay self-contained so I can `/clear` between phases without losing anything a command needs to know about itself. A shared skill is one more file to load and one more place state can silently diverge from what a command actually does. Five repeated lines cost less than that.

Of course, three commands deliberately didn't get the rule. `/jli-writes-specs`, `/jli-verifies-security` and `/jli-writes-tests-spec` only ever receive the parent folder, never a sub-issue folder, so there was nothing for the rule to apply to.

## Closing the Loop Back to Spec Review

One more wrinkle came out of combining sub-issues with specification review. `/jli-codes` can already emit a `status: review specs` signal that sends the chain back to `/jli-writes-spec` when something in the spec doesn’t hold up during implementation. I had to teach `/jli-writes-spec` to find that feedback in the right place, either as a flat sibling section called `### Specifications Need Review` inside `technical-specifications.md`, or nested inside a sub-issue’s own subfolder.

Since the spec being amended is the _shared_ parent spec, not something scoped to one sub-issue, the command now explicitly flags that the change affects every sibling sub-issue, not just the one that raised the flag.

## Documentation and a Small Bug on the Side

`AGENT-COMMAND-MIGRATION.md` needed updating to match all of this. So I split its single diagram into two: one showing the entry modes into the chain, and one showing the full chain end to end, plus a new section walking through how sub-issues fit into both.

## Final Observations

While working on [issue 85](https://github.com/JeremieLitzler/french-gas-stations-scraper/issues/85), I had to go back to specifications and coding until the expected result was reached. This showed me that, though the commands are independent, I could run through several cycles without an issue, similar to what the subagents would do. However, I, as a human, can look at the full history, since it was all recorded in the Markdown file.

It’d seem that I need an additional step to decide the next action ONLY in such a complex scenario. Running 7 rounds to finalize the sub issue mentioned above seemed a lot. Maybe it wasn’t an error but the normal flow of things. Imagining every scenario in advance is overkill to actually make good progress. Iterating is better/more efficient, in my opinion, just like I’m refining my chain of commands.

There were gaps that showed me that the AI models don’t come with the logic to say “Ah, there is incoherence. I’ll investigate”. This is something I’ll investigate to improve my commands and skills.

In reality, the principle of looping is what could prevent this from happening. Looping doesn’t remove 100% of incoherence. We all have to remember that AI is a statistical tool so it will **NEVER** reach 100% accuracy.

Hence, human check gates allow to remove some errors the AI model wouldn’t find. Now, it’s also a question of tradeoffs: you can loop 5, 10 or 20 times, but the cost will increase and cost you. Whether to loop or not to loop, you decide ultimately and you’re accountable for the result and its viability.

Is the chain of commands less efficient? At first, it may feel so because you took more of **YOUR** time to review but in the end, you’ve acquired and retained knowledge about how your application works from the business point of view **AND** the technical point of view.

To me, when you loop a lot, you may reach a better result. But in the end, if you lack the business and technical knowledge, what guarantees can you provide that it will work as you originally imagined it to work?

## Conclusion

None of this was designed in advance. The sub-issue handling, the dual-mode setup, the spec-review loop back, all of it came from running the chain against a feature that didn’t fit the shape I’d built two weeks earlier.

That’s the trade I made when I gave up the orchestrator for something less clever: the chain doesn’t anticipate edge cases for me. So I found them the way I found the sibling worktree bug, by actually observing them happen.

What it does give me is a chain that’s easy enough to open up and extend in an afternoon, one command at a time, without having to touch anything that already works.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

_Photo by Alex Knight on Pexels._
