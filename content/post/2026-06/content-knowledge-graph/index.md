---
title: "How To Persist Two Distinctly Scoped Graphs With Graphify"
description: "I already had a graphify map of how my site is built. Here is how I added a second one for what I actually write, kept the two from stepping on each other, and taught Claude which one to use."
image: 2026-06-30-content-knowledge-graph.png
imageAlt: "Two separate clusters of connected nodes, one for code and one for articles"
date: 2026-06-30
categories:
  - Artificial Intelligence
tags:
  - graphify
  - Claude Code
draft: true
---

Last week, [I graphed how this Hugo site is built](../first-use-graphify/index.md): the templates, the theme, my custom overrides. To keep that run useful I deliberately excluded `content/` with a `.graphifyignore`, because graphing 300+ published posts (and all their images) was out of scope.

But I needed to the content graph. So could `graphify` handle two graphs in the same repository, each with a clear scope. The first graph knows everything about _how_ the site works and nothing about _what_ I have actually written.

So this week I built a second graph, scoped to the articles only, and made sure the two never collide.

But why two graphs? Well, I need to make a big fix on my blog so I make Google Search happy in terms of SEO. So I need to add a new frontmatter property called `seoNoIndex` that I can toggle to disable my summaries around the gardening and composting and find the favors of Google to reindex all the rest of my content.

Let's go with this graph scoping task for now!

## Why two graphs instead of one

The two questions I ask are different, and mixing them only adds noise:

- "How does the site render math?" is about layouts, partials and TypeScript.
- "What have I written about no-dig gardening?" is about prose, topics and tags.

One big graph would smear those together, which doesn't sense. Two scoped graphs keep each answer clean:

| Graph                         | Scope                                          |
| ----------------------------- | ---------------------------------------------- |
| `graphify-out/` (the first)   | site machinery: layouts, theme, assets, deploy |
| `content-graph/graphify-out/` | the articles: posts, quick-tips, topics, tags  |

## The catch: the ignore that scoped the first graph killed the second

My first instinct was simply to run graphify on `content/`. It found **zero files**.

The reason is the very `.graphifyignore` that made the first graph work. graphify reads ignore rules from the repository root down, so the `content/` line I added last week applies to _any_ run inside this repo, including one I explicitly point at `content/`. The exclusion I wanted for the build graph was sabotaging the content graph.

So the content graph needs its own scope, in its own place, without me deleting the rule the build graph depends on.

## Building it, documents only

The fix was to give the content graph a separate home — a `content-graph/` folder with its own `graphify-out/` inside — and to enumerate the markdown directly instead of going through the ignore that blocks it.

Before spending any tokens, I checked what `content/` actually holds:

- **301 markdown articles**, about **229K words**
- **743 images**

That image count is the trap. `graphify` runs a vision pass on _every_ image, so "everything in `content/`" really means hundreds of extra agent calls on screenshots that add almost nothing to a map of _topics_. I skipped them and kept the run to documents only.

The 301 articles were split into 14 chunks of ~22 files, each handed to a Claude subagent running in parallel. About **1.38M tokens** later, and a few bucks of extra credits purchased, the merged graph was **1,031 nodes and 1,079 edges across 132 communities**.

And it is genuinely _my_ writing this time. The two heaviest hubs say it all:

- `Charles Dowding` and `Compost` (17 edges each) > my no-dig gardening notes
- `Software Development` and `Web Development` categories > the dev side

Two gravity wells, gardening and software, which is a fair summary of this blog.

## Keeping the two from colliding

With a second `graphify-out/` now living under `content-graph/`, the build graph would happily swallow it on its next rebuild. So I made the scoping explicit on both sides:

- The build graph's `.graphifyignore` now excludes **both** `content/` **and** `content-graph/`, so rebuilding it never pulls in prose or the content graph's own output.
- The content graph only ever scans `content/`, so the theme and layouts are out of range by construction.

Each graph is now blind to the other's scope.

## An honest caveat: the cache leaked into `content/`

The first build dropped a `graphify-out/` _inside_ `content/`, which is exactly the tree I am trying to keep clean. graphify derives its cache location from the folder it scans, and I was scanning `content/`.

The cure was to point graphify's output path at `content-graph/` with the `GRAPHIFY_OUT` environment variable, so the cache lands where it belongs. I also had to fix `.gitignore`: its `graphify-out/*` rule is anchored to the repository root, so it never covered the nested folders. Now the content graph follows the same policy as the first one — commit the durable `graph.json` and `GRAPH_REPORT.md`, ignore the cache, the HTML and the machine-local files.

## Making updates repeatable

I did not want this to be a one-off I have to reconstruct by hand every time I publish. So the deterministic part lives in a small driver script with two steps:

```bash
cd content-graph
python build_content_graph.py plan       # find articles that changed
python build_content_graph.py finalize    # rebuild the graph from the cache
graphify export html
```

`plan` checks the cache and only flags new or edited articles for extraction, so a no-change rebuild costs **zero** subagent calls. The curated community names are stored separately, keyed by each cluster's most central node, so they survive a rebuild even when the cluster numbers shift.

## Teaching Claude which graph to use

The last piece was making sure Claude Code picks the right map without me spelling it out each time. I wrote the rule into a project `CLAUDE.md`:

- A question about **how the site is built** > query the root graph.
- A question about **what I have written** > query the content graph.

The trick is simply the working directory: `graphify query` reads whichever `graphify-out/` sits in the current folder, so changing directory into `content-graph/` switches maps. If a question genuinely spans both, the instruction is to query each and say which graph each fact came from.

## My takeaways

A single ignore rule can scope one graph and silently break another. Scope by **where you put the output**, not only by what you exclude.

For a map of _topics_, skipping images is not a compromise, it is the point. The text carries the signal.

The real win is the same as last time: I now have a navigable map of my own writing, and an assistant that knows when to reach for it.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
