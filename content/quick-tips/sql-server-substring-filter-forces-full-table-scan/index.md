---
title: "Why Your SUBSTRING Filter Forces a Full Table Scan"
description: "A one-line T-SQL filter on the third character from the end of a name looks harmless, but it hides a correctness trap and guarantees a full scan. Here is what goes wrong and how I fixed it."
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-07-31
categories:
  - Software Development
tags:
  - SQL Server
  - T-SQL
  - Performance
  - Database
---

Someone handed me a query the other day and asked a simple question: any concerns, either in accuracy or performance?

Here it is:

```sql
SELECT *
FROM Person
-- Which LastName has a Y or Z as the third character from the end of the value
WHERE SUBSTRING(LastName, LEN(LastName) - 2, 1) IN ('Y', 'Z');
```

It reads cleanly. It even runs and returns rows. But the more I looked at it, the more I found someone hiding under those two functions: `SUBSTRING` and `LEN` calls. This is T-SQL on SQL Server, so everything below is in that dialect, and there is enough here to be worth walking through carefully.

## The Trailing-Space Trap

The biggest single correctness risk is the interaction between `LEN` and `SUBSTRING`, and it is easy to miss because both functions are doing exactly what they were designed to do.

`LEN` excludes trailing spaces. That is not a quirk of one server’s configuration. It is documented behavior. Microsoft’s own reference for the function states plainly that it “returns the number of characters of the specified string expression, excluding trailing spaces.”

`SUBSTRING`, on the other hand, indexes the full, untrimmed string, counting every real character from position 1.

So the two functions disagree about how long the string is. When `LastName` carries trailing whitespace — common in `CHAR(n)` columns or in data imported from a messy source — the start position is computed against the shorter logical length, while `SUBSTRING` counts against the longer physical one. The result is that you read the wrong character.

```sql
-- LastName = 'Lopez   ' (3 trailing spaces)
-- LEN = 5, so start = 3 -> SUBSTRING returns 'p', NOT the intended 'e'
```

The fix is to trim before you measure, so both functions see the same string:

```sql
WHERE SUBSTRING(RTRIM(LastName), LEN(RTRIM(LastName)) - 2, 1) IN ('Y','Z')
```

## What Happens to Short Names

The next thing I checked was what the expression does when the name is shorter than three characters, because that is exactly the kind of edge case a `SELECT *` demo never surfaces.

Here is an example:

- A length-2 name gives `start = 0`, so `SUBSTRING(x, 0, 1)` returns an empty string.
- A length-1 name gives `start = -1`, which also returns an empty string.

There is no error here, and no false positive either — an empty string never matches `Y` or `Z`. This is not an accident of the engine; it is spelled out in the `SUBSTRING` documentation, which says that if the start value "is less than 1, the returned expression begins at the first character," and the number of characters returned works out to zero in these cases. So the rows are silently excluded rather than crashing anything. That is fine if excluding them is what you meant. The point is to decide that on purpose rather than discover it later.

## Case Sensitivity and Collation

`IN ('Y','Z')` will happily match lowercase `y` and `z` too — but only under a case-insensitive collation, which happens to be the default on most installations. Move to a `_CS_` collation and those lowercase letters stop matching.

If the distinction matters, say so explicitly rather than leaning on whatever the server was configured with:

```sql
... IN ('Y','Z') COLLATE Latin1_General_CI_AI
```

And while we are enumerating the quiet exclusions: a `NULL` in `LastName` makes the whole predicate evaluate to `NULL`, so the row drops out. That is usually the behavior you want, but it is worth noting alongside the short-name case.

## The Part That Falls Into a Full Scan

Accuracy aside, the performance story is where this query really shows its cost, and it comes down to one word: **SARGable**.

SARGable is short for _Search ARGument able_. A predicate in a `WHERE`, `JOIN`, or `ON` clause is SARGable when the optimizer can use it as a search argument to seek through an index instead of scanning every row. The core rule is simple: the indexed column has to sit bare on one side of the comparison, with no functions or calculations wrapped around it.

```sql
-- SARGable: the column is bare, an index seek is possible
WHERE LastName = 'Smith'
WHERE OrderDate >= '2026-01-01'
WHERE LastName LIKE 'Sm%'        -- a prefix wildcard is fine

-- Non-SARGable: the column is wrapped in a function
WHERE SUBSTRING(LastName, 1, 3) = 'Smi'
WHERE YEAR(OrderDate) = 2026
WHERE LastName LIKE '%ith'       -- a leading wildcard kills the seek
```

The reason is structural. An index is sorted by the column's actual value, so the engine can binary-search straight to `’Smith'’. But the moment you wrap the column in `SUBSTRING`, the index is still sorted by `LastName`, not by the substring result. The engine has no way to jump to the answer, so it computes the expression for every single row.

That is a full scan, and no index on `LastName` will rescue the query as written.

The original predicate wraps `LastName` in both `SUBSTRING` and `LEN`, so it is firmly non-SARGable. On top of that, the `SELECT *` pulls back every column, inflating I/O and ruling out any covering index that might have softened the blow. Selecting only the columns you actually need is the cheap half of the fix.

There is also a cleaner way to write the same logic. It carries the same non-SARGable cost, but it reads better and drops the `LEN` arithmetic entirely:

```sql
WHERE LEFT(RIGHT(RTRIM(LastName), 3), 1) IN ('Y','Z')
```

## When the Query Runs Often

The usual way to make a non-SARGable predicate SARGable is to move the work off the column — like to rewrite ’WHERE YEAR(OrderDate) = 2026` as a range like ’WHERE OrderDate >= ’2026-01-01’ AND OrderDate < ’2027-01-01’’, and suddenly the index can seek.

Back to our `LastName` example, “the third character from the end” cannot be expressed as a range on the bare column. There is no rewrite that keeps `LastName` untouched.

When the logic genuinely resists that solution, the answer is to precompute it. You add a persisted computed column and index it, turning the write-time work into a read-time seek. A computed column is a virtual column that, as Microsoft’s documentation puts it, “isn’t physically stored in the table unless the column is marked `PERSISTED`“ — and a deterministic, persisted computed column of an indexable type can serve as a key column in an index.

```sql
ALTER TABLE Person
  ADD ThirdCharFromEnd AS SUBSTRING(RTRIM(LastName), LEN(RTRIM(LastName)) - 2, 1) PERSISTED;

CREATE INDEX IX_Person_ThirdCharFromEnd ON Person (ThirdCharFromEnd) INCLUDE (/* cols you need */);

-- then:
WHERE ThirdCharFromEnd IN ('Y','Z');
```

Now the expression is evaluated once, at write time, and stored as a real indexed value the optimizer can seek against. The hot-path query becomes a seek on a bare column, which is exactly what SARGability asked for.

## Conclusion

The query works for clean data of three characters or more. That sentence does a lot of load-bearing work. And it is fragile against trailing spaces, it inherits whatever case behavior the collation happens to impose, and it forces a full scan every time it runs.

None of those are visible in a quick test against tidy sample data, which is exactly why they are worth naming out loud. Trim the input, be explicit about the character cases, replace the `SELECT *` with something more refined, and if this is a path that often runs, persist and index the computed value.

Yes, a one-line filter deserves a second look precisely because it looks so harmless.

## References

- [LEN (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/len-transact-sql) — Microsoft Learn, on `LEN` excluding trailing spaces.
- [SUBSTRING (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/substring-transact-sql) — Microsoft Learn, on 1-based indexing and start values less than 1.
- [Specify computed columns in a table](https://learn.microsoft.com/en-us/sql/relational-databases/tables/specify-computed-columns-in-a-table) — Microsoft Learn, on `PERSISTED` columns and indexing them.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
