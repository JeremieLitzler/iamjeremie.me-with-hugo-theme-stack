---
title: "SQL Server - Resolve Collation Conflict"
description: "Collation define the "
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2025-12-04
categories:
  - Web Development
tags:
  - SQL Server
---

This SQL Server error occurs when you’re comparing columns from different tables that have different collation settings.

## Understanding the Collations

Let’s quickly review the meaning of what is a collation.

For example:

- `Latin1_General_100_CI_AI` is a modern collation with version 100 sorting rules
- `SQL_Latin1_General_CP1_CI_AS` is a legacy SQL Server collation

where :

- `CI` means Case Insensitive
- `AI` means Accent Insensitive
- `AS` means Accent Sensitive

Choose the solution based on whether you need a one-time fix (use COLLATE in query) or want to standardize your database (alter column collation).

Here are the solutions to solve the issue.

## Use COLLATE in Your Query

Add COLLATE DATABASE_DEFAULT to one of the columns in your comparison:

```sql
-- Option 1: Apply to one column
SELECT \*
FROM Table1 t1
JOIN Table2 t2 ON t1.Column1 = t2.Column2 COLLATE DATABASE_DEFAULT

-- Option 2: Apply to both columns
SELECT \*
FROM Table1 t1
JOIN Table2 t2 ON t1.Column1 COLLATE DATABASE_DEFAULT = t2.Column2 COLLATE DATABASE_DEFAULT

-- Option 3: Force specific collation
SELECT \*
FROM Table1 t1
JOIN Table2 t2 ON t1.Column1 = t2.Column2 COLLATE Latin1_General_100_CI_AI
Permanent Fix - Change Column Collation
```

If you want to permanently align the collations:

```sql
-- Check current collations
SELECT
TABLE_NAME,
COLUMN_NAME,
COLLATION_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE COLUMN_NAME IN ('YourColumn1', 'YourColumn2')
AND TABLE_NAME = 'Table1'

-- Change column collation
ALTER TABLE Table2
ALTER COLUMN Column2 VARCHAR(100) COLLATE Latin1_General_100_CI_AI
```

## Existing Table vs. Temporary Table

When you can’t alter an existing table but you can control the temp table definition, you should match the temp table’s collation to the existing table’s collation.

Here’s how to define your temp table:

```sql
-- Option 1: Match the ExistingTable table's collation explicitly
CREATE TABLE #TmpTable (
    [Code] NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
)

-- Option 2: Use DATABASE_DEFAULT (if ExistingTable uses database default)
CREATE TABLE #TmpTable(
    [Code] NVARCHAR(50) COLLATE DATABASE_DEFAULT NOT NULL
)
```

### To Find Content Table’s Exact Collation

If you’re not sure which collation ExistingTable.Code uses, run this:

```sql
SELECT
    COLUMN_NAME,
    COLLATION_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'ExistingTable'
    AND COLUMN_NAME = 'Code'
```

Then use that exact collation name in your temp table definition.

## Alternative: Fix at Join Time

If you prefer not to change the temp table definition, you can still fix it in your query.

In my case, I stumbled on the problem with the `join` clause:

```sql
SELECT c.*
FROM ExistingTable c
INNER JOIN #TmpCodesNeeded t
    ON c.Code = t.Code COLLATE SQL_Latin1_General_CP1_CI_AS
```

But defining the temp table with the correct collation upfront is cleaner and avoids needing COLLATE clauses throughout your queries.

## Documentation

Reference: [Microsoft Learn](https://learn.microsoft.com/en-us/sql/relational-databases/collations/collation-and-unicode-support).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credits: Image from [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
