---
title: "Amending A File in Last Commit"
description: "Example: bring a shared commit from a feature branch back to its parent"
image: /images/2026-04-29-logo-of-git-scm.svg
imageAlt: Logo of Git Versioning Software
date: 2026-05-27
categories:
  - Software Development
tags:
  - Git
  - Versioning Control
---

You’re working on `target-branch`. You create a new branch from it:

```bash
git checkout -b source-branch
```

You make a first commit specific to `source-branch`, then a second commit with changes that should also live on `target-branch`.

You need to bring only that last commit back to `target-branch`. How do you perform this task?

## The Solution

```bash
git checkout target-branch
git cherry-pick source-branch
```

When you pass a branch name without a range, `git cherry-pick` picks only the latest commit of that branch.

## Cherry-Picking Multiple Commits

If you need the last two commits instead:

```bash
git cherry-pick source-branch~2..source-branch
```

The range `source-branch~2..source-branch` means “all commits after the second-to-last up to and including the tip.”

## Handling Empty Cherry-Picks

You may encounter this message:

```plaintext
The previous cherry-pick is now empty, possibly due to conflict resolution.
```

It means the changes from that commit already exist on `target-branch`. The commit produces no diff.

You have two options:

```bash
git cherry-pick --skip      # skip it and move on
git cherry-pick --abort     # cancel the whole operation
```

This typically happens when a previous merge or cherry-pick already brought the changes in, or when conflict resolution accepted the target branch’s version entirely.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Git Logo by Jason Long is licensed under the Creative Commons Attribution 3.0 Unported License.
