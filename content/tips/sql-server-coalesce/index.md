---
title: "SQL Server - Coalesce"
description: "Usage of Coalesce with an example"
date: 2025-10-28
categories:
  - Web Development
tags:
  - SQL Server
---

## Scenario

If you want to pick a column from TableA, but if it's NULL, use a column from TableB, you need to use the `COALESCE` built-in function in SQL Server.

## Code

```sql
SELECT
    COALESCE(a.ColumnName, b.ColumnName) AS PreferredColumn
FROM
    TableA a
JOIN
    TableB b ON a.ID = b.ID;
```

`COALESCE` returns the first non-null value from the list.

## Documentation

Reference: [Microsoft Learn](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/coalesce-transact-sql).
