---
title: "Custom Equality Comparer Example"
description: "Understanding Equals and GetHashCode With Projections."
image: -.jpg
imageAlt:
date: 2026-10-19
categories:
  - Software Development
tags:
  - DotNet
  - CSharp
---

This is a custom **equality comparer** for C# that allows you to compare objects based on a specific property or calculation you define.

## What Can It Do

Instead of comparing entire objects, this comparer lets you specify _which part_ of an object to compare. It's particularly useful with LINQ methods like `Distinct()`, `GroupBy()`, or when using collections like `HashSet<T>` or `Dictionary<T>`.

## How Does It Work

First, we have this following constructor:

```csharp
public GenericEqualityComparer(Func<T, object> projection)
{
    // ...
}
```

It takes a function that extracts the value you want to compare from each object. For example, if you have a `Person` object, you might pass `p => p.LastName`, the projection function, to compare people by their last name only.

Then, we want to implement the `Equals` method:

```csharp
public bool Equals(T x, T y) => object.Equals(_projection(x), _projection(y));
```

It compares two objects by applying your projection function to each, then comparing the results. So it's comparing the _projected values_, not the full objects.

Finally, we implement the `GetHashCode` method:

```csharp
public int GetHashCode(T obj) => _projection(obj).GetHashCode();
```

It returns the hash code of the projected value. This is required for hash-based collections to work correctly.

## Let's See a Full Example

We design our class:

```csharp
public class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
}

// Compare people by last name only
var comparer = new GenericEqualityComparer<Person>(p => p.LastName);

var people = new List<Person>
{
    new Person { FirstName = "John", LastName = "Smith" },
    new Person { FirstName = "Jane", LastName = "Smith" },
    new Person { FirstName = "Bob", LastName = "Jones" }
};

// Get distinct last names
var distinctByLastName = people.Distinct(comparer).ToList();
// Result: John Smith and Bob Jones (Jane removed as duplicate last name)
```

This pattern is useful when you need flexible comparison logic without creating multiple comparer classes for different scenarios.

## What Is the Projected Values in the Example Above

The **projected values** are not the hash codes—they're the actual values returned by your projection function.

Let me clarify:

**Projected value** = whatever your `Func<T, object>` returns.

For example:

```csharp
// If your projection is this:
var comparer = new GenericEqualityComparer<Person>(p => p.LastName);

// Then the "projected value" is the LastName string itself
// For a Person with LastName = "Smith", the projected value is "Smith"

```

So, in the `Equals` method:

- `_projection(x)` returns the actual value (e.g., "Smith")
- `_projection(y)` returns the actual value (e.g., "Jones")
- Then it compares these values: `"Smith"` vs `"Jones"` = false

In the `GetHashCode` method:

```csharp
public int GetHashCode(T obj) => _projection(obj).GetHashCode();

```

- `_projection(obj)` returns the value (e.g., "Smith")
- `.GetHashCode()` then converts "Smith" into a hash code (e.g., 12345678)

So: **projected value** is actual data value (like a string, number, etc.)

**hash code** is an integer representation of that value for fast lookup

The hash code is derived _from_ the projected value, but they're different things.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
