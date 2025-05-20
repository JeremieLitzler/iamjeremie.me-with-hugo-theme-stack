---
title: "What is the Decorator Pattern"
description: "The Decorator pattern is a structural design pattern used to extend the functionality of objects in a flexible and reusable way."
image: 2025-05-23-4-colored-paint-brushes.jpg
imageAlt: 4 colored paint brushes
date: 2025-05-23
categories:
  - Software Development
tags:
  - Design Patterns
---

In C#, using the Decorator design pattern involves creating a set of decorator classes that are used to wrap concrete components. Here is a concrete example and some common use cases.

Let’s create a simple example involving a `Notifier` system where we can send notifications via different channels (Email, SMS, etc.).

## Step 1: Create a Component Interface

This step is essential to define the contract that the decorators will need to implement.

```csharp
public interface INotifier
{
    void Send(string message);
}
```

## Step 2: Create Concrete Components

```csharp
public class EmailNotifier : INotifier
{
    public void Send(string message)
    {
        Console.WriteLine($"Sending Email: {message}");
    }
}

```

## Step 3: Create Base Decorator Class

```csharp
public class NotifierDecorator : INotifier
{
    protected INotifier _notifier;

    public NotifierDecorator(INotifier notifier)
    {
        _notifier = notifier;
    }

    public virtual void Send(string message)
    {
        _notifier.Send(message);
    }
}

```

## Step 4: Create Concrete Decorators

```csharp
public class SMSNotifier : NotifierDecorator
{
    public SMSNotifier(INotifier notifier) : base(notifier)
    {
    }

    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"And sending SMS: {message}");
    }
}

public class FacebookNotifier : NotifierDecorator
{
    public FacebookNotifier(INotifier notifier) : base(notifier)
    {
    }

    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"And posting on Facebook: {message}");
    }
}

```

## Step 5: Use Decorators

Let’s put the code to the test:

```csharp
class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine($"## Use case: just Email");
        INotifier emailNotifier = new EmailNotifier();
        emailNotifier.Send("Hello World!");

        Console.WriteLine($"## Use case: Email+SMS");
        var smsNotifier = new SMSNotifier(emailNotifier);
        smsNotifier.Send("Hello World!");

        Console.WriteLine($"## Use case: Email+SMS+Facebook");
        var facebookNotifier = new FacebookNotifier(smsNotifier);
        facebookNotifier.Send("Hello World!");

        Console.WriteLine($"## Use case: Email+Facebook");
        var facebookNotifier2 = new FacebookNotifier(emailNotifier);
        facebookNotifier2.Send("Hello World!");
    }
}
```

### What’s the Output?

```plaintext
## Use case: just Email
Sending Email: Hello World!
## Use case: Email+SMS
Sending Email: Hello World!
And sending SMS: Hello World!
## Use case: Email+SMS+Facebook
Sending Email: Hello World!
And sending SMS: Hello World!
And posting on Facebook: Hello World!
## Use case: Email+Facebook
Sending Email: Hello World!
And posting on Facebook: Hello World!
```

### Step by Step Explanation

The first test is simple. Nothing special to explain.

The second, third and fourth tests show the Decorator pattern in action.

If you look at the third test, `facebookNotifier` wraps `smsNotifier`, itself wrapping `emailNotifier`.

`emailNotifier` is the base and when you call `facebookNotifier.Send("Hello World!")`, here’s what happens:

- `FacebookNotifier.Send` is called and the first thing happening within the method is a call to `base.Send(message)` (which is `smsNotifier.Send`).

- So then `SMSNotifier.Send` is called. Again the first thing happening within the method is a call to `base.Send(message)` (which is `emailNotifier.Send`).

- So `EmailNotifier.Send` is called and it prints “Sending Email: Hello World!”.

- Then control returns to `SMSNotifier.Send`, which prints “And sending SMS: Hello World!”.
- And finally control returns to `FacebookNotifier.Send`, which prints “And posting on Facebook: Hello World!”.

Each decorator adds its own behavior after calling the wrapped object’s method.

```plaintext
FacebookNotifier.Send
    -> SMSNotifier.Send
        -> EmailNotifier.Send
            (prints "Sending Email: Hello World!")
        (prints "And sending SMS: Hello World!")
    (prints "And posting on Facebook: Hello World!")

```

## Common Use Cases

When you want to:

1. **Extend Functionality**: When you want to add responsibilities to individual objects, not to an entire class.
2. **Combine Behaviors**: When you need to add a combination of behaviors at runtime. For example, combining various logging, authentication, or notification behaviors.
3. **Adhere to Single Responsibility Principle**: By using decorators, you can divide a class’s functionality into separate classes with specific responsibilities.
4. **Build User Interface**: Wrapping user interface elements to add responsibilities like borders, scrollbars, or decorations.
5. **Input/Output Streams**: Adding responsibilities to streams (e.g., adding buffering, encryption, compression, etc.).

## Sources

The resources below provide a comprehensive understanding of the Decorator pattern and its applications in software design.

- **Design Patterns: Elements of Reusable Object-Oriented Software** by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (Gang of Four)
- **Head First Design Patterns** by Eric Freeman, Elisabeth Robson
- [Microsoft Documentation on the Decorator Pattern](https://learn.microsoft.com/en-us/archive/msdn-magazine/2008/october/design-patterns-the-decorator-pattern)

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Nataliya Vaitkevich](https://www.pexels.com/photo/blue-and-white-paint-brush-5642113/)
