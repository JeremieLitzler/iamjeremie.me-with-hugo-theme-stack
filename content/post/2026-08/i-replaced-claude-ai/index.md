---
title: "I Replaced Claude.ai"
description: "Why I stopped chatting with Claude.ai and built a git-versioned archive of every Claude Code session instead."
image: 2026-08-24-from-claudeai-to-a-git-repository.jpg
imageAlt: From Claude.ai to A Git Repository
date: 2026-08-24
categories:
  - Artificial Intelligence
tags:
  - Claude Code
  - Claude
  - Git
  - Knowledge Management
---

For a while, claude.ai _was_ where my work with Claude lived.

Every question, every half-finished plan, every “wait, how did I fix that last time” answer was sitting in a chat history I didn’t control, couldn’t `grep`, and couldn’t guarantee would still be there in a year.

Plus, what if I stopped using Claude altogether? Could I export all conversations?

Since June 5, I’ve replaced it with something much simpler and sovereign alternative: a plain git repository I own, called `my-claude-conversations` (don’t look for it, it’s private).

## The Problem With a Chat History I Don’t Own

A hosted chat history is fine for a single conversation. It falls apart the moment you want it to be a _memory_.

I work across several machines, on projects that span weeks, and I regularly want to know how a past research session, brainstorm, or debugging session actually went, not just what the final answer was.

None of that is well served by a web app’s chat list. So I built a repository that plays that role instead, one I can clone, version, search, and back up like any other piece of software.

Plus, since February, I’ve been a Pro member of Claude, using Claude Code very often. So, what about using that new Git repository to store my sessions with Claude Code and being able to save them?

## Saving a Session From Anywhere

The core of it is a `/save-session` skill.

I run it at the end of any Claude Code session, in any project, and it does two things:

- it renders the session’s transcript into a self-contained HTML replay,
- and it writes a short markdown summary of what happened.

Both land in this new repository, under `replays/` and `summaries/`, named `YYYY-MM-DD-slug` so they sort chronologically and stay easy to scan.

What makes it work “from anywhere” is that it isn’t tied to any one project. It’s a global skill, installed once under my user profile, that locates the `my-claude-conversations` clone on whichever machine I’m on, and clones it fresh if it isn’t there yet.

That mattered more than I expected: I move between Windows or Linux machines, and the skill now detects the OS and resolves paths accordingly, so the same skill behaves correctly on both without me thinking about it.

So I can work on any of my projects and if I feel that the current session is worth keeping for a future REX or insight I want to share, I save the session and can replay the whole session just if I was back into Claude Code and on that session. The summary provides quick insights on the session, since the replay doesn’t contain the full session’s contents in the HTML.

### Baby Steps

The skill itself evolved a fair bit before it settled.

Early versions triggered two separate permission prompts, one to locate the session transcript and one to render it, which got old fast. Collapsing both steps into a single wrapper script turned it into one approval per save.

It also used to occasionally rediscover its own tool’s flags mid-run, adding a wasted round-trip before it could act; baking the exact invocation into the skill removed that too. None of this is dramatic, but it’s the kind of friction that decides whether you actually use a habit or quietly stop bothering.

## Multi-Session Projects Get Their Own Folder

Not everything fits in a single saved session. Some things I work on with Claude are projects in their own right, stretched over several sittings [^1]: sizing a home solar installation, deciding how to exit a platform I depend on, working through a technical migration.

For those, I keep a whole working folder under `prompts/`, named the same way as a session, `YYYY-MM-DD-slug`, but holding a lot more: the initial prompt that kicked things off, a living plan document that gets corrected in place rather than rewritten from scratch, numbered rounds of feedback as the plan matures, and whatever calculation scripts or raw data the analysis needed.

It’s a heavier structure than a single replay and summary, and it’s meant to be. A session record tells me what happened in one sitting. A `prompts/` folder tells me how a decision got made, round by round, with the reasoning still attached to it.

## Where This Is Heading

The summaries in particular have become something I go back to on purpose. When I’m looking for what to write about next, I read back through them, because they’re the records I have of which sessions actually taught me something worth sharing, whether that’s a fix, a comparison, or a lesson learned the hard way. That’s still a manual pass on my end today, but it’s the direction the archive is pulling me in: not just a record of what I did with Claude, but raw material for what I write about it afterward.

None of this replaces claude.ai as a place to have a conversation. What it replaces is the assumption that the conversation itself is worth keeping only as long as the chat window remembers it.

Plus, owning the record is enormous added value to me: in a repository I can clone, diff, and search, I turn every session into something I can actually learn from later, not just something I lived through once.

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Gemini.

[^1]: "Sittings" just means individual sessions at the keyboard—separate work stretches, not one continuous conversation. “Stretched over several sittings” = the project isn’t done in one sit-down; it’s built up across multiple separate sessions over time (a day here, a week later, etc.), as opposed to a single `/save-session`-sized conversation.
