---
title: "Custom Equality Comparer Example"
description: "Understanding Equals and GetHashCode With Projections."
image: 2026-10-19-comparing-two-cards-on-adult-hands.jpg
imageAlt: Free Pair of adult hands holding green and yellow toy cars on a white surface, symbolizing choice.
date: 2026-10-19
categories:
  - Software Development
tags:
  - DotNet
  - CSharp
---

This is a custom **equality comparer** for C# that allows you to compare objects based on a specific property or calculation you define.

## What Can It Do

Instead of comparing entire objects, this comparer lets you specify _which part_ of an object to compare. It’s particularly useful with LINQ methods like `Distinct()`, `GroupBy()`, or when using collections like `HashSet<T>` or `Dictionary<TKey, TValue>`.

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

It compares two objects by applying your projection function to each, then comparing the results. So it’s comparing the _projected values_, not the full objects.

Finally, we implement the `GetHashCode` method:

```csharp
public int GetHashCode(T obj) => _projection(obj)?.GetHashCode() ?? 0;
```

It returns the hash code of the projected value. Hash-based collections first use the hash code to find a bucket, then call `Equals` only on items in that bucket. If two objects are equal according to `Equals`, they must therefore produce the same hash code, otherwise they would land in different buckets and never be compared.

The `?.` and `?? 0` handle the case where the projection returns `null` (for example, a `Person` without a `LastName`): `object.Equals` already handles `null` safely, but calling `GetHashCode()` on `null` would throw a `NullReferenceException`.

Putting it all together, the full comparer looks like this:

```csharp
public class GenericEqualityComparer<T> : IEqualityComparer<T>
{
    private readonly Func<T, object> _projection;

    public GenericEqualityComparer(Func<T, object> projection)
    {
        _projection = projection;
    }

    public bool Equals(T x, T y) => object.Equals(_projection(x), _projection(y));

    public int GetHashCode(T obj) => _projection(obj)?.GetHashCode() ?? 0;
}
```

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

In practice, `Distinct()` keeps the first item it meets for each last name, so John stays and Jane goes. However, the documentation describes the result sequence as unordered, so don't build logic that depends on that order.

This pattern is useful when you need flexible comparison logic without creating multiple comparer classes for different scenarios.

If all you need is `Distinct()` and you target .NET 6 or later, `people.DistinctBy(p => p.LastName)` gives the same result without a custom comparer. The comparer remains useful for `HashSet<T>`, `Dictionary<TKey, TValue>`, or older target frameworks.

### Why `GetHashCode` Matters Here

Suppose the comparer kept the projection-based `Equals` but used the default `obj.GetHashCode()`, which is reference-based for classes (the hash values below are illustrative, not real computed values):

- John Smith gets hash `48291`, so it goes into bucket A.
- Jane Smith gets hash `91734`, so it goes into bucket B.
- `Distinct()` never compares them with `Equals`, because they are in different buckets.
- Result: both are kept, even though the comparer says they are equal.

With the comparer's `GetHashCode`, both hash `"Smith"`. They land in the same bucket, `Equals` runs and returns `true`, and Jane is dropped.

The rule only goes one way. Equal objects must have equal hashes, but equal hashes don't mean the objects are equal (that's a collision, and `Equals` sorts it out). That's why hashing the same projected value that `Equals` compares meets the contract.

## What Are the Projected Values in the Example Above

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
public int GetHashCode(T obj) => _projection(obj)?.GetHashCode() ?? 0;

```

- `_projection(obj)` returns the value (e.g., "Smith")
- `.GetHashCode()’ then converts “Smith” into a hash code (e.g., 12345678)

So: **the projected value** is actual data value (like a string, number, etc.)

**hash code** is an integer representation of that value for fast lookup

The hash code is derived _from_ the projected value, but they’re different things.

## Sources for This Article

- **Microsoft Documentation**:
  - [`IEqualityComparer<T>` Interface](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iequalitycomparer-1): defines the `Equals(T, T)` and `GetHashCode(T)` pair that a custom comparer implements.
  - [`IEqualityComparer<T>.GetHashCode(T)` Method](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iequalitycomparer-1.gethashcode): states that if `Equals` returns `true` for two objects, `GetHashCode` must return the same value for both.
  - [`Object.GetHashCode` Method](https://learn.microsoft.com/en-us/dotnet/api/system.object.gethashcode): explains that equal hash codes don’t imply equality, that the default implementation for reference types is based on the object’s reference, and that `GetHashCode()` should not throw exceptions.
  - [`Enumerable.Distinct` Method](https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable.distinct): documents the overload that accepts an `IEqualityComparer<T>` and notes that the result sequence is unordered.
  - [`Enumerable.DistinctBy` Method](https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable.distinctby): available since .NET 6, it removes duplicates using a key selector instead of a custom comparer.
- **.NET Runtime Source Code**:
  - [`Distinct.cs`](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Linq/src/System/Linq/Distinct.cs): shows that `Distinct()` builds a `HashSet<TSource>` with the comparer you pass in, which is why `GetHashCode` decides which items get compared.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit : Photo by SHVETS production on Pexels (`https://www.pexels.com/photo/person-holding-toy-cars-9742535/`).
