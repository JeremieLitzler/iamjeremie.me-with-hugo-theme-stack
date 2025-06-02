---
title: "How To Edit Multiple Git Commit Messages"
description: "I rushed in my commit the other day and I forgot to specify the commit type… Here’s how you should do it."
image: 2025-04-11-a-branch-like-canal.jpg
imageAlt: A branch-like canal
date: 2025-04-11
categories:
  - Software Development
tags:
  - Git
---

To edit several commit messages in Git, you can use **interactive rebase**. This method allows you to modify the commit history and update the messages for multiple commits. Below are the steps to achieve this:

- Start an Interactive Rebase
- Choose Commits to Edit
- Edit Commit Messages
- Complete the Rebase
- Push Changes

Let’s detail all these steps.

## Start an Interactive Rebase

Run the following command to start an interactive rebase for the last **`N`** commits (replace **`N`** with the number of commits you want to edit):

```bash
git rebase -i HEAD~N
```

This will prompt your text editor to open.

## Choose Commits to Edit

In the file that opened, you’ll see a list of the last **`N`** commits in reverse order (most recent at the top).

Each commit will be prefixed with **`pick`**. To edit a commit message, replace **`pick`** with **`reword`** for the corresponding commit.

For example, in my case, I wanted to `reword` all commits with a missing conventional commit type:

```plaintext
reword e499d89 restyle page login to fix buttons
reword 0c39034 restyle page settings and profiles/[username]
pick d7136fb fix: editing a subentity does refresh entities and its subentities list
reword f7fde4a restyle page subentity
```

After you specified the commit to edit, you can save and close the file.

## Edit Commit Messages

After closing the file, Git will pause at each commit marked with **`reword`**, opening your default text editor for you to modify the commit message.

Update the message as needed, save, and exit.

## Complete the Rebase

Once all messages are edited, Git will replay the commits and complete the rebase. If there are no conflicts, your changes will be finalized.

This step requires no action from you.

## Push Changes

If you have already pushed these commits to a remote repository, you’ll need to force-push to update the remote history:

```bash
git push --force
# or
git push --force-with-lease
```

Please note: force-pushing rewrites history and can affect other collaborators. Use it carefully. Often it isn’t allowed on the repository because you can mess things up if you aren’t careful.

If you perform a simple `git push`, your push will fail with an error because the local history has been rewritten and no longer matches the remote branch’s history. This is due to Git’s default behavior of rejecting non-fast-forward updates to prevent overwriting changes on the remote branch [[1](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/changing-a-commit-message)][[2](https://www.atlassian.com/git/tutorials/rewriting-history)].

To successfully update the remote branch with your rewritten history, you must use **`git push --force`** or **`git push --force-with-lease`**. These commands overwrite the remote history with your local changes. If you skip this step, the remote branch remains unchanged, and no new commits are created.

Here is a summary of both options:

| **Feature**              | `git push --force`                             | `git push --force-with-lease`                                                                                                                      |
| ------------------------ | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Safety**               | Low: Overwrites remote history unconditionally | High: Checks remote state before overwriting                                                                                                       |
| **Use Case**             | Solo work, emergency fixes                     | Collaborative work, rebasing/squashing                                                                                                             |
| **Overwrite Prevention** | No                                             | Yes: Rejects push if remote has new commits                                                                                                        |
| **Lease Reference**      | Not supported                                  | Optional: Specify expected remote commit[](https://safjan.com/understanding-the-differences-between-git-push-force-and-git-push-force-with-lease/) |
| **Dry Run**              | No                                             | Supported via **`--dry-run`**                                                                                                                      |

If you ran **`git pull`** after rewriting your commit history (e.g., via an interactive rebase), Git attempted to merge the remote branch’s history with your rewritten local history. This process likely created **merge commits** to reconcile the differences between the two histories, as the local and remote branches had diverged due to the rebase.

After this merge, you were able to push because your local branch was now aligned with the remote branch, but it included additional merge commits that preserved both histories (the original remote history and your rewritten local history).

You then say: “That’s no good, I want a clean and correct history”.

## But Many Repositories Enforce Protected Branch Rules

Yes, they do and both `--force` and `--force-with-lease` will be rejected if the branch is protected…

Then, the best thing you could do is to implement on your repository a commit linter to force the commit message to follow the conventional commit rules.

Then, no need to rewrite history. I’ll try to implement that on my personal repositories soon to serve as a good practice and automatic reminder to follow conventional commit rules 😊

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Kashif Shah](https://www.pexels.com/photo/aerial-view-of-irrigation-canals-in-punjab-pakistan-31454645/)
