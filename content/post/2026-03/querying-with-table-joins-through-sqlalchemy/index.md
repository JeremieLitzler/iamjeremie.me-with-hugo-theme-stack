---
title: "Querying With Table Joins Through SQLAlchemy"
description: "There is more than one way to join tables, but here is the one that worked for me."
image: 2026-03-02-chemistry-set-with-4-tubes-erlenmeyer-flask-and-a-beaker.jpg
imageAlt: Chemistry set with 4 tubes, Erlenmeyer flask and a beaker
date: 2026-03-02
categories:
  - Web Development
tags:
  - Python
  - SQL Alchemy
---

When building a Python application, I needed to fetch data spread across two related tables in a single query. Here is what I learned about doing joins with SQLAlchemy.

## The SQL

To express something like:

```sql
SELECT * FROM event
JOIN event_journal ON event.event_id = event_journal.event_id
```

## The Python Equivalent

Write the SQLAlchemy statement in the following way:

```python
from sqlalchemy.orm import Session

session = Session()
results = session.query(EventEntity, EventJournalEntity).join(
    EventJournalEntity,
    EventEntity.event_id == EventJournalEntity.event_id
).all()

# Process results: contains tuples of (EventEntity, EventJournalEntity)
for event, journal in results:
    print(f"Event: {event.id}, Journal: {journal.id}")
```

I’d like to add a few comments:

- `session.query(EventEntity, EventJournalEntity)` tells SQLAlchemy you want columns from both tables—the result will be a list of tuples rather than a flat list of one entity.
- `.join(EventJournalEntity, EventEntity.event_id == EventJournalEntity.event_id)` specifies the target table and the `ON` condition explicitly, which avoids ambiguity when the relationship isn’t preconfigured on the model.
- You can chain `.filter()`, `.order_by()`, and other clauses after `.join()` as you normally would on a single-entity query.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Kindel Media](https://www.pexels.com/photo/colorful-liquids-in-laboratory-glasswares-8325715/).
