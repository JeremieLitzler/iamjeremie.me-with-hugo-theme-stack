---
title: "SQL Server - Collation, Accents and Unique Constraints"
description: "Collations help with characters sensitivity and define various constraints."
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-03-11
categories:
  - Web Development
tags:
  - SQL Server
---

Let’s say we save some information in a ’NVARCHAR’column and we don’t want to worry about accents or character casings to handle unicity.

What should you do?

## The Example

Let’s take the example of a `Person` table with the `Name` column.

I’d like to make sure the user’s input doesn’t cause an issue of unicity in the records, whether the input is `Jeremie Litzler` or `Jérémie Litzler`.

## Checking the current COLLATION

First, let’s check the current collation of the column:

```sql
SELECT  COLUMN_NAME,  COLLATION_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = Person' AND COLUMN_NAME = 'Name';
```

## Interpreting the COLLATION

Let’s say the collation is `Latin1_General_100_CI_AI`. What does it mean?

- Latin1_General_100: Modern collation with version 100 sorting rules
- CI = Case Insensitive
- AI = Accent Insensitive
- AS = Accent Sensitive

## The Solution

So, if I want to avoid both input `Jeremie Litzler` and `Jérémie Litzler` to be inserted, then change the collation to `Latin1_General_100_CI_AS`.

That way, running ’SELECT _ FROM Person WHERE NAME = 'Jeremie Litzler'’ would return the same entry as ’SELECT _ FROM Person WHERE NAME = 'Jérémie Litzler'’.

## Going Further

The best way is to add a unique constraint:

```sql
ALTER TABLE Person
    ADD CONSTRAINT IX_Person_Name UNIQUE
        ([Name])
```

However, make sure your column, if of the type `NVARCHAR`, doesn’t use the `MAX` precision. You must, therefore, limit the size of the column to create the unique constraint.

## Documentation

Reference: [Microsoft Learn](https://learn.microsoft.com/en-us/sql/relational-databases/collations/collation-and-unicode-support).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credits: Image from [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
