---
title: "Updating Part of a Column Value For Many Records"
description: "You will, as a backend developer, need someday to update several records as once to update part of a column’s value. But how? This is the topic of this article"
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-08-10
categories:
  - Web Development
tags:
  - SQL Server
---

Let’s say you have a table where you store paths of somes files uploaded through your web application.

Those path start with `\\original-network-drive`, which is a network path in Windows-style, at the beginning of the project. But then, the network path changes. How do you write an update statement to make sure all records point to the new network path?

## The SQL

```sql
UPDATE Files
SET Path = REPLACE(Path, '\\original-network-drive', '\\new-network-drive')
WHERE Path LIKE '\\original-network-drive%';
```

That’s it!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
