---
title: "Amending A File in Last Commit"
description: "Example: to remove an accidently pushed secret to a configuration file"
image: /images/2026-04-29-logo-of-git-scm.svg
imageAlt: Logo of Git Versioning Software
date: 2026-04-29
categories:
  - Software Development
tags:
  - Git
  - Versioning Control
---

To revert a specific file to its previous state in the last commit:

```bash
git checkout HEAD~1 -- <file>
git commit --amend
git push --force-with-lease
```

Or if you just want to restore the file locally without amending the commit yet:

```bash
git checkout HEAD~1 -- <file>
```

This replaces the file with its version from one commit before, staging it automatically.

## But All Traces of the File’s Commit Aren’t Gone

As described in [the previous article](../git-remove-file-from-last-pushed-commit/index.md#but-all-traces-of-the-files-commit-arent-gone), any history rewrite (amend, rebase, etc.) leaves the old commit object and its associated tree/blob objects as dangling. It doesn’t matter whether you removed a file or just reverted a change—the previous version of that blob stays in `.git/objects` until garbage collected.

The same cleanup applies:

```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

The `reflog` is actually the main thing keeping those objects “reachable.” Git’s `reflog` records where `HEAD` and branch tips previously pointed, so even after rewriting, the old commits are referenced there for a default of 90 days. That’s why you need to expire it first before `gc` will prune anything.

The official [Git documentation](https://git-scm.com/docs/git-reflog) explains that “_the expiration time is taken from the configuration setting `gc.reflogExpire`, which, in turn, defaults to 90 days._”

Worth noting: unreachable entries have a separate setting `gc.reflogExpireUnreachable`, which defaults to 30 days. So after a history rewrite, the old entries are unreachable and would become prunable after 30 days, not 90.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Git Logo by Jason Long is licensed under the Creative Commons Attribution 3.0 Unported License.
