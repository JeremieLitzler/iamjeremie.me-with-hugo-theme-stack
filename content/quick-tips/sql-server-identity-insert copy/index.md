---
title: "SQL Server - Checking the Health of a Single Index"
description: "Before you rebuild or reorganize an index, you want to know its fragmentation, size, and fill factor. Here is the query, and the caveats behind it."
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-07-14
categories:
  - Web Development
tags:
  - SQL Server
---

When you add or maintain an index, you often want a quick health check:

- how fragmented is it,
- how big is it,
- what fill factor was applied,
- and is it even enabled?

Here is a query that pulls all of that for one specific index.

## The Information Query

```sql
SELECT
    i.name                          AS IndexName,
    i.type_desc                     AS IndexType,
    s.avg_fragmentation_in_percent  AS FragmentationPct,
    s.page_count * 8 / 1024.0       AS SizeMB,
    i.fill_factor,
    i.is_disabled
FROM sys.indexes i
INNER JOIN sys.partitions p
    ON i.object_id = p.object_id AND i.index_id = p.index_id
CROSS APPLY sys.dm_db_index_physical_stats(
    DB_ID(), i.object_id, i.index_id, NULL, 'LIMITED') s
WHERE OBJECT_NAME(i.object_id) = 'MyTableNeedingAnIndex'
  AND i.name = 'IX_MyTableNeedingAnIndex_ColumnToIndex'  -- pin to your new index
ORDER BY SizeMB DESC;
```

Now, you need to understand some **important rules**:

1. `sys.dm_db_index_physical_stats` is a function, not a table. You call it with `CROSS APPLY` (or `OUTER APPLY`) so it runs once per index row; a plain `JOIN` won’t work. Running it requires at least **`CONTROL` permission** on the table.
2. `LIMITED` option is the cheapest mode to query the information. It only scans the parent (non-leaf) pages of the B-tree, which makes it fast but selective: you get `avg_fragmentation_in_percent` and `page_count`, but detail columns such as `avg_page_space_used_in_percent`, `fragment_count`, and `record_count` come back `NULL`. Switch to `SAMPLED` or `DETAILED` when you need those.
3. `NULL` is a wildcard, and typos are silent. `DB_ID()` and `OBJECT_ID()` return `NULL` when a name can’t be resolved, and the function reads `NULL` as “all databases / all objects.” A misspelled table name won’t raise an error—it’ll happily scan everything.

## An Example

So, let’s suppose you have a table and an index you just created:

```sql
CREATE TABLE MyTableNeedingAnIndex (
    Id          INT IDENTITY(1,1) PRIMARY KEY,
    ColumnToIndex NVARCHAR(100),
    Payload     NVARCHAR(MAX)
);

CREATE NONCLUSTERED INDEX IX_MyTableNeedingAnIndex_ColumnToIndex
    ON MyTableNeedingAnIndex (ColumnToIndex);
```

Running the health-check query against it returns a single row: the index name, `NONCLUSTERED`, its current fragmentation, its size in MB, and whether it’s disabled (`0`).

## Documentation

The official Microsoft documentation is:

`sys.dm_db_index_physical_stats (Transact-SQL)`—[https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-index-physical-stats-transact-sql](https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-index-physical-stats-transact-sql)

You may also want the catalog views the query joins:

- `sys.indexes (Transact-SQL)`—[https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-indexes-transact-sql](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-indexes-transact-sql)
- `sys.partitions (Transact-SQL)`—[https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-partitions-transact-sql](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-partitions-transact-sql)

It applies to SQL Server, Azure SQL Database, Azure SQL Managed Instance, Azure Synapse Analytics, and Analytics Platform System (PDW).

If you want a specific product version, append the `view` parameter to the URL (e.g., `?view=sql-server-ver17` for the latest, or `?view=sql-server-ver16’).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
