---
title: "First Steps Pushing Dotfiles With Chezmoi"
description: "I already knew how to pull my dotfiles down with chezmoi. Sending a local change back to the remote repo turned out to be a two-step dance I had to learn. Here are my baby steps."
image: 2026-08-14-a-child-taking-a-small-steps-up-a-staircase.jpg
imageAlt: A child taking a small steps up a staircase
date: 2026-08-14
categories:
  - Software Development
tags:
  - Chezmoi
  - Dotfiles
  - Git
  - Command Line
---

I’m making baby steps with [chezmoi](https://www.chezmoi.io/), the dotfiles manager. I already had a dotfiles repository set up with a minimal setup\. I initialized it from a laptop I needed to reset but needed to keep my development setup. I was comfortable with one half of the workflow: pulling changes from the remote and applying them to my reset machine.

What I hadn’t figured out yet was the other half—how do I save a change I made _locally_ back to the remote? Indeed, I didn’t use the steps I’m going to describe below while setting up the initial files.

It turns out the answer is short, but it only makes sense once you own the mental model. So let me walk through the small steps I just took.

## The Mental Model

The thing that confused me at first is that chezmoi juggles two different “states,” and I only understood one of them.

There is the **source state**, which lives in chezmoi’s own git repository—usually at `~/.local/share/chezmoi`. This is my dotfiles repository checkout. Then there is the **target state**, which is the actual dotfiles sitting in my home directory: `~/.bashrc`, my editor config, my Claude setup and so on.

Once I saw it that way, the commands I already used made sense. When I run:

```bash
chezmoi update
```

chezmoi is really doing two things in sequence:

- It runs `git pull --autostash --rebase` in the source directory,
- Then it applies the changes to my home directory. One command, two operations. That is why pulling always felt effortless—chezmoi collapsed the two steps into one for me (read [chezmoi daily operations](https://www.chezmoi.io/user-guide/daily-operations/) for the full documentation).

What about going the _other_ direction has no single command? Well, it didn’t happen so. I have to do the two stages myself.

## Capturing a Local Change Into the Source

Say I edited `~/.bash_profile` directly, the way I normally would. chezmoi doesn’t know anything happened yet, because I changed the target state, not the source state. To bring that edit back into the source repository, I run `chezmoi add` with the path:

```bash
chezmoi add ~/.bash_profile
```

I first assumed I had to `cd` into the folder where the dotfile lives before adding it. I didn’t. `chezmoi add` takes a path, so I can run it from anywhere and let chezmoi resolve the location itself.

The neat part is that, for a file that chezmoi _already_ manages, `chezmoi add` simply re-imports it, picking up my local edits. That is exactly what I imagined.

## Versioning and Pushing

Capturing the change into the source repository is only stage one. The file is now updated inside `~/.local/share/chezmoi`, but that is still just a local git repository. To version it, I jump into that repository and use plain git:

```bash
# drops me into the source repo
chezmoi cd
# check what's pending
git status
# pick whatever you need before adding
# you may not need everything.
# check first, commit after!
git add dot_bash_profile
git commit -m "add .bash_profile"
git push
# leave the chezmoi shell
exit
```

`chezmoi cd` opens a subshell already sitting in the source directory, so the git commands are ordinary from there.

**Important:** When I’m done, `exit` takes me back to where I started. If you see that the Git Bash (which I was using) behaves very slowly, then you didn’t run the steps of the above code block.

Before committing, you preview what actually changed with:

```bash
chezmoi diff
```

That shows the difference between the source and the target, so I can confirm I’m about to version the right thing.

## The lazy option I might grow into

There is a way to let chezmoi handle the git steps for me. Two variables in the `git` section of `~/.config/chezmoi/chezmoi.toml` control it:

```toml
[git]
    autoCommit = true
    autoPush = true
```

Per the reference, `autoCommit` will “commit changes to the source state after any change,” and `autoPush` will “push changes to the source state after any change”—both default to `false` ([configuration variables](https://www.chezmoi.io/reference/configuration-file/variables/)). With those on, any `chezmoi add`, `re-add`, or `edit` commits—and pushes—automatically.

For now I’m leaving them off. As a beginner I would rather see my `git status` and commit deliberately than have things fly off to the remote behind my back. Plus, I might not need everything from a dot file or dot folder.

## Conclusion

The whole outgoing workflow turned out to be four small moves: `chezmoi add` the file into the source, `chezmoi cd` into the repository, commit with git, and push. Pulling was one command because chezmoi hides the seam; pushing just asks me to see the seam for myself. That is the baby step I took today, and my dotfiles repository gets richer by the day as I learn to CLI my work.

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Jep Gambardella on Pexels (`https://www.pexels.com/photo/a-cute-little-boy-sitting-on-the-wooden-stairs-while-looking-afar-6224250/`).
