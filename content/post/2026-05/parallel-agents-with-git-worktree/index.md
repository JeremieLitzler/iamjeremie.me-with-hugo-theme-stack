---
title: "Parallel Agents With Git Worktree"
description: "I never heard of worktrees until I needed to run Claude Code in parallel. But it needs adjustements to one’s Git usage."
image: /images/2026-03-09-white-robot-looking-at-the-camera.jpg
imageAlt: White robot looking at the camera
date: 2026-05-11
categories:
  - Artificial Intelligence
tags:
  - Git
  - Claude Code
---

Back in March, a colleague of mine, the same one as before, came to me and said:

> Have you figured out how to run parallel agents with Claude Code?

I answered with the negative.

He continued:

> Do you know worktrees?

Again, I didn’t know about this feature of the popular versioning control software. So he presented the feature, native to Git, and then it clicked in my mind!

## What Are WorkTrees

Git worktrees let you check out multiple branches of the same repository simultaneously, each in its own directory, sharing a single `.git` database. Instead of stashing or committing half-finished work to switch branches, you just `cd` into another worktree.

To get started, you need to clone the repository as _bare_:

```sh
git clone https://github.com/JeremieLitzler/git-experimentations --bare
```

Then, you can browse the repository’s main folder and can create your first worktree.

However, bare clones, by default, don’t create remote-tracking branches (`refs/remotes/origin/*`), like the `main` that you’ll probably need. Instead, the remote branches are mapped directly to local refs. You can verify with `git branch -a`—you won’t see `origin/main`.

To fix that, fetch with the standard refspec first:

```bash
cd git-experimentations.git
# The terminal looks like "/e/Git/GitHub/git-experimentations.git (BARE:main)"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```

Now `origin/main` exists and the following worktree command will work:

```bash
git worktree add main main
```

**Why this happens:** `git clone --bare` sets the fetch refspec to `+refs/heads/*:refs/heads/*`, mirroring remote branches as local branches rather than tracking branches. The config change above restores the usual non-bare behavior.

Next you can create a new worktree:

```sh
git worktree add feature-branch -b feature-branch
cd feature-branch
# The terminal becomes "/e/Git/GitHub/git-experimentations.git/feature-branch (feature-branch)"
```

The above command creates a new working directory `feature-branch` linked to the new branch `feature-branch`.

Running `git worktree list` will show all active worktrees, and `git worktree remove` cleans one up.

The main constraint is that no two worktrees can have the same branch checked out at the same time. So if you used to use `git checkout` to switch from a branch to another, you’ll need to stop.

Once you’ve made your feature changes, you simply push the branch to remote and create the PR.

After the PR merge, you can clean up the local repository with several commands, some you know already, some new because of the worktree usage:

```sh
# update the main branch
cd ../main
git pull origin main
# Remove the worktree:
cd ..
git worktree remove feature-branch
# Delete the local branch:
git branch -d feature-branch`
# Delete the remote branch, if not done while merging the PR:
git push origin --delete feature-branch
# Prune stale remote refs:
git fetch origin --prune
```

You can read more about them [in the official docs](https://git-scm.com/docs/git-worktree).

## Why Worktrees For Agent Parallel Runs

It may seem obvious to some of you, but the ones who didn’t get yet, I’ll explain now.

Using worktrees with Claude Code will enable you to work in parallel on two different features.

You simply launch two terminals, each with its Claude Code running and you can tackle the development of a feature.

It’s similar to have two developers working on the same project, but different features. And with that comes the same issues: if both feature touch the same files, you’ll run into merge conflicts when merging the second feature after the first was integrated in the `main` branch of the repository.

## Caveats With Worktrees

There’s one and it has to do with Windows and a long path. When I tried the agent workflow with worktrees, I had a worktree name like this: `fix_the-back-button-in-browser-fail-to-load-index-page-from-a-platform-page`.

Then, when the code reviewer and test runner agent came onto the scene, they both failed. Why? Because the full path was `/e/Git/GitHub/SocialMediaPublisherApp.git/fix_the-back-button-in-browser-fail-to-load-index-page-from-a-platform-page/`.

The worktree folder's name is extremely long. When the agent tries to `cd` into it via bash, MINGW64 on Windows can choke on very long paths, causing commands to silently fail or error out before even running `npm` commands.

I capped at 30 chars the slug evaluation and the issue never came back.

But, if you are on Windows, use WSL to emulate a Linux OS on Windows without its limitations.

## Going Beyond Worktrees

Now that you know what are worktrees and how you could use them in your workflow, you can start using [Worktrunk](https://worktrunk.dev/), a Git worktree management tool for parallel AI agent workflows. It provides a better DX to you and Claude.

To be honest, I am not using parallel Claude Code a lot. I don’t spend enough time (or maybe tokens 🙃) to really need it, but I have integrated it in my team of agents. You can look [at this repository as an example](https://github.com/JeremieLitzler/SocialMediaPublisherApp/tree/develop/.claude/agents) to review my agents.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
