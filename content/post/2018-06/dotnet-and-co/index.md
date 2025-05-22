---
title: "History of .NET and C# from .NET 4.7.2"
description: "All the versions of .NET and C# from 4.7.2 and on."
image: 2018-06-02-history-of-dotnet.svg
imageAlt:
date: 2018-06-02
categories:
  - Web Development
tags:
  - Dot Net
  - Csharp
---

Here is a list of the major .NET and C# versions starting from .NET Framework 4.7.2, including subsequent .NET Core and .NET releases, and their associated C# language versions.

## Major .NET Versions (from .NET Framework 4.7.2 onward)

| .NET Version         | Release Year | Notes                                                                                                                                                |
| -------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| .NET Framework 4.7.2 | 2018         | Last in-place update before 4.8; improvements across ASP.NET, BCL, CLR, etc.[^1][^6][^4]                                                             |
| .NET Framework 4.8   | 2019         | Final major .NET Framework version; future work moved to .NET Core[^1]                                                                               |
| .NET Core 2.0        | 2017         | Start of cross-platform, open-source .NET Core era                                                                                                   |
| .NET Core 2.1        | 2018         | LTS release; supported until 2021                                                                                                                    |
| .NET Core 3.0        | 2019         | Added Windows desktop app support (WinForms, WPF)                                                                                                    |
| .NET Core 3.1        | 2019         | LTS release; widely adopted for cross-platform apps                                                                                                  |
| .NET 5               | 2020         | Unified .NET Core and .NET Framework; dropped "Core" from name                                                                                       |
| .NET 6               | 2021         | LTS release; major improvements and new features. [More details in this article](../../../post/2021-12/whats-new-with-dotnet6/index.md).             |
| .NET 7               | 2022         | Current release cadence: annual major updates                                                                                                        |
| .NET 8               | 2023         | LTS release; continued performance and language enhancements. [More details in this article](../../../post/2023-12/whats-new-with-dotnet8/index.md). |
| .NET 9               | 2024         | Latest non-LTS release (as of April 2025)[^3]                                                                                                        |

## Major C# Versions (from C# 7.3 onward)

| C# Version | Associated .NET Version(s)          | Major Features/Notes                                                                                                                                                                          |
| ---------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7.3        | .NET Framework (all), .NET Core 2.x | Last version for .NET Framework; performance and language improvements[^3]. [More details in this article](../../../post/2018-06/whats-new-in-csharp-7-3/index.md).                           |
| 8.0        | .NET Core 3.x, .NET Standard 2.1    | Nullable reference types, async streams, ranges, switch expressions[^3] [^5]                                                                                                                  |
| 9.0        | .NET 5                              | Records, init-only setters, top-level statements, pattern matching enhancements[^3] [^5]                                                                                                      |
| 10.0       | .NET 6                              | Record structs, global usings, file-scoped namespaces[^3] [^5]. [More details in this article](../../../post/2021-12/whats-new-with-dotnet6/index.md#c-10-new-coding-features-with-examples). |
| 11.0       | .NET 7                              | Raw string literals, list patterns, required members[^3]                                                                                                                                      |
| 12.0       | .NET 8                              | Collection expressions, primary constructors for classes[^3]. [More details in this article](../../../post/2023-12/whats-new-with-dotnet8/index.md#c-12-new-coding-features-with-examples).   |
| 13.0       | .NET 9                              | Latest features as of 2025[^3]                                                                                                                                                                |

## .NET and C# Version Mapping

| .NET Version       | Default C# Version |
| ------------------ | ------------------ |
| .NET Framework 4.x | 7.3                |
| .NET Core 2.x      | 7.3                |
| .NET Core 3.x      | 8.0                |
| .NET 5             | 9.0                |
| .NET 6             | 10.0               |
| .NET 7             | 11.0               |
| .NET 8             | 12.0               |
| .NET 9             | 13.0               |

## Summary

- **.NET Framework 4.7.2** was released in April 2018, followed by 4.8, which is the final major .NET Framework version[^1][^6][^4].
- **.NET Core** evolved into the unified **.NET 5+** platform, which is now the future of .NET development.
- **C# 7.3** is the last version officially supported by .NET Framework; newer C# features require .NET Core 3.x or later[^3].
- **C# versions** continue to advance with each major .NET release, with C# 13 being the latest as of 2025[^3].

This overview should help you track the major .NET and C# versions relevant to modern development scenarios.

[^1]: https://en.wikipedia.org/wiki/.NET_Framework_version_history

[^2]: https://www.c-sharpcorner.com/article/c-sharp-versions/

[^3]: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-versioning

[^4]: https://support.microsoft.com/en-us/topic/microsoft-net-framework-4-7-2-offline-installer-for-windows-05a72734-2127-a15d-50cf-daf56d5faec2

[^5]: https://www.reddit.com/r/csharp/comments/1d9r3ck/whats_the_most_significant_release_version_of_c/

[^6]: https://visualstudiomagazine.com/articles/2018/05/01/net-framework-update.aspx

[^7]: https://dotnetcrunch.in/csharp-version-history-features/

[^8]: https://dotnet.microsoft.com/en-us/download/dotnet-framework/net472

[^9]: https://dotnet.microsoft.com/fr-fr/download/dotnet-framework/net472

[^10]: https://support.microsoft.com/fr-fr/topic/programme-d-installation-microsoft-net-framework-4-7-2-hors-connexion-pour-windows-05a72734-2127-a15d-50cf-daf56d5faec2

[^11]: https://learn.microsoft.com/fr-fr/dotnet/framework/migration-guide/versions-and-dependencies

[^12]: https://learn.microsoft.com/fr-fr/dotnet/csharp/language-reference/language-versioning

[^13]: https://learn.microsoft.com/en-us/dotnet/framework/install/versions-and-dependencies

[^14]: https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-version-history

[^15]: https://learn.microsoft.com/fr-fr/dotnet/csharp/language-reference/configure-language-version

[^16]: https://github.com/Microsoft/dotnet/blob/master/releases/net472/dotnet472-changes.md

[^17]: https://learn.microsoft.com/fr-fr/dotnet/csharp/whats-new/csharp-version-history

[^18]: https://www.reddit.com/r/csharp/comments/xng9em/choosing_c_version_for_project/

[^19]: https://learn.microsoft.com/fr-fr/dotnet/framework/migration-guide/how-to-determine-which-versions-are-installed

[^20]: https://stackoverflow.com/questions/28669786/are-c-sharp-and-net-versions-dependent-on-each-other
