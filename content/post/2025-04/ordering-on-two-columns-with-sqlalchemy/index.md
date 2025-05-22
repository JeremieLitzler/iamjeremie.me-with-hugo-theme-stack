---
title: "Sorting On Two Columns With SQLAlchemy"
description: "It isn’t just about alphabetical sorting and chronological sorting. There is more to it."
image: 2025-04-07-boxes-sorting-stuff.jpg
imageAlt: Boxes sorting stuff
date: 2025-04-07
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Python
  - SQL Alchemy
---

When we sort data, we need to take into account the NULL values. I’d like to share something I’ve learned through a practical example while building a Python application.

## The SQL

For example, to build this SQL Statement:

```sql
SELECT * FROM event
WHERE
status IN ('NEW', 'TODO') AND
confirmed_at IS NULL AND
created_at <= p_cutoff_datetime
ORDER BY
coalesce(in_progress_at, created_at) DESC NULLS LAST
```

## The Python Equivalent

Write the SQLAlchemy statement in the following way:

```python
            from sqlalchemy import select, update, func, and_, nullslast

            query = session.query(EventEntity).filter(
                and_(
                    EventEntity.status.in_(statuses),
                    EventEntity.confirmed_at == None,
                    EventEntity.created_at <= cutoff_datetime
                )
            ).order_by(
                nullslast(
                    func.coalesce(
                        EventEntity.in_progress_at,
                        EventEntity.created_at
                    ).desc()
                )
            )
```

A few comments:

- `coalesce` function takes the first value if provided otherwise, it takes the second.
- `nullslast` function ensure the null values don’t appear first, which is the default logic in SQL

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [RDNE Stock project](https://www.pexels.com/photo/boxes-on-the-floor-8580732/)
