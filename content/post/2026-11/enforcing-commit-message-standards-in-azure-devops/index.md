---
title: "Enforcing Commit Message Standards in Azure DevOps"
description: "Commit messages convey important information, often used to provide the scope of change between version."
image: /images/2026-04-29-logo-of-git-scm.svg
imageAlt: Logo of Git Versioning Software
date: 2026-11-23
categories:
  - Software Development
tags:
  - Versioning Control
---

To write automatically release notes with Git, many use convential commits. Often, you use a software factory like GitHub or Azure DevOps to track features and bugs.

When it comes to commit messages, including important information in this small string (ticket ID, scope, etc) does need the whole team to be on the same page to keep the release note clean.

Let’s see how you can enforce a commit message policy.

## Enforcing Git Commit Messages On Azure DevOps Repositories

If you're using Azure DevOps Server (on-premises), you can implement server-side Git hooks. However, this isn't available in Azure DevOps Services (cloud).

So how do you enforce the whole team commit with consistent messages?

You can use `commit-msg` hook on developers' local machines. For that, create a `.git/hooks/commit-msg` file in each developer's local repository.

This validates messages before they're committed locally.

For example, the following `commit-msg` hook will ensure the messages follow the conventional commit message struture:

```bash
#!/bin/sh
commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore): .{10,}$"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "Error: Commit message doesn't follow conventional commit format"
    echo "Format: <type>: <description>"
    exit 1
fi

```

## Custom Enforment Rules

If your team doesn't follow conventional commit rules, you can tweak the regular expression:

```bash
#!/bin/sh

commit_msg=$(cat "$1")

# Pattern: #[work_item_id]-commit-type: [message <= 34 chars]
# Examples:
#   #1234-feat: add user login
#   #5678-fix(auth): resolve token issue
pattern="^#[0-9]+-[a-z]+(\\([a-zA-Z0-9_-]+\\))?: .{1,34}$"

if ! echo "$commit_msg" | head -n 1 | grep -qE "$pattern"; then
    echo "❌ Error: Commit message doesn't follow the required format"
    echo ""
    echo "Required format:"
    echo "  #[work_item_id]-commit-type: [message]"
    echo ""
    echo "Rules:"
    echo "  - Must start with # followed by work item ID (numbers only)"
    echo "  - Commit type (e.g., feat, fix, docs, refactor, test, chore)"
    echo "  - Optional scope in parentheses (e.g., (auth), (api))"
    echo "  - Message must be 1-34 characters long"
    echo ""
    echo "Valid examples:"
    echo "  #1234-feat: add user login"
    echo "  #5678-fix(auth): resolve token issue"
    echo "  #9012-docs: update README"
    echo ""
    echo "Your message:"
    echo "  $commit_msg"
    exit 1
fi

exit 0

```

Anything that doesn't match the pattern will fail the `git commit -m` command.

## Ensuring the Rule is Applied For All

Since `.git/hooks` isn't tracked by Git, you have an option that requires a single step to make sure the commit message rule is enforced:

1. create a directory `.githooks/` at the root of the repository.
2. create the `commit-msg` hook with the content above
3. update the `README.md` to communicate the fact that everyone needs to run this command when cloning the repository:

```sh
git config core.hooksPath .githooks
```

Another idea would be to include a `initial-repo-setup.sh` to run once you cloned the repository:

```bash
#!/bin/sh
# setup.sh - Run this after cloning

echo "🔧 Setting up repository..."

# Configure hooks path
git config core.hooksPath .githooks
echo "✅ Git hooks configured"

# Make hooks executable
chmod +x .githooks/*
echo "✅ Hooks are executable"

echo ""
echo "🎉 Setup complete! You're ready to commit."

```

## Conclusion

On a project with several persons working together, enforcing a good strategy to use consistent commit message is a best practice, but it need to be discussed, because opinions often vary from a person to another.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit:
