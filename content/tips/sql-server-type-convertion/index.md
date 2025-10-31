---
title: "SQL Server - Cast and Convert"
description: "Usage of Cast and Convert with an example"
date: 2025-10-31
categories:
  - Web Development
tags:
  - SQL Server
---

In SQL Server, you can convert an INT to VARCHAR using either the CAST or CONVERT function. Here are both options:

## Using `CAST`

```c#
SELECT CAST(123 AS VARCHAR(10)) AS ConvertedValue;
```

## Using `CONVERT`

```c#
SELECT CONVERT(VARCHAR(10), 123) AS ConvertedValue;
```

## Key points

Always specify the length for VARCHAR (e.g., VARCHAR(10)), otherwise SQL Server uses a default length of 30.

If you omit the length, it might cause truncation or unexpected results in some contexts.

## Documentation

Reference: [Microsoft Learn](https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver17).
