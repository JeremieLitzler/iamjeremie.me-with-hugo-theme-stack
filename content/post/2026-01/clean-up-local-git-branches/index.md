---
title: "Clean Up Local Git Branches"
description: "If you complete many features of an application or resolve many bugs, your local repository can become cluttered with local Git branches."
image: 2026-01-19-flowers-of-a-magnolia-tree.jpg
imageAlt: Flowers of a magnolia tree
date: 2026-01-19
categories:
  - Tools
tags:
  - Git
  - Bash
---

As I was working on [my Vue and Supabase Boilerplate project](https://github.com/JeremieLitzler/VueSupabaseBoilerplate), I completed many features. I needed to have a script that would remove any local branch not named `main` or `develop` or that wasn’t the checked-out branch or that didn’t have a remote equivalent.

Yes, what follows will remove any branch that you may have created and not yet pushed ⚠️. So be careful.

Let’s see how to speed up the clean-up process.

## The Bash Script

I love bash scripts to do small tasks like this. With it, you can achieve so much without any new software or service. Using Git Bash, which comes with Git by default, you can run the following:

```sh
#!/bin/bash

# Default to dry-run mode
DRY_RUN=true

echo "Parse command line arguments"
while [[ "$#" -gt 0 ]]; do
    case $1 in
        # The "-D" parameter will set the dry run variable to false.
        -D) DRY_RUN=false ;;
        # Anything else fails
        *) echo "Unknown parameter: $1. Use `-D` to execute actual branch clean up"; exit 1 ;;
    esac
    shift
done

echo "Fetch all remotes to ensure we have latest information"
git fetch --all

echo "Get list of remote branches (strip refs/remotes/origin/ prefix)"
REMOTE_BRANCHES=$(git branch -r | sed 's/origin\///' | tr -d ' ')
echo $REMOTE_BRANCHES
echo ""

echo "Now, process each local branch"
# The variable `branch` comes from the last line in the loop
# and represents the current iteration of the `git branch` ouput
while read -r branch; do
    # Clean branch name (remove leading spaces and asterisk)
    branch_name=$(echo "$branch" | sed 's/^* //;s/^ *//')
    # Set is_current if branch name has "*", meaning it is the checkout branch
    is_current=$(echo "$branch" | grep -q "^\*" && echo true || echo false)

    [[ -z "$branch_name" ]] && echo "Skip branch because is empty" && continue

    [[ "$branch_name" == "develop" || "$branch_name" == "main" ]] && echo "Skip branch because is develop or main" && continue

    echo "Check if <$branch_name> exists on remote"
    if ! echo "$REMOTE_BRANCHES" | grep -q "^${branch_name}$"; then
        if [ "$DRY_RUN" = true ]; then
            echo "Would delete branch: <$branch_name>"
        else
            if [ "$is_current" = true ]; then
                echo "Skipping current branch: <$branch_name>"
            else
                echo "Deleting branch: <$branch_name>"
                git branch -D "$branch_name"
            fi
        fi
    else
        echo "Remote branch exists for <$branch_name>. Skip delete."
    fi
# Runs the `git branch` command to list all local branches
done < <(git branch)
```

## A Little Caveat With Former Remote Branches

If you run the script and you have had remote branches deleted, after a PR completion, for example, you may notice that some branches are flagged: “Remote branch exists for `a-branch`” but they really don’t exist anymore.

What’s going on?

### How Remote References Work

Remote-tracking branches are local references that represent the state of branches in your remote repository. They act as bookmarks to remember where the remote branches were during your last synchronization (see [Git documentation](https://git-scm.com/book/pt-pt/v2/Ramifica%C3%A7%C3%A3o-do-Git-Remote-Branches)).

When someone deletes a branch on the remote server, your local repository won’t automatically remove its reference to that branch until you explicitly prune it (read [more about branch pruning](https://hswolff.com/blog/prune-remote-git-branches/)).

These remote-tracking references are stored locally in your `.git/refs/remotes/` directory (or in the `.git/packed-refs` file for optimized storage), while your remote configuration settings are kept in `.git/config`. They’re managed separately from the actual remote repository state.

This separation is why you need to explicitly tell Git to clean up these references when they become stale.

### Updating Remote References

There are several ways to update these stale references:

- Using `git fetch with prune`

```bash

git fetch --prune
# Short hand version
git fetch -p
```

This command fetches updates from the remote repository and removes any remote-tracking references that no longer exist on the remote.

- Using `git remote prune`

```bash
git remote prune origin
```

This command specifically removes stale remote-tracking branches without fetching new updates.

- Enable Automatic Pruning

To automatically prune stale references whenever you fetch or pull, you can configure Git with:

```bash
git config --global fetch.prune true
```

This setting ensures your remote branch references stay clean without manual intervention.

## Conclusion

All you have to do now is to create a file `clean-git-local-branches.sh` and run it.

```sh
sh ./clean-git-local-branches.sh
```

Then, once you’re satisfied with the dry run, run the script with `-D` to effectively delete the local branches.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Francesco Ungaro](https://www.pexels.com/photo/branches-of-tree-with-magnolia-flowers-7492107/).
