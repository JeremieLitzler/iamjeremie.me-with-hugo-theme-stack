---
title: "What’s New With C# 7.3"
description: "Below is a comprehensive summary, with examples, of the most important updates in C# 7.3, the last major version in the .NET framework and .NET 2.x."
image: 2018-06-01-csharp-7-3-logo.svg
imageAlt: An image made with Claude.ai with the text "C# 7.3"
date: 2018-06-01
categories:
  - Web Development
tags:
  - DotNet
  - Csharp
---

## Summary of New Features in C# 7.3

C# 7.3 introduced several enhancements focused on performance, safety, and incremental improvements to existing features.

Here are the main new code features, along with code examples to illustrate their usage:

## Performance and Safety Features

### Reassignable `ref` Local Variables

You can now reassign `ref` local variables, making them behave more like traditional variables.

```csharp
int a = 10, b = 20;
ref int refVar = ref a;
refVar = ref b; // Now allowed in C# 7.3
refVar = 30;    // b is now 30
```

### Initializers on `stackalloc` Arrays

Before C# 7.3, the stackalloc operator could only be used within unsafe contexts and for pointer types, making it impossible to initialize a `Span<T>` or a managed array directly with a list of values in safe code. Instead, you would need to allocate memory on the stack using unsafe code and then manually copy or initialize the data.

Here's how you could emulate the original example:

```csharp
// Unsafe block required for pointer operations
unsafe
{
    // Allocate memory for 4 integers on the stack
    int* numbersPtr = stackalloc int[^4];

    // Initialize the array elements
    numbersPtr[^0] = 1;
    numbersPtr[^1] = 2;
    numbersPtr[^2] = 3;
    numbersPtr[^3] = 4;

    // Use the pointer as needed
    for (int i = 0; i < 4; i++)
    {
        Console.WriteLine(numbersPtr[i]);
    }
}
```

The alternative in safe code (pre-C# 7.3) would look like this:

Use a managed array:

```csharp
int[] numbers = new int[] { 1, 2, 3, 4 };
```

Or, if you need a span over a managed array:

```csharp
int[] array = { 1, 2, 3, 4 };
Span<int> span = array.AsSpan();
```

Now, you can use initializers to allocate and initialize stack memory in a single statement.

```csharp
Span numbers = stackalloc int[] { 1, 2, 3, 4 }; // New in 7.3
```

### Access Fixed Fields Without Pinning

You can now access fixed-size buffer fields in structs without needing a pinning statement.

### `fixed` Statement Pattern Support

The `fixed` statement can now operate on any type that has a suitable `GetPinnableReference` method, not just arrays or strings.

I haven't quite understood the concept behind it, the `fixed` statement pattern in C# is primarily used to enable safe and efficient access to the memory address of managed objects, especially when interoperating with native code or performing performance-critical operations that require pointers.

The "pattern" aspect refers to the ability, introduced in C# 7.3, for user-defined types to participate in the fixed statement by implementing a specific method signature.

Maybe, someday, I will work on something that requires. Or it will be replaced by some more efficient methods.

## New Generic Constraints

C# 7.3 introduced the `unmanaged`, `Enum`, and `Delegate` generic type constraints to address longstanding limitations in the language's generics system. These constraints were added to enable more precise and type-safe generic programming, especially in scenarios that previously required workarounds or were outright impossible.

### Why Were These Constraints Introduced?

**1. The `unmanaged` Constraint**

- **Purpose:** Allows you to restrict a generic type parameter to unmanaged types—those that can be represented as a contiguous block of memory and do not contain any references to managed objects.
- **Why Needed:** This is particularly useful for low-level programming tasks such as interop with native code, serialization, or any scenario requiring direct memory manipulation. Previously, you could only use the `struct` constraint, which was too broad and included types with reference fields, making certain operations unsafe or impossible without reflection or unsafe code.
- **Benefit:** With the `unmanaged` constraint, you can now write reusable, type-safe methods that operate on any unmanaged type, enabling efficient memory operations and interop scenarios without sacrificing type safety[^1] [^2] [^4] [^5].

**2. The `Enum` Constraint**

- **Purpose:** Restricts a generic type parameter to be an enumeration type.
- **Why Needed:** Before C# 7.3, there was no way to ensure at compile time that a generic parameter was an enum. Developers had to use awkward workarounds (like combining `struct` and `IConvertible` constraints) or rely on runtime checks, which were less efficient and less safe.
- **Benefit:** The new constraint allows you to write generic methods and classes that work specifically with enums, enabling compile-time safety and eliminating the need for reflection or complex workarounds. This is useful for utility methods that operate on enums, such as value parsing, validation, or conversion to strings[^1] [^3] [^5] [^6].

**3. The `Delegate` Constraint**

- **Purpose:** Restricts a generic type parameter to delegate types.
- **Why Needed:** There was previously no way to enforce at compile time that a generic parameter was a delegate. This limited the ability to write generic code that manipulates delegates, such as combining or invoking them in a type-safe way.
- **Benefit:** The `Delegate` constraint now allows you to create generic methods and classes that operate only on delegates, ensuring type safety and enabling more expressive APIs for event handling, command patterns, or expression trees[^1] [^2] [^4] [^7].

### Technical Background

- **CLR Support:** The underlying .NET runtime (CLR) has always supported these constraints, but the C# language did not expose them until version 7.3. This means the addition was mainly a language design decision to make generics more expressive and type-safe.
- **Community Demand:** Developers had long requested these features, especially the `Enum` constraint, as generics became more widely used and the limitations became more apparent.

### Examples With `unmanaged`, `Enum`, and `Delegate` Constraints

You can now constrain generic type parameters to unmanaged types, enums, or delegates.

```csharp
// Unmanaged constraint
void ProcessBuffer(T[] buffer) where T : unmanaged
{
    // Can use pointers safely
}

// Enum constraint
void PrintEnumName(T value) where T : Enum
{
    Console.WriteLine(value.ToString());
}

// Delegate constraint
void RegisterHandler(T handler) where T : Delegate
{
    handler.DynamicInvoke();
}
```

## Quality of Life Improvements

### Declaration Expressions in Initializers and Queries

You can now use `out var` and pattern variables in field initializers, property initializers, constructor initializers, and LINQ queries.

Very practical to avoid two lines of code!

```csharp
// Field initializer
public class Example
{
    private int value = int.TryParse("42", out var i) ? i : 0;
}

// Constructor initializer
public class Example2
{
    public int Number;
    public Example2(string s) : this(int.TryParse(s, out var i) ? i : 0) {}
    public Example2(int n) { Number = n; }
}
```

### Tuple Equality Operators

You can now compare tuples using `==` and `!=`.

```csharp
var t1 = (1, "hello");
var t2 = (1, "hello");
bool areEqual = t1 == t2; // true
```

### Attach Attributes to Backing Fields

You can now use `[field: Attribute]` to attach attributes directly to the backing field of auto-implemented properties.

```csharp
public class Example
{
    [field: NonSerialized]
    public int Data { get; set; }
}
```

### Improved Overload Resolution

The compiler is now better at resolving overloads, especially when arguments differ by `in`, reducing ambiguous cases.

Before C# 7.3, the following would generator a compilation error:

```csharp
struct S { }

static void M(S arg) { Console.WriteLine("by value"); }
static void M(in S arg) { Console.WriteLine("by in"); }
```

C# 7.3 introduced a rule: if you call M(s), the compiler will choose the by-value overload. If you want the in overload, you must explicitly use the in modifier:

```csharp
S s = new S();
M(s);      // Calls: static void M(S arg)
M(in s);   // Calls: static void M(in S arg)
```

[^1]: [https://blog.jetbrains.com/dotnet/2018/07/19/unmanaged-delegate-enum-type-constraints-c-7-3-rider-resharper/](https://blog.jetbrains.com/dotnet/2018/07/19/unmanaged-delegate-enum-type-constraints-c-7-3-rider-resharper/)

[^2]: [https://devblogs.microsoft.com/premier-developer/dissecting-new-generics-constraints-in-c-7-3/](https://devblogs.microsoft.com/premier-developer/dissecting-new-generics-constraints-in-c-7-3/)

[^3]: [https://dotnetfalcon.com/whats-new-in-c-7-3/](https://dotnetfalcon.com/whats-new-in-c-7-3/)

[^4]: [https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters)

[^5]: [https://www.infoq.com/news/2018/05/CSharp-7.3/](https://www.infoq.com/news/2018/05/CSharp-7.3/)

[^6]: [https://stackoverflow.com/questions/50218754/c-sharp-7-3-enum-constraint-why-cant-i-use-the-enum-keyword](https://stackoverflow.com/questions/50218754/c-sharp-7-3-enum-constraint-why-cant-i-use-the-enum-keyword)

[^7]: [https://www.telerik.com/blogs/constraining-generics-in-c](https://www.telerik.com/blogs/constraining-generics-in-c)
