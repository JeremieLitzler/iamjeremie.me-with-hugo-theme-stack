#!/usr/bin/env python3
"""Driver for the CONTENT-ONLY knowledge graph (content-graph/graphify-out/).

Why this exists: the repo-root .graphifyignore excludes content/ on purpose, so the
ROOT build graph stays scoped to site machinery. That same rule would make a normal
`graphify content` run find zero files. This driver enumerates content/ markdown
directly (bypassing only the content/ exclusion) and runs the rest of the graphify
pipeline into content-graph/graphify-out/ — fully separate from the root graph.

Two phases, with LLM extraction of *changed* files in between:

  python build_content_graph.py plan      # detect docs, check cache, write chunklists
                                           # -> prints which files still need extraction
  # (host agent dispatches one general-purpose subagent per chunklist, each writing
  #  .graphify_chunk_NN.json — only needed for files the cache missed)
  python build_content_graph.py finalize   # merge chunks+cache, build, cluster, report, html

A no-change update needs no subagents: `plan` reports 0 uncached, `finalize` rebuilds
from the semantic cache. Curated community names live in labels-override.json (keyed by
each community's most-central node id, so they survive community renumbering).
"""
from __future__ import annotations
import json, math, os, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "graphify-out"
CHUNK_SIZE = 22

# graphify derives its cache dir from the SCAN root (content/), which would drop a
# graphify-out/ inside the content tree. Redirect every graphify path to this folder
# instead — must be set before graphify is imported (graphify.paths reads it once).
os.environ["GRAPHIFY_OUT"] = str(OUT)


def content_root() -> Path:
    root_file = OUT / ".graphify_root"
    return Path(root_file.read_text(encoding="utf-8").strip().lstrip("﻿")).resolve()


def plan() -> None:
    from graphify.detect import classify_file, _is_sensitive, FileType, count_words
    from graphify.cache import check_semantic_cache

    root = content_root()
    docs = sorted(
        str(p) for p in root.rglob("*")
        if p.is_file() and not _is_sensitive(p) and classify_file(p) == FileType.DOCUMENT
    )
    words = sum(count_words(Path(d)) for d in docs)
    OUT.mkdir(parents=True, exist_ok=True)
    detect = {
        "files": {"code": [], "document": docs, "paper": [], "image": [], "video": []},
        "total_files": len(docs), "total_words": words, "needs_graph": True,
        "warning": None, "skipped_sensitive": [], "graphifyignore_patterns": 0,
        "scan_root": str(root),
    }
    (OUT / ".graphify_detect.json").write_text(json.dumps(detect, ensure_ascii=False), encoding="utf-8")

    cn, ce, ch, uncached = check_semantic_cache(docs, root=str(root))
    if cn or ce or ch:
        (OUT / ".graphify_cached.json").write_text(
            json.dumps({"nodes": cn, "edges": ce, "hyperedges": ch}, ensure_ascii=False), encoding="utf-8")
    else:
        (OUT / ".graphify_cached.json").unlink(missing_ok=True)

    # Clear any stale chunk artifacts from a previous run
    for f in OUT.glob(".graphify_chunk_*.json"):
        f.unlink()
    for f in OUT.glob(".graphify_chunklist_*.txt"):
        f.unlink()

    n_chunks = 0
    if uncached:
        chunks = [uncached[i:i + CHUNK_SIZE] for i in range(0, len(uncached), CHUNK_SIZE)]
        for i, ch_files in enumerate(chunks, 1):
            (OUT / f".graphify_chunklist_{i:02d}.txt").write_text("\n".join(ch_files), encoding="utf-8")
        n_chunks = len(chunks)

    print(json.dumps({
        "documents": len(docs), "words": words,
        "cached": len(docs) - len(uncached), "uncached": len(uncached),
        "chunklists": n_chunks,
        "chunk_paths": [str(OUT / f".graphify_chunk_{i:02d}.json") for i in range(1, n_chunks + 1)],
    }, indent=2))


def finalize() -> None:
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json
    from graphify.cache import save_semantic_cache

    root = content_root()
    detect = json.loads((OUT / ".graphify_detect.json").read_text(encoding="utf-8"))

    # Merge any freshly-extracted chunks, persist them to the cache
    new_nodes, new_edges, new_h = [], [], []
    for c in sorted(OUT.glob(".graphify_chunk_*.json")):
        d = json.loads(c.read_text(encoding="utf-8"))
        new_nodes += d.get("nodes", []); new_edges += d.get("edges", []); new_h += d.get("hyperedges", [])
    if new_nodes or new_edges or new_h:
        save_semantic_cache(new_nodes, new_edges, new_h, root=str(root))

    cached = {}
    if (OUT / ".graphify_cached.json").exists():
        cached = json.loads((OUT / ".graphify_cached.json").read_text(encoding="utf-8"))
    all_nodes = cached.get("nodes", []) + new_nodes
    all_edges = cached.get("edges", []) + new_edges
    all_h = cached.get("hyperedges", []) + new_h
    seen, nodes = set(), []
    for n in all_nodes:
        if n["id"] not in seen:
            seen.add(n["id"]); nodes.append(n)
    extraction = {"nodes": nodes, "edges": all_edges, "hyperedges": all_h,
                  "input_tokens": 0, "output_tokens": 0}

    G = build_from_json(extraction, root=str(root), directed=False)
    if G.number_of_nodes() == 0:
        sys.exit("ERROR: extraction produced no nodes")
    communities = cluster(G)
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    labels = _label(G, communities)
    questions = suggest_questions(G, communities, labels)

    if not to_json(G, communities, str(OUT / "graph.json")):
        sys.exit("ERROR: refused to shrink graph.json (content removed?). Delete graph.json to force.")
    report = generate(G, communities, cohesion, labels, gods, surprises, detect,
                      {"input": 0, "output": 0}, str(root), suggested_questions=questions)
    (OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    (OUT / ".graphify_labels.json").write_text(
        json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False), encoding="utf-8")

    # cleanup intermediates
    for name in (".graphify_detect.json", ".graphify_cached.json"):
        (OUT / name).unlink(missing_ok=True)
    for f in OUT.glob(".graphify_chunk_*.json"):
        f.unlink()
    for f in OUT.glob(".graphify_chunklist_*.txt"):
        f.unlink()
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities")
    print("Now run: graphify export html   (from this folder)")


def _label(G, communities) -> dict:
    """Auto-label each community from its most-central node; curated names in
    labels-override.json (keyed by that central node's id) win when present."""
    override = {}
    ov = HERE / "labels-override.json"
    if ov.exists():
        override = json.loads(ov.read_text(encoding="utf-8"))
    members = defaultdict(list)
    for k, v in communities.items():
        if isinstance(v, list):          # {community_id: [node_ids]}
            members[k].extend(v)
        else:                            # {node_id: community_id}
            members[v].append(k)
    deg = dict(G.degree())
    labels = {}
    for c, ids in members.items():
        top = sorted(ids, key=lambda i: (-deg.get(i, 0),
                     G.nodes[i].get("file_type") == "document"))[0]
        if top in override:
            labels[c] = override[top]
        else:
            name = str(G.nodes[top].get("label", top)).split(" (article)")[0].strip()
            labels[c] = name[:37] + "..." if len(name) > 40 else name
    return labels


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "plan":
        plan()
    elif cmd == "finalize":
        finalize()
    else:
        sys.exit("usage: build_content_graph.py [plan|finalize]")
