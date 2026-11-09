---
title: "Grouping Rows by Year, Month, Day and Hour in SQL Server"
description: "Counting rows per hour in T-SQL takes four date parts or one truncated datetime. Here are both queries, and what they leave out by default."
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-11-04
categories:
  - Software Development
tags:
  - SQL Server
---

When you need stats, a count of rows per hour out of a SQL Server table, broken down by year, month, day and hour, gives you the data you need. I know the syntax in Oracle and mistakenly thought it was similar to the Microsoft product. But it wasn’t.

It is a query I rarely write, only when I’m in need of statistical data, but this time, I’ll save the syntax in an article, along with the two details that make the result misleading if I ignore them, and a bonus: how to get the subtotals in the same result.

The examples use a `CreatedAt` datetime column on a `dbo.Events` table. Swap in your own names.

## Grouping by the Four Date Parts

The direct translation of “year, month, day, hour” is one grouping expression per part:

```sql
SELECT
    YEAR(CreatedAt)           AS [Year],
    MONTH(CreatedAt)          AS [Month],
    DAY(CreatedAt)            AS [Day],
    DATEPART(HOUR, CreatedAt) AS [Hour],
    COUNT(*)                  AS Total
FROM dbo.Events
GROUP BY
    YEAR(CreatedAt),
    MONTH(CreatedAt),
    DAY(CreatedAt),
    DATEPART(HOUR, CreatedAt)
ORDER BY [Year], [Month], [Day], [Hour];
```

The first three columns use the `YEAR`, `MONTH` and `DAY` shorthands and the fourth goes through `DATEPART`. Microsoft’s reference for [`DATEPART`](https://learn.microsoft.com/en-us/sql/t-sql/functions/datepart-transact-sql) says the values returned for the `year`, `month` and `day` dateparts “are the same as those returned by the functions `YEAR`, `MONTH`, and `DAY`, respectively”, so you could write all four with `DATEPART` and get the same result.

Two things in this query look redundant and aren’t. The expressions are repeated in the `GROUP BY` instead of reusing the `[Year]` or `[Hour]’ aliases, because the [`GROUP BY`documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql) is explicit that a`GROUP BY`column expression “can’t contain a column alias that you define in the`SELECT` list.”

And the `ORDER BY` is there because, in the words of the same page, “the `GROUP BY` clause doesn’t order the result set.” Without it, the hours come back in whatever order the engine found convenient. The `ORDER BY`, on the other hand, can use the aliases.

## One Column per Hour Instead of Four

Four integer columns are fine to read in a result grid. They are awkward as soon as I want to chart the result or join it to something else, because the hour is now spread over four keys. A single datetime per hour bucket is easier to work with, and that means truncating `CreatedAt` to the hour.

On SQL Server 2022 and later, there is a function for exactly that:

```sql
-- Will provide `2026-10-26 08:00:00.000` values for "HourBucket"
SELECT DATETRUNC(HOUR, CreatedAt) AS HourBucket, COUNT(*) AS Total
FROM dbo.Events
GROUP BY DATETRUNC(HOUR, CreatedAt)
ORDER BY HourBucket;
```

The [`DATETRUNC` reference](https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql) describes it in one line: it “returns an input date truncated to a specified datepart.”

- `DATETRUNC(HOUR, CreatedAt)` gives ’2026-10-26 08:00:00.000’, ’2026-10-26 09:00:00.000`.
- `DATETRUNC(DAY, CreatedAt)` gives ’2026-10-26 00:00:00.000`, ’2026-10-27 00:00:00.000` and so on.

It also keeps the data type of its input, so a ’datetime2` column gives a ’datetime2` bucket. The same page notes that `DATETRUNC` “was introduced in SQL Server 2022 (16.x)”, which rules it out on older instances.

On those, the classic workaround does the job:

```sql
SELECT DATEADD(HOUR, DATEDIFF(HOUR, 0, CreatedAt), 0) AS HourBucket, COUNT(*) AS Total
FROM dbo.Events
GROUP BY DATEADD(HOUR, DATEDIFF(HOUR, 0, CreatedAt), 0)
ORDER BY HourBucket;
```

It reads strangely at first, until you understand the meaning of the first `0`. SQL Server interprets `0` as January 1, 1900, a detail the `DATEPART` page mentions in its examples. So `DATEDIFF(HOUR, 0, CreatedAt)` counts the whole hours elapsed since that date, and `DATEADD` adds that many hours back onto it. The minutes and seconds never make the round trip.

## Hours With No Rows Are Missing

Both queries only return the hours that have at least one row. A quiet night between 2 a.m. and 5 a.m. doesn't show up as three rows with a total of zero. It doesn't show up at all.

That is harmless when I am looking for the busiest hours. However, when I am drawing a timeline, it can be misleading because a chart will happily connect 1 a.m. to 6 a.m. with a straight line. To show the empty hours as zero, the buckets have to come from somewhere other than the data: a calendar or numbers table that lists every hour of the period, with the events `LEFT JOIN`ed onto it.

## The Hour Boundaries Follow the Stored Time Zone

If `CreatedAt` is stored in UTC, the day and the hour I am grouping on are UTC ones. For anyone reading the report in another time zone, the "day" starts and ends at the wrong moment, and the busiest hour is shifted by the offset.

The fix is to convert before grouping, with [`AT TIME ZONE`](https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql), which is available from SQL Server 2016. The documentation explains why it has to be applied twice on a plain datetime column: when the input "is provided without offset information, the function applies the offset of the time zone assuming that _input_date_ is in the target time zone." So the first call only declares that the stored value is UTC, and the second one actually converts it:

```sql
SELECT
    YEAR(l.LocalCreatedAt)           AS [Year],
    MONTH(l.LocalCreatedAt)          AS [Month],
    DAY(l.LocalCreatedAt)            AS [Day],
    DATEPART(HOUR, l.LocalCreatedAt) AS [Hour],
    COUNT(*)                         AS Total
FROM dbo.Events AS e
CROSS APPLY (
    SELECT e.CreatedAt AT TIME ZONE 'UTC' AT TIME ZONE 'Central European Standard Time' AS LocalCreatedAt
) AS l
GROUP BY
    YEAR(l.LocalCreatedAt),
    MONTH(l.LocalCreatedAt),
    DAY(l.LocalCreatedAt),
    DATEPART(HOUR, l.LocalCreatedAt)
ORDER BY [Year], [Month], [Day], [Hour];
```

The time zone name is one of the Windows names, and the list of those installed on the server is exposed through the `sys.time_zone_info` system view.

Daylight saving time adds a wrinkle. When the clocks go back, the local hour from 2 a.m. to 3 a.m. happens twice, and both occurrences fall into the same local bucket. When the clocks go forward, one hour is missing from the result. It is called the joy of time handling! Remember that it is not the when that matters, but the where...

## Subtotals in the Same Result

The last thing you could need next to the hourly counts is the total per day, per month and per year. Rather than running four queries, `GROUP BY ROLLUP` produces them in one pass. The documentation says it "creates a group for each combination of column expressions" and then "rolls up the results into subtotals and grand totals", moving "from right to left, decreasing the number of column expressions."

```sql
SELECT
    YEAR(CreatedAt)           AS [Year],
    MONTH(CreatedAt)          AS [Month],
    DAY(CreatedAt)            AS [Day],
    DATEPART(HOUR, CreatedAt) AS [Hour],
    COUNT(*)                  AS Total
FROM dbo.Events
GROUP BY ROLLUP (
    YEAR(CreatedAt),
    MONTH(CreatedAt),
    DAY(CreatedAt),
    DATEPART(HOUR, CreatedAt)
);
```

With the four expressions in that order, right to left gives exactly the levels you are after: the hourly rows, then a row per day where `[Hour]` is `NULL`, a row per month where `[Day]` and `[Hour]’ are `NULL`, a row per year, and a final row with every part `NULL`for the grand total. The order of expressions matters here, which it doesn’t in a plain`GROUP BY`.

Here is what the result looks like in a few sample rows (sorted for readability, since `ROLLUP` doesn’t guarantee an order either):

```text
Year  Month  Day   Hour  Total
----  -----  ----  ----  -----
2026  10     30    22    5
2026  10     30    NULL  5      <- total for October 30
2026  10     NULL  NULL  5      <- total for October
2026  11     3     8     12
2026  11     3     9     20
2026  11     3     NULL  32     <- total for November 3
2026  11     4     8     15
2026  11     4     NULL  15     <- total for November 4
2026  11     NULL  NULL  47     <- total for November
2026  NULL   NULL  NULL  52     <- total for 2026
NULL  NULL   NULL  NULL  52     <- grand total
```

If `CreatedAt` can itself be `NULL`, a data row and a subtotal row look alike. Adding [`GROUPING([column expression])`](https://learn.microsoft.com/en-us/sql/t-sql/functions/grouping-transact-sql) to the `SELECT` list tells them apart, as it “returns 1 for aggregated or 0 for not aggregated in the result set”.

## References

- [DATEPART (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/datepart-transact-sql), Microsoft Learn, on the equivalence with `YEAR`, `MONTH` and `DAY`, and on ’0` being January 1, 1900.
- [DATETRUNC (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql), Microsoft Learn, on truncating to a datepart and its introduction in SQL Server 2022.
- [GROUP BY (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql), Microsoft Learn, on aliases, ordering and `ROLLUP`.
- [GROUPING (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/functions/grouping-transact-sql), Microsoft Learn, on telling `ROLLUP` subtotal rows from standard `NULL` values.
- [AT TIME ZONE (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql), Microsoft Learn, on converting a datetime without offset information.

## Conclusion

Grouping by the hour is four date parts in the `GROUP BY`, or one truncated datetime when the result feeds a chart or a join. The query itself is the easy part.

What deserves a second look is what the result means: hours without rows are absent rather than zero, and the hours are those of the time zone the column was stored in. As a bonus, the subtotals are one `ROLLUP` away.

Which do you use when you build your stats? What did you learn?

Share with me and, as always, if you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
