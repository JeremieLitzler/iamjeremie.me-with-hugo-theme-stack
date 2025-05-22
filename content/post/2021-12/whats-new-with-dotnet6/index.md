---
title: "What’s New With .NET 6 and C# 10"
description: "Below is a comprehensive summary of the most important updates of .NET 6, released on November 14, 2023 as a Long-Term Support (LTS) version."
image: 2021-12-01-dotnet-6-logo.svg
imageAlt: A .NET 6.0 made with Claude.ai
date: 2021-12-01
categories:
  - Web Development
tags:
  - DotNet
  - Csharp
---

## .NET 6.0: Full Summary of What’s New

.NET 6.0, released in November 2021[^1], is a major Long-Term Support (LTS) release, marking the completion of the .NET unification journey between .NET Framework with .NET Core. It brings significant improvements in performance, developer productivity, and platform reach, and introduces new features across the entire ecosystem.

First, it unifies the SDK, base libraries, and runtime across cloud, desktop, mobile, IoT, and web apps, making code sharing and cross-platform development easier than ever[^1] [^4] [^7].
It brings support for three years, providing stability for enterprise adoption[^1] [^4].

We find the following major new features

- **Performance Improvements** with:

  - Extensive optimizations throughout the runtime and libraries, resulting in faster execution, lower latency, and reduced memory usage[^1] [^4] [^5].
  - FileStream has been rewritten for better async I/O performance, especially on Windows[^1] [^3] [^4].
  - Introduction of dynamic Profile-Guided Optimization (PGO) for runtime-tuned code generation[^1] [^4] [^5].
  - Crossgen2 replaces the original Crossgen tool for more advanced ahead-of-time (AOT) compilation[^1].

- **Developer Productivity**

  - **Hot Reload**: Make code changes and see them immediately in running apps, without rebuilding or restarting—supported in Visual Studio 2022 and the .NET CLI[^1] [^3] [^4] [^7] [^8].
  - **Minimal APIs**: Build lightweight HTTP APIs with minimal dependencies and code, ideal for microservices and small web services[^1] [^4] [^6] [^7] [^8].
  - **C# 10**: New language features like global usings, file-scoped namespaces, record structs, and improved lambda expressions simplify code and boost productivity[^1] [^4]. We’ll review the new features [with examples later in the article](#c-10-new-coding-features-with-examples).
  - **F# 6**: Enhanced async programming, pipeline debugging, and performance improvements[^4].
  - **Visual Basic**: Improvements to the Visual Studio experience and Windows Forms project handling[^4].

{{< blockcontainer jli-notice-warning "Hot Reload... Efficient?">}}

It really depends. After working on a large application bundled with an Angular frontend in 2024, I cannot say it is as snappy as Vue.js with Vite.

{{< /blockcontainer >}}

- **Cloud and Diagnostics**

  - Improved cloud diagnostics with built-in support for OpenTelemetry and dotnet monitor, now production-ready and available in Azure App Service[^2] [^4].
  - Enhanced logging with a new source generator for performant logging APIs[^1].

- **Web and Networking**

  - **HTTP/3 Support**: ASP.NET Core, HttpClient, and gRPC can now interact with HTTP/3 clients and servers, improving network performance and reliability[^4] [^7] [^8].
  - **WebAssembly Enhancements**: Better performance, native dependencies, and AOT compilation for Blazor WebAssembly apps[^4].
  - **Blazor Improvements**: Components can be rendered from JavaScript, enabling tighter integration with JS-based apps[^4].
  - **Single-Page App (SPA) Pattern**: More flexible integration with popular JavaScript frameworks like Angular and React[^4].
  - **Async Streaming & W3C Logging**: Enhanced support for returning data before response completion and IIS-style logging in ASP.NET Core[^8].

- **Cross-Platform and UI**

  - **.NET MAUI (Multi-platform App UI) Support**: Enables building cross-platform apps for Android, iOS, macOS, and Windows from a single codebase[^4] [^7].
  - **Native Apple Silicon (Arm64) Support**: Full native support for Apple M1/M2 chips, as well as improved Windows Arm64 support[^4].

- **APIs and Libraries**

  - **New Reflection APIs**: Added types to inspect code for nullability, aiding tools and serializers[^1].
  - **DateOnly and TimeOnly**: New structs for date-only and time-only values, simplifying scenarios like birthdays and business hours[^1].
  - **Time Zone Enhancements**: Support for both IANA and Windows time zone IDs, with automatic conversion and new helper methods[^1].
  - **LINQ Improvements**: New methods and optimizations for querying data[^1] [^7].
  - **JSON APIs**: More capable and higher-performance JSON serialization, including source generation for serializers[^4].

## C# 10 New Coding Features with Examples

C# 10, introduced with .NET 6, brings several enhancements that streamline code, improve readability, and boost productivity. Here are some of the most notable features with practical examples.

### 1. Constant Interpolated Strings

Previously, `const` strings could not use string interpolation. In C# 10, you can now declare constant interpolated strings as long as all expressions are themselves constants.

```csharp
const string Name = "Alan";
const string Designation = $"{Name} - Employee"; // Valid in C# 10

string NameNonConstant = "Alan";
const string Designation = $"{Name} - Employee"; // Invalid in C# 10

```

### 2. Global Using Directives

You can now declare `using` directives as global, making them available across the entire project and eliminating repetitive `using` statements in every file.

```csharp
// In GlobalUsings.cs
global using System;
global using System.Collections.Generic;
```

Now, `System` and `System.Collections.Generic` are available everywhere in your project without explicit imports in each file[^9][^11].

### 3. File-Scoped Namespace Declaration

File-scoped namespaces reduce indentation and boilerplate by applying a namespace to the entire file with a single line.

```csharp
namespace MyProject.Models;

public class Person
{
    public string Name { get; set; }
}
```

This replaces the older, more verbose block-style namespace[^10] [^12].

### 4. Lambda Improvements

- **Natural Types for Lambdas:** The compiler can now infer delegate types for lambdas, reducing the need for explicit type declarations.
- **Lambda Return Types and Attributes:** You can specify return types and apply attributes to lambdas.

```csharp
var numbers = new List { 1, 2, 3, 4, 5 };
var evenNumbers = numbers.Where(x => x % 2 == 0); // Natural type inference

Func add = (int x, int y) => x + y; // Explicit return type if needed
```

### 5. File-Scoped Types

You can now declare types that are only accessible within the file using the `file` modifier.

```csharp
file class InternalHelper
{
    // Only accessible within this file
}
```

### 6. Extended Property Patterns

Property patterns in switch expressions are more powerful and concise.

```csharp
if (person is { Address.City: "London" })
{
    // Matches if person's address city is London
}
```

### 7. Record Structs

You can now declare record structs for value-type records.

```csharp
public readonly record struct Point(int X, int Y);
```

### 8. Assignment and Declaration in Deconstruction

You can declare and assign variables in a single deconstruction statement.

```csharp
(string firstName, string lastName) = GetName();
```

[^1]: [https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-6)

[^2]: [https://www.c-sharpcorner.com/article/what-is-new-in-net-6-0/](https://www.c-sharpcorner.com/article/what-is-new-in-net-6-0/)

[^3]: [https://www.bigscal.com/blogs/backend/net-6-introduction-features-example/](https://www.bigscal.com/blogs/backend/net-6-introduction-features-example/)

[^4]: [https://devblogs.microsoft.com/dotnet/announcing-net-6/](https://devblogs.microsoft.com/dotnet/announcing-net-6/)

[^5]: [https://brainhub.eu/library/net-6-upgrade](https://brainhub.eu/library/net-6-upgrade)

[^6]: [https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-6.0](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-6.0)

[^7]: [https://www.softacom.com/wiki/development/asp-net-6-0-improvements-of-net-6/](https://www.softacom.com/wiki/development/asp-net-6-0-improvements-of-net-6/)

[^8]: [https://www.youtube.com/watch?v=UMkir_Qey8Y](https://www.youtube.com/watch?v=UMkir_Qey8Y)

[^9]: [https://gunnarpeipman.com/global-usings/](https://gunnarpeipman.com/global-usings/)

[^10]: [https://www.jetbrains.com/guide/dotnet/tips/file-scoped-namespaces/](https://www.jetbrains.com/guide/dotnet/tips/file-scoped-namespaces/)

[^11]: [https://devblogs.microsoft.com/dotnet/welcome-to-csharp-10/](https://devblogs.microsoft.com/dotnet/welcome-to-csharp-10/)

[^12]: [https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history)
