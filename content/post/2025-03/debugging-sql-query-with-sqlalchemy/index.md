---
title: "Debugging SQL Query With SQLAlchemy"
description: "SQLAlchemy provides ORM-like querying to any database. But knowing what is the final SQL executed can help us."
image: 2025-03-19-a-green-weevil-bug.jpg
imageAlt: A Green Weevil bug
date: 2025-03-19
categories:
  - Web Development
tags:
  - Tip of the Day
  - Python
---

To view the SQL executed by SQLAlchemy, you need to import the driver from `sqlalchemy.dialects`. Adjust it to your needs.

The final code is the following:

```python
from sqlalchemy.dialects import sqlite

query = session.query(Entity).filter(
    and_(
        Entity.status.in_(target_statuses),
        Entity.confirmed_at == None,
        Entity.created_at <= cutoff_datetime
    )
).order_by(func.coalesce(
    Entity.in_progress_at,
    Entity.created_at)
)

# This prints out the SQL code generated and executed by SQLAlchemy
print(query.statement.compile(dialect=sqlite.dialect()))
```

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/green-black-and-brown-insect-40875/).
