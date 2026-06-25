---
title: "First use of graphify to map this Hugo site"
description: "graphify builds a knowledge graph that Claude Code can use in tasks you give it. But you need to know a few things."
image: 2026-06-25-first-use-graphify.jpg
imageAlt: "A network of connected nodes representing a knowledge graph"
date: 2026-06-25
categories:
  - Artificial Intelligence
tags:
  - graphify
  - Claude Code
draft: true
---

I ran graphify for the first time on my own Hugo site to turn the templates, scripts and drafts into a navigable knowledge graph. Here is what happened, step by step.

## What graphify does

graphify takes a folder of files (code, docs, papers, images, video) and builds a queryable knowledge graph out of it: it extracts entities and relationships, detects communities, surfaces the most connected "god nodes", and produces three outputs — an interactive HTML graph, a raw `graph.json`, and an audit report (`GRAPH_REPORT.md`). Everything lands in a `graphify-out/` directory.

## Setting It Up

### Step 1: Detecting the corpus

The very first scan of the repository root found a lot more than I expected:

- **1,414 files** and **~8.96M words**
- 29 code files, 473 documents, **912 images**

That is well over graphify's thresholds (more than 2M words and more than 500 files), so it warned me and asked which subfolder to narrow to. The breakdown by top-level folder made the problem obvious:

| Folder    | Files |
| --------- | ----: |
| `content` |  1045 |
| `themes`  |   179 |
| `static`  |   120 |
| `layouts` |    29 |
| `_drafts` |    24 |

The `content/` folder (my published blog posts and all their images) was the bulk of it.

### Step 2: Narrowing the scope with `.graphifyignore`

Rather than graph 1,000+ published posts, I excluded `content/` by adding a `.graphifyignore` file:

```text
content/
```

That dropped the corpus to **345 files / ~1M words**, but it still left **161 images** — mostly the theme's demo assets and decorative files in `themes/` and `static/`. Since graphify runs a separate vision pass on _every_ image, that would have meant roughly 161 extra agent calls for very little graph value. So I excluded images too:

```text
content/
*.png
*.jpg
*.jpeg
*.gif
*.svg
*.webp
*.ico
*.avif
*.bmp
*.tiff
```

My final corpus was **184 files** — 26 code files and 158 documents, about 42K words.

### Step 3: Extraction

Extraction ran in two passes:

1. **Structural (AST)** on the code files > deterministic and free. It produced **314 nodes and 950 edges**.
2. **Semantic (LLM)** on the 158 documents. Since I had no Gemini key set, graphify dispatched **8 Claude subagents in parallel**, each handling a chunk of ~20 files grouped by directory. The Hugo `.html` templates, the i18n YAML tables, the theme config and my draft posts were all read this way.

Merging the two passes (and de-duplicating shared nodes like `helper/icon`) gave a final extraction of **514 nodes and 1,152 edges**, costing about **316K input tokens**.

### Step 4: The graph

After building, clustering and labelling, the graph cleanly separated four worlds:

- the **hugo-theme-stack structure** (templates, partials, widgets, comment providers, render hooks),
- the **TypeScript source** (search, color scheme, gallery, scrollspy),
- and my **custom site overrides** (Tally contact form, Stripe donate, Substack optin, image conversion, Netlify CMS and the scheduled-publish function).

### An honest caveat

The health check flagged about 143 collapsed/duplicate edges and a self-loop. Almost all of it came from the **minified vendor JavaScript** in `static/js` (KaTeX, Mermaid, Vibrant, PhotoSwipe): the AST parser turns their single-letter functions into noise. There were also 26 dangling cross-chunk references. The graph is perfectly usable, but the "minified JS" communities and most of the god nodes below are vendor artifacts, not my own code.

This produced the following edges:

1. `qa()` — 50 edges
2. `Ps()` — 48 edges
3. `Ms()` — 43 edges
4. `Gs()` — 40 edges
5. `ys()` — 26 edges
6. `zr()` — 23 edges
7. **`Search`** — 15 edges
8. `aa()` — 14 edges
9. `vr()` — 13 edges
10. `po()` — 13 edges

Numbers 1-6 and 8-10 are minified-bundle internals. `Search` is the one genuine hub — my theme's client-side search class.

So I added the `static/js/` folder the ignore list.

## Suggested questions

These are the questions graphify thinks the graph is uniquely positioned to answer:

- **What is the exact relationship between `sidebar/right.html` and `Pagination`?** (an ambiguous edge, flagged for review)
- **Why does `helper/image` bridge "Theme article components & widgets" and "Page templates & article layout"?** (high betweenness > a real architectural bridge in my code)

I'll address them later.

## Does It Really Save Tokens

## My Takeaways

- `.graphifyignore` is essential: pointing it at `content/`, `static/js/` and image files took the run from intractable to fast.
- The AST pass is great for real code, but **minified vendor bundles pollute the graph**.
- The genuinely useful signal was about **my own overrides versus the upstream theme**, and how the custom features (contact form, donate, Substack, image conversion) cluster together.

The interactive graph (`graphify-out/graph.html`) is the real payoff — a map I can navigate instead of a report I read once.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
