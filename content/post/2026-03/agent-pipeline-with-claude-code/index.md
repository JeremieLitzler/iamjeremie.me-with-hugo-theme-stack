---
title: "Agent Pipeline With Claude Code"
description: "Just like us, AI is better when it is specialized. One responsibility, one agent and the output provide a much better result."
image: 2026-03-09-white-robot-looking-at-the-camera.jpg
imageAlt: White robot looking at the camera
date: 2026-03-16
categories:
  - Artificial Intelligence
tags:
  - Claude Code
---

On February 19 of this year, I recreated a dead link checker application with Claude Code. And I started by setting up the team of sub agents to build this application.

I just started to use Claude Code a week before and I was already feeling that I should give a specific task of the project realization to a given agent:

- one writes the specifications,
- one codes,
- one tests,
- one handles versioning
- and one orchestres the workflow.

Let’s look at how it went.

## About Using Sub-agents

It **works well when you’re clear with subagent responsibility**—clearly non-overlapping. Just like when you work in a human team.

That’s not what I did from the start with all agents. But I refined them I realized that.

For example, the boundaries between the orchestrator and git subagent weren’t very clear. Both would run Git commands when only one was supposed to.

So let’s me show how I went about it.

## The Starting Point

Originally, [Claude.ai](http://Claude.ai) suggested a shell script, but I didn’t like that. I wanted the sub-agents to communicate through Markdown files. In that way, when a sub-agent completed its task, it'd report back to the orchestrator who handed off the job to the next agent in line.

In addition, this allows for versioning of the development process.

[Claude.ai](http://Claude.ai) suggested this starting file structure:

```plaintext
project/
├── .agents/
│   ├── specs.md          # specs-agent output
│   ├── code-ready.md     # coder-agent output
│   └── test-results.md   # test-agent output
├── orchestrator.sh       # glues agents together
└── prompts/
    ├── specs.txt
    ├── coder.txt
    ├── tester.txt
    └── git.txt
```

I tweaked it to this one:

```plaintext
project/
├── .agents-output/
│   ├── specs.md          # specs-agent output
│   ├── code-ready.md     # coder-agent output
│   └── test-results.md   # test-agent output
└── .agents-brain/
    ├── agent-0-orchestrator.md
    ├── agent-1-specs.md
    ├── agent-2-coder.md
    └── agent-3-tester.md
    └── agent-4-git.md
```

`.agent-output` files are empty at the start and as the sub-agent works, it’ll be filled out. If you read [my previous article](../organizing-specifications-with-claude-code/index.md), the `.agents-ouput` is similar to `docs/prompts/tasks`.

The `.agents-brain` is the most important part that you need to adjust to your sensitivities and habits.

Here are [my agent’s brains](https://github.com/JeremieLitzler/deadlinkchecker/tree/main/.agents-brain) for the project. This isn’t the latest version, because I have since integrated and fine-tuned the structure inside the other project `SocialMediaPublisherApp` available [here](https://github.com/JeremieLitzler/SocialMediaPublisherApp).

Once I tweaked everything, I launched Claude Code in the terminal and the orchestrator agent picked up my initial prompt in the `README.md` to start the work.

{{< blockcontainer jli-notice-warning "Important remark">}}

If you use Claude Code for a longer time than me, you might say: _“Yes, but subagents should go under `.claude/agents`“_. Yes, I know I found out about that a bit later in the journey. I’ll come to that in another article.

{{< /blockcontainer >}}

## Agentic Programming Doesn’t Mean it’s Always Right

And neither humans.

At first, I asked to use a Bash script to perform the job. But when the testing agent tried to do its job, it failed over and over, ignoring the `MAX_RETRIES = 3` and unable to verify the logic worked as expected…

Claude suggested using Python at first instead before I specifically asked for Bash. I thought that Bash would require no dependencies and came bundled with Git.

The Python route required Python installed and, I thought, many other dependencies. But it turns out it didn’t, as Python comes all the built-in libraries my application needed.

The lesson: don’t always think you know the best approach, nor trust the AI to do the job without directions. But don’t be afraid to try a few routes.

## Improving the Workflow

As I continued to build the application, I refined the brains of each agent and tweaked the workflow:

- I added intermediate commits after each agent, first specifications, then coding and finally testing agents, once they completed their job.
- I asked to commit after the specifications or code was approved.
- I updated the specifications agent to provide less code and let the coding agent handle that job itself.
- I updated the git agent to make a better choice in regards to the type of commit it’d choose. It kept making a wrong pick committing specifications with the type `chore` instead of `docs`. I also made clear that it needed to follow conventional commits, providing clear examples.
- I installed GitHub CLI through Scoop to enable the orchestrator to create PR, complete it, when the human validates, and to close the related issue. It turned out to be a Git subagent responsibility later on on my learning path.
- I also improved the output folder structure to become the following:

```plaintext
project/
├── .agents-output/
|   ├── 0-user-requests/
|       ├── _initial.md # contains the former Markdown content
|       ├── 2026-02-26-07-33-28-issue-23-reorganize-agents-output-folder.md
|       └── 2026-02-26-13-01-39-issue-35-add-option-to-exclude-3xx-from-email-notifications.md
│   ├── 1-business-specifications/
|       ├── _initial.md
|       ├── 2026-02-26-07-33-28-issue-23-reorganize-agents-output-folder.md
|       └── 2026-02-26-13-01-39-issue-35-add-option-to-exclude-3xx-from-email-notifications.md
│   ├── 2-technical-specifications/
|       ├── _initial.md
|       ├── 2026-02-26-07-33-28-issue-23-reorganize-agents-output-folder.md
|       └── 2026-02-26-13-08-18-issue-35-add-option-to-exclude-3xx-from-email-notifications.md
│   └── 3-test-results/
|       ├── _initial.md
|       ├── 2026-02-26-07-33-28-issue-23-reorganize-agents-output-folder.md
|       └── 2026-02-26-13-13-31-issue-35-add-option-to-exclude-3xx-from-email-notifications.md
```

## Adding New Agents

From the original agent pool I defined, I ended up adding a few new ones :

- an agent reviewing security concerns of the application right after the specifications.
- an agent defining test use cases before coding and writing the tests after coding. Yes, TDD isn’t something I’ve yet figured out in my agent pipeline.
- a code reviewer after I tried the Claude Code reviewer workflow, but somehow, I wasn’t able to make it work. For now, this agent does the job and actually found useful adjustments post-coding.
- a maintenance agent in the agent pipeline whom I could ask for updates whenever I encountered issues while running an agent or the process. It occurred a few times when I made changes to agent organization, in particular when integrating the Git worktree feature in the pipeline to run parallel pipelines.

However, I’ll need to take a step back at one point and clarify the definition of agent, skill and tool. I’m pretty sure some of my “agents” are skills in reality.

That’s a topic for yet another coming article.

## Next Steps

I’d like to let the AI do more unassisted work, but this requires defining the features or bugs very clearly in advance. Otherwise it can go sideways and waste your available tokens and time. Also, there are a lot of shell commands that require approval, and for good reasons. That could limit the possibility of running an unassisted Claude Code without major security trade-offs.

Indeed, when I use Claude Code, the 5 h-session limit is reached fast, but if I give the teams work and build a system to monitor the 5 h-session limit so it can pause and resume the agents, I might get more out of the price paid for the service. I’m sure that’s something possible.

However, I think human interactions are still **really needed** because the human gives ideas. He enriches the ideas as he sees the product gets built and he catches the AI hallucinations (still numerous). At least, that’s how I felt building the DeadLinkChecker application.

In the meantime, I shared this with a few colleagues and it stirred up a lot of interest. One shared the following tools:

- the [system prompts (this is my fork)](https://github.com/JeremieLitzler/claude-code-system-prompts) that Anthropic use to make their agents.
- the [Serena MCP](https://github.com/oraios/serena?tab=readme-ov-file) to optimize token consumption. [Rust Token Killer](https://github.com/rtk-ai/rtk/) is another little software to save on input tokens that I’ll talk about soon because I already integrated it contrary to the first.
- the [Open Code project](https://opencode.ai/docs), an alternative to Claude Code, which you can use with free LLMs and many other premium but sometimes less expensive LLMs like DeepSeek, Gemini, Mistral, etc.
- the [AgentOS package](https://buildermethods.com/agent-os) that can shape better specifications and keeps agents aligned in a lightweight system that fits how you already build.

Clearly, I have got many things to experiment and share in the near future. So subscribe ⬇️⬇️⬇️

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

_Photo by Alex Knight on Pexels._
