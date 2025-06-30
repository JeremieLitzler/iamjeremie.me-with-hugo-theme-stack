---
title: "How to Cast a datetimeoffset to String in SQL Server"
description: "Time zones in dates hold important information. Let’s lose it!"
image: 2025-06-23-a-clock-in-a-big-building.jpg
imageAlt: A clock in a big building
date: 2025-06-23
categories:
  - Software Development
tags:
  - SQL Server
---

In SQL Server, there are two main methods to convert a `datetimeoffset` to a string.

## Using CONVERT Function

The `CONVERT` function with style 121 is the most efficient method:

```sql
DECLARE @DateTimeOffset datetimeoffset(3) = '1997-12-31 14:53:00.123 +04:30';
DECLARE @StringDTO varchar(35) = CONVERT(nvarchar(35), @DateTimeOffset, 121);
```

**Important Note**: When using `CONVERT`, you must specify an adequate length for the `nvarchar` parameter to accommodate the full `datetimeoffset` value including fractional seconds and time zone offset [[^1](#sources-i-read-on-the-topic)].

## Using FORMAT Function

The `FORMAT` function offers more flexibility with culture-specific formatting:

```sql
DECLARE @date datetimeoffset = '2030-05-25 23:59:30.1234567 +07:00';
SELECT FORMAT(@date, 'G', 'en-us') AS FormattedDate;
```

## Format Styles

When using CONVERT, these are some common-style numbers for `datetimeoffset`:

| Style | Output Format                  |
| ----- | ------------------------------ |
| 121   | `yyyy-mm-dd hh:mi:ss.mmm(24h)` |
| 126   | `yyyy-mm-ddThh:mi:ss.mmm`      |
| 127   | `yyyy-mm-ddThh:mi:ss.mmmZ`     |

The styles 121 and 126 are recommended, as it preserves the time zone offset information [[^2](<(#sources-i-read-on-the-topic)>)].

For example:

```sql
DECLARE @DateTimeOffset datetimeoffset(3) = '1997-12-31 14:53:00.123 +04:30';
DECLARE @DateTimeString121 varchar(35) = CONVERT(nvarchar(35), @DateTimeOffset, 121);
DECLARE @DateTimeString126 varchar(35) = CONVERT(nvarchar(35), @DateTimeOffset, 126);
DECLARE @DateTimeString127 varchar(35) = CONVERT(nvarchar(35), @DateTimeOffset, 127);
select @DateTimeString121, @DateTimeString126, @DateTimeString127;
```

will output:

```plaintext
--@DateTimeString12
1997-12-31 14:53:00.123 +04:30

--@DateTimeString126
1997-12-31T14:53:00.123+04:30

@DateTimeString127 (e.g. UTC time)
1997-12-31T10:23:00.123Z
```

You can use [SQLiteOnline.com](http://SQLiteOnline.com) to test this with all major RBMS engines.

## Sources I read on the topic

- [^1] : [https://stackoverflow.com/questions/65823243/convert-datetimeoffset-to-varchar](https://stackoverflow.com/questions/65823243/convert-datetimeoffset-to-varchar)
- [^2] : [https://www.dofactory.com/sql/convert-datetime-to-string](https://www.dofactory.com/sql/convert-datetime-to-string)

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Muffin Land](https://www.pexels.com/photo/ornate-clock-at-musee-d-orsay-interior-28748289/)
