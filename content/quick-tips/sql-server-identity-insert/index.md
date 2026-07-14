---
title: "SQL Server - Rules About IDENTITY_INSERT"
description: "If you copy data from a database to another, you might need to preserve the identifiers. But there is a caveat."
image: /quick-tips/images/sql-server.webp
imageAlt: Logo of Microsoft SQL Server
date: 2026-07-06
categories:
  - Web Development
tags:
  - SQL Server
---

To use `IDENTITY_INSERT = ON` in a SQL Server script, you’re enabling the ability to explicitly insert values into a table’s identity column (which normally auto-generates values). Here’s how to do it properly:

```sql
SET IDENTITY_INSERT [TableName] ON;

INSERT INTO [TableName] ([IdentityColumn], [OtherColumn1], [OtherColumn2], ...)
VALUES (IdentityValue, Value1, Value2, ...);

SET IDENTITY_INSERT [TableName] OFF;
```

Now, you need to understand some **important rules**:

1. **Only one table** in a session can have `IDENTITY_INSERT` set to `ON` at a time.
2. You **must include** the identity column in the `INSERT` statement.
3. The value you insert must **not conflict** with existing values in the identity column.

So, let’s suppose you have a table called `Employees`:

```sql
CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100),
    Position NVARCHAR(100)
);
```

To insert a specific `EmployeeID`:

```sql
SET IDENTITY_INSERT Employees ON;

INSERT INTO Employees (EmployeeID, Name, Position)
VALUES (1001, 'Jérémie Litzler', 'Developer');

SET IDENTITY_INSERT Employees OFF;
```

## A Few Extra Interesting Facts

I learned some interesting points when I dug the topic into more detail.

First, the value doesn’t strictly have to avoid conflicts in all cases—a duplicate only fails if a unique constraint/PK exists (which is the usual case). What the docs specifically note is: if the value inserted is larger than the current identity value for the table, SQL Server automatically uses the newly inserted value as the current identity value.

And second, the user must own the table or have ALTER permission on the table.

## Documentation

The official Microsoft documentation is:

**SET IDENTITY_INSERT (Transact-SQL)**—https://learn.microsoft.com/en-us/sql/t-sql/statements/set-identity-insert-transact-sql

It applies to SQL Server, Azure SQL Database, Azure SQL Managed Instance, Azure Synapse Analytics, and SQL database in Microsoft Fabric.

If you want a specific product version, append the `view` parameter to the URL (e.g., `?view=sql-server-ver17` for the latest, or `?view=sql-server-ver16’).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Microsoft Server](https://www.microsoft.com/en-us/sql-server)
