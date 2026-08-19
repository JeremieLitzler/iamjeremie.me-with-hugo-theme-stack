---
title: "Building a Self-Excluding Index Note with Obsidian Dataview"
description: "A Dataview query that lists every note in a folder except the index note itself, and the FROM-clause parsing error that got in the way."
image: 2026-08-21-building-a-stack-of-books-sitting-on-top-of-a-wooden-table.jpg
imageAlt: a stack of books sitting on top of a wooden table
date: 2026-08-21
categories:
  - Tutorials
tags:
  - Obsidian
  - Note-Taking
---

I have organized a few folders of Obsidian\. For each one, I created a single index note at the top\. This note lists all the other notes, including their tags, so that I can quickly see them all\.

The most evident instrument for that task is [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), the plugin that enables you to question your vault like a tiny database\.

In essence, my desire was straightforward\: a table displaying the title and tags of each note in the folder, excluding the index note, since it shouldn’t include itself\.

## Understanding `FROM`

`FROM` in Dataview isn’t a general expression slot. It only accepts a literal source: a folder path as a string, a `#tag`, a `[[link]]`, or those combined with `and`, `or`, and `-`.

It lacks any notion of \`this\` and can’t evaluate dynamic field accesses such as \`this\.file\.folder\` at parse time\. This is because the source must be resolvable before the query starts running\. However, \`WHERE\` and \`TABLE\` are evaluated per row, which is where expressions like \`this\.file\.folder\` and \`this\.file\` should be evaluated\.

In my initial version, I had included a row\-based expression in a section that can only handle literal values, causing the parser to highlight that specific line rather than those surrounding it\.

## Two working versions

To build what I needed, I had two options:

```dataview
TABLE file.tags AS "Tags"
WHERE file.folder = this.file.folder AND file != this.file
SORT file.name ASC
```

This kept the resilience I was after in the first place. Comparing \`file\.folder\` against \`this\.file\.folder\` ensures that the query will find the right notes, even if the folder is renamed or moved, since both sides of the comparison are evaluated fresh each time the query runs\.

The downside is that this version scans the entire vault and filters afterwards, rather than narrowing the search at the start\.

For a small vault that’s not something I’d notice, but if you want to avoid the full scan, `FROM` still works fine as long as you give it what it actually wants: a literal path.

```dataview
TABLE file.tags AS "Tags"
FROM "path/to/folder"
WHERE file != this.file
SORT file.name ASC
```

That version is faster, but it stops working silently if the folder is ever renamed\. Nothing errors out; the index note just stops listing anything, since \`FROM\` keeps pointing at a path that no longer exists\.

I went with the first version as my default\. I’d rather trade some query speed for the ability to rename a folder without having to remember to correct an index note somewhere else\. For now… I’ll see if my choice remains the same as my vault grows\.

## Let’s Keep in Touch

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Brian Huynh on Unsplash.
