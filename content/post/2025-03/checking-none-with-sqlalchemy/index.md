---
title: "Checking None With SQLAlchemy"
description: "Here is a little tip for anyone who learns to use SQLAlchemy."
image: 2025-03-26-an-empty-subway.jpg
imageAlt: An empty subway
date: 2025-03-26
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Python
  - SQL Alchemy
---

Checking for `None` occurs often enough that you need to know this little tip.

## The SQL

To build this SQL Statement:

```sql
SELECT * FROM event
WHERE confirmed_at IS NULL
```

## Not How To Write It

You shouldn’t declare your SQLAlchemy query as follows:

```python
query = session.query(EventEntity).filter(
    EventEntity.confirmed_at is None,
)
```

It feels natural if you have written Python code before, but it won’t work.

## Correct Syntax

Instead, use SqlAlchemy like this, using `==` operator :

```python
query = session.query(EventEntity).filter(
    EventEntity.confirmed_at == None,
)
```

## Why

Because *SQLAlchemy* uses *magic methods (or operator overloading)* to create `SQL` constructs, it can only handle operators such as `!=` or `==`, but isn’t able to work with `is` (which is a very valid Python construct).

Source: [Stackoverflow](https://stackoverflow.com/a/5632224/3910066)

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/empty-subway-train-302428/)
