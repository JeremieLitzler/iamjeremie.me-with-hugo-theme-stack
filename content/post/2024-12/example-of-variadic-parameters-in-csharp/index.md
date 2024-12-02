---
title: "What is an example of Variadic Parameters?"
description: "Variadic parameters allow you to pass a variable number of arguments to a method."
image: images/2024-12-02-code-example-of-variadic-parameter.jpg
imageAlt: Code example of variadic parameter
date: 2024-12-02
categories:
  - Web Development
---

This keyword is used before the parameter type in the method signature. Here is an example to illustrate how variadic parameters work in C#:

## Example of Variadic Parameters in C#

```csharp
using System;

public class VariadicExample
{
    // Method that accepts a variable number of integer parameters
    public static int Sum(params int[] numbers)
    {
        int total = 0;
        foreach (int number in numbers)
        {
            total += number;
        }
        return total;
    }

    public static void Main(string[] args)
    {
        // Calling the method with different numbers of parameters
        Console.WriteLine(Sum(1, 2, 3));       // Output: 6
        Console.WriteLine(Sum(1, 2, 3, 4, 5)); // Output: 15
        Console.WriteLine(Sum(10, 20));        // Output: 30
        Console.WriteLine(Sum());              // Output: 0
    }
}

```

## Explanation

We start with the **Method Declaration**:

```csharp
public static int Sum(params int[] numbers)
```

The `params` keyword allows the method to accept a variable number of integer arguments. These arguments are treated as an array within the method.

Then, we use the parameter like this:

```csharp
int total = 0;
foreach (int number in numbers)
{
    total += number;
}
return total;

```

The method iterates through the `numbers` array, summing up all the values.

Let’s take usage examples:

```csharp
  Console.WriteLine(Sum(1, 2, 3));
  Console.WriteLine(Sum(1, 2, 3, 4, 5));
  Console.WriteLine(Sum(10, 20));
  Console.WriteLine(Sum());
```

The method `Sum` is called with different numbers of arguments. The `params` keyword allows the method to handle these calls gracefully.

## Type Checking

Naturally, the parameters must all match the type on the variadic parameters. At least, in C#, it’s the case.

However, this isn’t true for all languages: for example, if you use plain JavaScript, you can use variadic parameters through the spread operator (`...numbers`) if you use modern JavaScript.

```javascript
function sumOfNumbers(...numbers) {
  return numbers.reduce((total, current) => total + current, 0);
}

console.log(sumOfNumbers(1, 2, 3, 4)); // Output: 10
```

It replaced the use of the implicit `arguments` variable.

Consequently, if you had the following code:

```javascript
function SumOfNum() {
  let total = 0;
  for (let i = 0; i < arguments.length; i++) {
    total += arguments[i];
  }
  return total;
}

console.log("Sum is ", SumOfNum(1, 2, 3, "4"));
```

You would get this output:

```plaintext
Sum is 64
```

To solve that issue (unless you really need that behavior), using TypeScript’s static typing bring the C# strength:

```ts
// Basic numeric sum function
function sumNumbers(...numbers: number[]): number {
  return numbers.reduce((total, num) => total + num, 0);
}

// TypeScript will generate a compile-time error
console.log("Sum is ", SumOfNum(1, 2, 3, "4"));
```

## Why Use Variadic Parameters

Variadic parameters simplify the method signature and makes the code more flexible and easier to maintain, avoiding method signature proliferation for different numbers of parameters.

Have you ever used variadic parameters? Maybe, today, you’ll find code where you could apply the programming feature.

Did you learn something?

{{< blockcontainer jli-notice-tip "Follow me">}}

If so, make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

Thanks for reading this article
{{< /blockcontainer >}}

<!-- more -->
