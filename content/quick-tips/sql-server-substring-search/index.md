---
title: "SQL Server - Filter on NVARCHAR Column With Substring"
description: "And what it can hide in term of performance and accuracy"
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-06-10
categories:
  - Software Development
tags:
  - SQL Server
---

This SQL Server trick seems simple, but let’s look at it in detail.

## The Basics

The following selects persons which LastName has a Y or Z as the third character from the end of the value:

```sql
SELECT *
FROM Person
WHERE SUBSTRING(LastName, LEN(LastName) - 2, 1) IN ('Y', 'Z');
```

## About Accuracy

First, `LEN()` ignores trailing spaces. In SQL Server, `LEN()` strips trailing spaces but `SUBSTRING` indexes the _full_ string. If `LastName` has trailing whitespace (common in `CHAR(n)` columns or messy imports), the start position is computed against a shorter logical length, while `SUBSTRING` counts the real characters — so it reads the wrong character.

```sql
-- LastName = 'Lopez   ' (3 trailing spaces)
-- LEN = 5, so start = 3 -> SUBSTRING returns 'p', NOT the intended 'e'
```

So run a trim first:

```sql
WHERE SUBSTRING(RTRIM(LastName), LEN(RTRIM(LastName)) - 2, 1) IN ('Y','Z')
```

Next, let’s talk about case sensitivity and collation. `IN ('Y','Z')` matches `y`/`z` only under a case-insensitive collation (the default). On a `_CS_` collation, lowercase third-from-end letters won’t match. Make it explicit if it matters which the collation in the `WHERE` clause:

```sql
... IN ('Y','Z') COLLATE Latin1_General_CI_AI
```

## About Performance

The predicate is non-SARGable. Wrapping `LastName` in `SUBSTRING`/`LEN` means SQL Server can’t seek an index. It must evaluate the expression for **every row**, forcing a full table/clustered index scan. No index on `LastName` will help as written.

A cleaner equivalent expression (same non-SARGable cost, but clearer intent and avoids the `LEN` math):

```sql
WHERE LEFT(RIGHT(RTRIM(LastName), 3), 1) IN ('Y','Z')
```

If this query runs often, add a **persisted computed column** and index it, turning the scan into a seek:

```sql
ALTER TABLE Person
  ADD ThirdCharFromEnd AS SUBSTRING(RTRIM(LastName), LEN(RTRIM(LastName)) - 2, 1) PERSISTED;

CREATE INDEX IX_Person_ThirdCharFromEnd ON Person (ThirdCharFromEnd) INCLUDE (/* cols you need */);

-- then:
WHERE ThirdCharFromEnd IN ('Y','Z');
```

## About SARGable

**SARGable** means **S**earch **ARG**ument **able**. A predicate (a `WHERE`/`JOIN`/`ON` condition) is SARGable if the query optimizer can use it as a _search argument_ to **seek** through an index rather than scanning every row.

### The core rule

A predicate is SARGable when the **indexed column is left bare** on one side of the comparison — no functions, no calculations wrapped around it.

```sql
-- ✅ SARGable: column is bare, index seek possible
WHERE LastName = 'Smith'
WHERE Price > 100
WHERE OrderDate >= '2026-01-01'
WHERE LastName LIKE 'Sm%'        -- prefix wildcard is OK

-- ❌ Non-SARGable: column wrapped in a function/expression
WHERE SUBSTRING(LastName, 1, 3) = 'Smi'
WHERE YEAR(OrderDate) = 2026
WHERE Price * 1.1 > 100
WHERE LastName LIKE '%ith'       -- leading wildcard kills the seek
```

### Why Does It Matter

An index is sorted by the column’s actual value. The engine can binary search (seek) to `Smith` instantly. But once you wrap the column — e.g., `SUBSTRING(LastName, ...)`— the index is sorted by`LastName`, _not_ by the substring result. The engine has no way to jump to the answer, so it must compute the expression for **every row** (a scan).

### What Can You Do to Fix It

Rewrite the statement so the column stays bare and the computation happens on the other side (or via a range). For example:

```sql
-- ❌ Non-SARGable
WHERE YEAR(OrderDate) = 2026

-- ✅ SARGable: same result as a range the index can seek
WHERE OrderDate >= '2026-01-01' AND OrderDate < '2027-01-01'
```

When the logic genuinely can’t be expressed against the bare column (like “third character from the end”), the workaround is a **persisted computed column with its own index** — you precompute the expression once at write time so there’s a real indexed value to seek against, as shown above.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
