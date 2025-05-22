---
title: "What’s New With .NET 8 and C# 12"
description: "Below is a comprehensive summary of the most important updates of .NET 8, released on November 14, 2023 as a Long-Term Support (LTS) version."
image: 2023-12-01-dotnet-8-logo.svg
imageAlt: A .NET 8.0 made by myself
date: 2023-12-01
categories:
  - Web Development
tags:
  - DotNet
  - Csharp
---

## .NET 8.0: Full Summary of What’s New

.NET 8 brings significant improvements and new features across performance, developer productivity, cloud-native development, AI integration, and cross-platform capabilities. Below is a comprehensive summary of the most important updates.

### Major Highlights

.NET 8.0 includes improvements for:

- **Performance** with substantial runtime and library optimizations, including a new Dynamic Profile-Guided Optimization (PGO) code generator, which can boost app performance by up to 20% [^2] [^1] [^7].
- **Cloud-Native Development** with the introduction of .NET Aspire, a new stack for building observable, production-ready cloud-native applications with improved local developer experience[^2].
- **Containerization** to produce smaller, more secure container images with non-root user support, enabling faster and safer deployments[^2].
- **Native AOT (Ahead-of-Time) Compilation** to enhance support for compiling apps to native code, reducing memory usage, improving startup times, and eliminating the need for JIT at runtime[^2] [^3].
- **AI Integration** with easier integration with AI services and plugins, including improved `System.Numerics` and collaboration with Azure OpenAI[^2].

### Key Features and Improvements

On the performance and diagnostics side, .NET 8.0 adds:

- Dynamic PGO for smarter code optimization[^2].
- Faster application startup and reduced memory usage.
- Improved diagnostics and observability tools for easier monitoring, profiling, and debugging[^3].

It comes with C# 12 Language Features:

- Primary constructors for all classes and structs, simplifying object initialization.
- Default values for lambda expression arguments.
- Type aliasing for any type, not just named ones[^3][^2].
- Enhanced pattern matching and other expressiveness improvements[^3] [^6].

I’ll detail them [below with examples](#c-12-new-coding-features-with-examples).

Garbage Collection and Memory Management receive updates:

- with new dynamic memory limits for the garbage collector, especially useful for cloud and Kubernetes scenarios[^3].
- with an API for refreshing memory limits at runtime.

JSON Handling gets better with:

- Faster and more standards-compliant JSON serialization/deserialization (RFC 8259, ECMA-404)[^5].
- Support for property serialization from interface hierarchies.
- New attributes for stricter JSON mapping with better error handling[^3] [^5].

Regarding ASP.NET Core 8, the frontend solution of Microsoft,

- We see up to 18% faster than .NET 7 for web workloads[^3].
- We receive Native AOT support for web apps.
- We can enjoy enhanced Blazor with Full-stack Blazor for unified web UI development, improved server-side rendering, and better interactivity[^3] [^2] [^4].
- And finally, APIs for metrics, dependency injection, and cloud readiness receive improvements over the previous version [^4] [^5].

With Entity Framework Core 8, support for complex/value type support (e.g., Address, Coordinate) is introduced. Also, lazy loading, no-tracking queries, JSON column mapping, and model building receive performance boost [^7] [^3].

On the cross-platform framework .NET MAUI for native-ready applications, .NET 8.0 brings better controls, gesture recognizers, navigation, and platform integration.
On the DX side, performance enhancements for cross-platform (Windows, macOS, Android, iOS) app development[^7] [^3].

For better control over time and faking values, this .NET version introduces a new `TimeProvider` class and `ITimer` interface[^3].

On the cryptography side, it adds SHA-3 support for enhanced security and improves the randomness APIs (e.g., `GetItems()`, `Shuffle()`), useful for secure and unbiased data handling[^3][^5].

### Feature Comparison Table

| Area                 | .NET 8 Improvements/Features                                 |
| -------------------- | ------------------------------------------------------------ |
| Performance          | Dynamic PGO, faster startup, reduced memory, Native AOT      |
| Language             | C# 12: primary constructors, pattern matching, type aliasing |
| Cloud-Native         | .NET Aspire, container images, dynamic GC memory limits      |
| Web                  | ASP.NET Core 8, Blazor full-stack, metrics APIs              |
| Cross-Platform       | .NET MAUI enhancements, WPF, Windows Forms updates           |
| AI Integration       | System.Numerics, Azure OpenAI, plugin support                |
| Security             | SHA-3, improved randomness APIs                              |
| Data                 | EF Core 8: complex types, JSON mapping, lazy loading         |
| Diagnostics          | Improved profiling, logging, observability tools             |
| Developer Experience | Visual Studio 2022, Codespaces, DevOps enhancements          |

## C# 12 New Coding Features with Examples

It introduces several new language features[^8] that enhance expressiveness and reduce boilerplate. Here are some of the most notable additions, each with a code example.

### Primary Constructors for Classes and Structs

Primary constructors allow you to declare constructor parameters directly in the class or struct declaration, simplifying property initialization.

```csharp
public class Employee(string firstName, string lastName, DateTime hireDate, decimal salary)
{
    public string FirstName { get; init; } = firstName;
    public string LastName { get; init; } = lastName;
    public DateTime HireDate { get; init; } = hireDate;
    public decimal Salary { get; init; } = salary;
}
```

This reduces boilerplate and makes your classes more concise[^9] [^13].

### Default Values for Lambda Expression Parameters

You can now specify default parameter values in lambda expressions, similar to regular methods.

```csharp
Func add = (x, y = 5) => x + y;

Console.WriteLine(add(10));    // Output: 15 (y defaults to 5)
Console.WriteLine(add(10, 20)); // Output: 30 (y is 20)
```

This makes lambdas more flexible and concise[^10] [^12] [^8].

### Alias Any Type

You can now create aliases not just for named types, but for any type, including tuples, arrays, and more.

```csharp
using Person = System.Collections.Generic.Dictionary;

Person p = new Person();
p["Name"] = "Alice";
p["Age"] = 25;
```

This helps with code readability and reuse[^11].

{{< blockcontainer jli-notice-tip "I can see how this could be useful">}}

Though, you need to make sure the alias is used a single responsibility.

And I’d add a suffix to the alias to know the underlying type just by reading the type alias, like `PersonDico` for example.

{{< /blockcontainer >}}

### Collection Expressions

C# 12 introduces collection expressions for easier array and collection initialization and merging.

```csharp
int[] part1 = [1, 2, 3];
int[] part2 = [4, 5, 6];
int[] combined = [.. part1, .. part2];

foreach (var number in combined)
    Console.Write($"{number} "); // Output: 1 2 3 4 5 6
```

This syntax is concise and expressive for collection manipulation[^12].

{{< blockcontainer jli-notice-warning "It's almost the same as JavaScript.">}}

⚠️ Be careful of the two dots instead of three dots syntax…

{{< /blockcontainer >}}

### Pattern Matching Enhancements

The pattern matching is now more powerful, enabling property patterns, relational patterns, and negation directly in conditions.

```csharp
// Property patterns in switch
switch (shape)
{
    case Circle { Radius: var radius }:
        Console.WriteLine($"Radius: {radius}");
        break;
    case Rectangle { Width: var width, Height: var height }:
        Console.WriteLine($"Width: {width}, Height: {height}");
        break;
}

// Relational patterns
if (value is >= 10 and <= 20)
{
    // value is between 10 and 20 inclusive
}

// Negation patterns
if (shape is not Circle)
{
    // shape is not a Circle
}
```

[^1]: [https://learn.microsoft.com/fr-fr/dotnet/core/whats-new/dotnet-8/overview](https://learn.microsoft.com/fr-fr/dotnet/core/whats-new/dotnet-8/overview)

[^2]: [https://www.bytehide.com/blog/net-8-has-been-released-summary-new-features](https://www.bytehide.com/blog/net-8-has-been-released-summary-new-features)

[^3]: [https://www.techcronus.com/blog/dot-net-8-features/](https://www.techcronus.com/blog/dot-net-8-features/)

[^4]: [https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-8.0](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-8.0)

[^5]: [https://www.syncfusion.com/blogs/post/whats-new-dot-net-8-for-developers](https://www.syncfusion.com/blogs/post/whats-new-dot-net-8-for-developers)

[^6]: [https://dev.to/pvsdev/whats-new-in-net-8-2l8j](https://dev.to/pvsdev/whats-new-in-net-8-2l8j)

[^7]: [https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/overview](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/overview)

[^8]: [https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-12](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-12)

[^9]: [https://dev.to/ssukhpinder/primary-constructors-in-c-12-3ol1](https://dev.to/ssukhpinder/primary-constructors-in-c-12-3ol1)

[^10]: [https://www.c-sharpcorner.com/blogs/default-values-for-lambda-expressions-in-c-sharp-122](https://www.c-sharpcorner.com/blogs/default-values-for-lambda-expressions-in-c-sharp-122)

[^11]: [https://www.c-sharpcorner.com/article/alias-any-type-in-c-sharp-12/](https://www.c-sharpcorner.com/article/alias-any-type-in-c-sharp-12/)

[^12]: [https://www.capitalnumbers.com/blog/c-sharp-12-new-features/](https://www.capitalnumbers.com/blog/c-sharp-12-new-features/)

[^13]: [https://www.c-sharpcorner.com/blogs/primary-constructors-in-c-sharp-12](https://www.c-sharpcorner.com/blogs/primary-constructors-in-c-sharp-12)
