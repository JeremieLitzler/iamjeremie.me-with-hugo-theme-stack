# Project instructions

## Two knowledge graphs — pick the right one per request

This repo has **two separate graphify graphs**, each scoped to a different concern. When a
question could be answered from a graph, choose by subject:

| If the question is about…                                                                 | Use this graph                       | Query from                |
| ----------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------- |
| **How the website is built** — layouts, partials, shortcodes, the Hugo theme, assets (TS/CSS), config, build/deploy, search, taxonomy templates | `graphify-out/` (root)               | repo root                 |
| **The written content** — articles/posts/quick-tips, their topics, tags, what I've written about (gardening, .NET, Vue, Python, DevOps…), cross-article links | `content-graph/graphify-out/`        | the `content-graph/` dir  |

`graphify query` uses the `graphify-out/` in the **current working directory**, so the cwd
selects the graph: query the root graph from the repo root; `cd content-graph` first to query
the content graph. If a request spans both ("does any article document how the theme renders
math?"), query both and say which graph each fact came from. If genuinely ambiguous, ask.

## Keeping the two graphs scoped when rebuilding

- **Root build graph** (`/graphify` or `/graphify --update` at repo root): the root
  `.graphifyignore` excludes `content/` and `content-graph/`, so a rebuild only sees site
  machinery and never ingests prose or the content graph's own outputs. Nothing extra needed.
- **Content graph**: the `content/` exclusion above would make a plain `graphify content` run
  find zero files, so it has its own driver that enumerates `content/` markdown directly:

  ```bash
  cd content-graph
  python build_content_graph.py plan       # detects docs, checks cache, writes chunklists
  #   -> for each .graphify_chunklist_NN.txt the cache missed, dispatch one
  #      general-purpose subagent (see build_content_graph.py header) to write
  #      .graphify_chunk_NN.json. A no-change update reports 0 uncached — skip this step.
  python build_content_graph.py finalize    # merge + build + cluster + report
  graphify export html
  ```

  It is **docs-only** (the 743 co-located images are intentionally skipped). The semantic cache
  makes updates incremental — only new/changed articles get re-extracted. Curated community
  names live in `content-graph/labels-override.json` (keyed by each community's central node id
  so they survive renumbering).
