---
title: "Rebase vs. Merge With Git"
description: "Understanding the two concepts will help you understand when to use rebase or merge with Git versioning system."
image: 2026-01-12-a-forest-with-trees.jpg
imageAlt: A forest with trees
date: 2026-01-12
categories:
  - Software Development
tags:
  - Git
---

I needed to understand the two methods because I’ve always used the merge method, thinking that the `rebase` wasn’t efficient or dangerous based. I’ve read.

But the truth was more nuanced.

The choice between rebasing and creating merge commits depends on your specific needs and workflow. So let’s review what each method brings.

## Rebase Benefits

The first thing you read about `rebase` is that it creates a cleaner, linear commit history. In fact, `rebase` allows you to rewrite the history.

Finally, it eliminates unnecessary merge commits, you know the “Merged from PR xxxxxx” messages after you’ve merged a feature branch into `develop`.

## Merge Benefits

First, `merge` method will preserve the complete repository’s history. Hence, it makes it easier to track feature implementation.

It also makes conflict resolution easier, though I came to learn how to perform a `rebase` with little conflict resolution difficulty.

Then, it’s easier to undo if mistakes occur.

Finally, it maintains accurate timestamps of commits.

## When to Use Rebase

The main reason I’ve seen so far using `rebase` is to maintain a clean, linear project history.

Also, when you deal with smaller, focused changes that need to be integrated cleanly, you can use `rebase`. I’ve looked at the commit history of several open source projects and in none of them did I see a “Merged PR xxxx” commit message.

## When to Use Merge

Though it’s recommended not to have long-living branches, using `merge` is a better option in this scenario.

Also, when multiple developers are collaborating on the same branch, this method makes it easier to work. Again, that really depends on what you’re doing because, with a team working on distinct features, each individual should almost always work on a distinct branch, specific to a given feature and bug fix.

Also, `merge` doesn’t rewrite history, like `rebase` does, so use when you need to preserve the exact history.

Some have said when you want simpler conflict resolution, using `merge` will help. Though I believe that you can resolve conflicts easily with `rebase` using `squash` on your feature branch. That applies to the case when you want to update your feature branch that is behind `develop`. Yes, `squash` to combine multiple commits into a single.

If you really want to keep your atomic commits, if you use that commit method, then yes, merging `develop` into your feature branch may be more challenging to resolve conflicts. However, atomic commits don’t mean one commit per file, which I believed to be a few years ago.

## Best Practice Recommendations

If you’re ever in doubt, it’s recommended to use merge instead of `rebase` due to its lower risk and easier recovery options. However, if you’re working on a feature branch alone and haven’t pushed it to remote yet, consider rebasing to clean up your commits before creating the pull request.

Remember that both approaches will successfully integrate your changes—the main difference lies in how the project’s history appears and how conflicts are handled.

## Practical Examples

I’ll provide a complete series of steps covering the various use cases when to use `rebase` and merge with the hypothesis that :

- we work on a simple git repository a single text file
- we want to emulate a big team with parallel feature development
- we want to test a revert

### Initial Setup

```bash
#Create and initialize repository
mkdir git-demo && cd git-demo
git init
echo "Initial content" > file.txt
git add file.txt
git commit -m "Initial commit"
```

### Scenario 1: Feature Branch Development

```bash
# Create and switch to feature branch
git checkout -b feature/simple-scenario
echo "Feature A content" >> file.txt
git commit -am "Add feature A"

# Meanwhile, main branch gets updated (simulating team work)
# Of course, you should NEVER push directly to develop...
git checkout main
echo "Hotfix content" >> file.txt
git commit -am "Add hotfix"

# Something happens on main
git checkout main
git pull

# Rebase approach (recommended for feature branches)
git checkout feature/simple-scenario
# Rewrite the history, no "merge" commit
git rebase main

# Alternative: Merge approach
git checkout feature/simple-scenario
# This create a "merge" commit.
git merge main
```

### Scenario 2: Parallel Feature Development

```bash
# Create two parallel features
git checkout main
git checkout -b feature/parallel-1
echo "Feature B content" >> file.txt
git commit -am "Add feature B"

git checkout main
git checkout -b feature/parallel-2
echo "Feature C content" >> file.txt
git commit -am "Add feature C"

# Merge feature/parallel-1 first (simulating PR merge)
git checkout main
git merge feature/parallel-1

# Now feature/parallel-2 needs updating
git checkout feature/parallel-2
git rebase main
```

### Scenario 3: Interactive Rebase for Cleanup

```bash
# Create feature with messy commits
git checkout -b feature/with-many-commits
echo "Feature: Basic reporting" >> file.txt
git commit -am "WIP: Start reporting"
echo "Feature: Advanced reporting" >> file.txt
git commit -am "Fix typo"
echo "Feature: Report export" >> file.txt
git commit -am "Actually add reporting feature"
echo "Feature: Report scheduling" >> file.txt
git commit -am "Oops forgot this part"

# Clean up with interactive rebase
# This combines all commits into one clean commit
git rebase -i HEAD~4
# In the editor, mark commits as 'squash' except the first
# then reword commit messages to keep one

# After cleanup, merge to main
git checkout main
git merge feature/with-many-commits
```

### Scenario 4: Revert With Merge

```bash
# Create a feature and merge it
git checkout main
git checkout -b feature/bad
echo "Bad feature content" >> file.txt
git commit -am "Add bad feature"
git checkout main
git merge feature/bad

# Create new feature from reverted main
git checkout -b feature/fixed-feature

# Revert the merge
git revert -m 1 HEAD

echo "Fixed feature content" >> file.txt
git commit -am "Add fixed feature"
```

### Scenario 5: Revert With Rebase

We can have three variations of this:

#### Method A: Interactive Rebase to Drop Commits

```bash
# Setup: Create and merge a feature we'll want to revert
git checkout main
git checkout -b feature/bad-feature
echo "Feature: Problematic feature" >> file.txt
git commit -am "Add problematic feature"
git checkout main
git merge feature/bad-feature

# Add more work after the bad feature
echo "Feature: Good feature after bad" >> file.txt
git commit -am "Add good feature"

# Now we want to remove the bad feature using rebase
# Use interactive rebase to drop the bad commit
git rebase -i HEAD~2

# In editor, delete the line with "Add problematic feature" or mark it as 'drop'
# Save and exit
# Manually fix any conflicts if they arise
# The bad feature commit is now removed from history
```

When the feature hasn’t been pushed to a shared repository, or you have a team agreement to rewrite history, this method can be used.

#### Method B: Rebase onto Earlier Point

```bash
# Setup scenario
git checkout main
echo "Before bad feature" >> file.txt
git commit -am "Commit before bad feature"

GOOD_COMMIT=$(git rev-parse HEAD)

echo "Bad feature content" >> file.txt
git commit -am "Bad feature we want to remove"

echo "Another commit" >> file.txt
git commit -am "Commit after bad feature"

# Create a temporary branch at current position
git branch temp-current

# Reset to before bad commit
git reset --hard $GOOD_COMMIT

# Cherry-pick the commits we want to keep
git cherry-pick temp-current

# If there are conflicts, resolve them

# Delete temp branch
git branch -D temp-current
```

This variation helps you remove a specific commit and keep everything else, especially with a complex history.

#### Method C: Rebase with `--onto` to Remove Middle Commits

```bash
# Setup
git checkout main
echo "Commit A" >> file.txt
git commit -am "Commit A"

echo "Bad feature start" >> file.txt
git commit -am "Bad commit 1"

echo "Bad feature continue" >> file.txt
git commit -am "Bad commit 2"

BAD_END=$(git rev-parse HEAD) # Bad commit 2

echo "Good commit after" >> file.txt
git commit -am "Good commit after bad feature"

# Find the commit before bad commits
BAD_START=$(git rev-parse HEAD~3)  # Commit A

# Rebase to remove bad commits
# Syntax: git rebase --onto <new-base> <old-base> <branch>
# This means: take commits after BAD_END and replay them onto BAD_START
git rebase --onto HEAD~3 HEAD~1
```

We use `--onto` when you need surgical precision to remove a range of commits from the middle of your history.

### Scenario 6: Complex Rebase with Conflicts

```bash
# Create conflicting changes
git checkout main
git checkout -b feature/parallel-work
echo "Feature edits line 1" >> file.txt
git commit -am "Feature D change 1"

git checkout main
echo "Main edits line 1" >> file.txt
git commit -am "Main change 1"

# Resolve with rebase
git checkout feature/parallel-work
git rebase main

# If conflicts occur:
# 1. Fix conflicts in file.txt
# 2. git add file.txt
# 3. git rebase --continue
```

### Important Rules

1. Never rebase branches that others are working on
2. Create meaningful commit messages
3. **Always** test after rebasing or merging

## Sources

Here are _some_ articles and forum threads that I looked at on the topic. Do take the time to read them as well.

1. [https://www.tempertemper.net/blog/git-rebase-versus-merge](https://www.tempertemper.net/blog/git-rebase-versus-merge)
2. [https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)
3. [https://stackoverflow.com/questions/804115/when-do-you-use-git-rebase-instead-of-git-merge/64319712](https://stackoverflow.com/questions/804115/when-do-you-use-git-rebase-instead-of-git-merge/64319712)
4. [https://www.gitkraken.com/learn/git/problems/git-rebase-vs-merge](https://www.gitkraken.com/learn/git/problems/git-rebase-vs-merge)
5. [https://www.aviator.co/blog/rebase-vs-merge-pros-and-cons/](https://www.aviator.co/blog/rebase-vs-merge-pros-and-cons/)
6. [https://blog.mergify.com/git-merging-vs-rebasing-the-complete-guide-for-modern-development/](https://blog.mergify.com/git-merging-vs-rebasing-the-complete-guide-for-modern-development/)
7. [https://softwareengineering.stackexchange.com/questions/309919/merge-vs-rebase-pull-requests-on-github](https://softwareengineering.stackexchange.com/questions/309919/merge-vs-rebase-pull-requests-on-github)
8. [https://www.atlassian.com/git/tutorials/merging-vs-rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
9. [https://blog.git-init.com/differences-between-git-merge-and-rebase-and-why-you-should-care/](https://blog.git-init.com/differences-between-git-merge-and-rebase-and-why-you-should-care/)
10. [https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests](https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests)

## Conclusion

If you want an interactive Git learning experience, I recommend [Learning Git Branching](https://learngitbranching.js.org/) website. It’ll guide you, step by step, in a CLI-like web interface, to learn the ins and outs of Git.

Photo by [Hasan Albari](https://www.pexels.com/photo/ray-of-lights-passing-through-trees-1172626/).
