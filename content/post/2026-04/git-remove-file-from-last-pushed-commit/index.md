---
title: "Remove File From Last Pushed Commit"
description: "Example: to remove an accidently pushed .env file"
image: /images/2026-04-29-logo-of-git-scm.svg
imageAlt: Logo of Git Versioning Software
date: 2026-04-24
categories:
  - Software Development
tags:
  - Git
  - Versioning Control
---

To remove a file from the last pushed commit:

```bash
git rebase -i HEAD~1
```

In the editor, change `pick` to `edit`, save and close. Then:

```bash
git rm --cached <file>        # removes from tracking only

# or

git rm <file>                 # removes from tracking + disk
git commit --amend
git rebase --continue

git push --force-with-lease   # force push to overwrite remote
```

- **Note**: `--force-with-lease` is safer than `--force` as it fails if someone else pushed in the meantime. If it’s a shared branch, warn your team before force-pushing.

## But All Traces of the File’s Commit Aren’t Gone

Indeed, the file’s blob object still exists in `.git/objects`. Git stores content as objects, and even after rewriting history, the old objects remain as **dangling/unreachable objects** until garbage collected.

To purge it (important if the file contained secrets):

```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

This removes unreachable objects from the local repository. But if you already pushed the original commit, the object may still exist on the remote (GitHub retains dangling objects for a while).
Therefore, for secrets, you should rotate them regardless.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Git Logo by Jason Long is licensed under the Creative Commons Attribution 3.0 Unported License.
