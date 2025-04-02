---
title: "Proper “And” Syntax With SQLAlchemy"
description: "Here is a new little tip for anyone who learns to use SQLAlchemy."
image: 2025-04-02-a-child-hand-on-an-adult-hand.jpg
imageAlt: A child hand on an adult hand
date: 2025-04-02
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Python
  - SQL Alchemy
---

To build this SQL Statement:

```sql
SELECT * FROM event
WHERE
status IN ('NEW', 'TODO') AND
confirmed_at IS NULL AND
created_at <= p_cutoff_datetime
```

You shouldn’t declare your SQLAlchemy query as follows:

```python
            query = session.query(EventEntity).filter(
                    EventEntity.status.in_(statuses),
                    EventEntity.confirmed_at == None,
                    EventEntity.created_at <= cutoff_datetime
            )
```

It will output the following SQL statement:

```sql
SELECT * FROM event
WHERE
0 != 1 -- 🤔
```

The `0 != 1` is SQLAlchemy’s way of creating a condition that always returns false.

Instead, use SQLAlchemy like this, wrapping your conditions with the `_and` operator :

```python
            from sqlalchemy import and_

            query = session.query(EventEntity).filter(
                and_(
                    EventEntity.status.in_(statuses),
                    EventEntity.confirmed_at == None,
                    EventEntity.created_at <= cutoff_datetime
                )
            )
```

That’s it for this one!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Juan Pablo Serrano](https://www.pexels.com/photo/father-and-child-s-hands-together-1250452/)
