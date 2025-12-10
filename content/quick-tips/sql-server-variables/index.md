---
title: "SQL Server - Variables"
description: "Usage of simple variable with an example"
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2025-12-04
categories:
  - Web Development
tags:
  - SQL Server
---

## Scenario

If you want to store a value of a column from a table, a variable will do the trick.

## Code

```sql
-- You declare the variable with the prefix `@` and its type.
DECLARE @Total INT;

--Optionnally, you can set a default value
SET @Total = 0;
GO

-- You store the value you need into the variable
SELECT @Total = COUNT(*)
FROM dbo.Orders
WHERE OrderDate >= '2025-01-01';
```

## Documentation

Reference: [Microsoft Learn](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/variables-transact-sql).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credits: Image from [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
