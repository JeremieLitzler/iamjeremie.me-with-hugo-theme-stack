---
title: "Simple Factory vs. Factory Method Patterns"
description: "The Factory Method Pattern and the Simple Factory are both creational design patterns used to create objects, but they do so in different ways."
image: 2025-05-13-simple-factory-pattern-vs-factory-method-pattern-image.jpg
imageAlt: Simple Factory vs. Factory Method” over a gradient background
date: 2025-05-13
categories:
  - Software Development
tags:
  - Design Patterns
---

## Simple Factory Pattern

The Simple Factory encapsulates the object creation process in a single method and doesn’t involve inheritance. It’s a basic implementation where a class contains a method for creating instances of other classes. This method typically takes parameters to decide which instance to create.

Here is an example in C#:

```csharp
public class ShapeFactory
{
    public enum ShapeType
    {
        Circle,
        Square
    }

    public static IShape CreateShape(ShapeType type)
    {
        switch (type)
        {
            case ShapeType.Circle:
                return new Circle();
            case ShapeType.Square:
                return new Square();
            default:
                throw new ArgumentException("Invalid type");
        }
    }
}

public interface IShape
{
    void Draw();
}

public class Circle : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a Circle");
    }
}

public class Square : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a Square");
    }
}

// Usage
class Program
{
    static void Main(string[] args)
    {
        IShape circle = ShapeFactory.CreateShape(ShapeFactory.ShapeType.Circle);
        circle.Draw();

        IShape square = ShapeFactory.CreateShape(ShapeFactory.ShapeType.Square);
        square.Draw();
    }
}
```

## Factory Method Pattern

The Factory Method Pattern involves a method in a base class which is overridden by subclasses to create specific instances. This pattern uses inheritance and relies on subclasses to handle the instantiation of objects.

Here is the example in C#:

```csharp
// Abstract class
public interface IShape
{
    void Draw();
}

// Concrete class: Circle
public class Circle : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a Circle");
    }
}

// Concrete class: Square
public class Square : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a Square");
    }
}

// Abstract Creator
public abstract class ShapeFactory
{
    public abstract IShape CreateShape();

    public void DrawShape()
    {
        var shape = CreateShape();
        shape.Draw();
    }
}

// Concrete Creator: Circle Factory
public class CircleFactory : ShapeFactory
{
    public override IShape CreateShape()
    {
        return new Circle();
    }
}

// Concrete Creator: Square Factory
public class SquareFactory : ShapeFactory
{
    public override IShape CreateShape()
    {
        return new Square();
    }
}

// Usage
class Program
{
    static void Main(string[] args)
    {
        ShapeFactory circleFactory = new CircleFactory();
        circleFactory.DrawShape();

        ShapeFactory squareFactory = new SquareFactory();
        squareFactory.DrawShape();
    }
}

```

## Let’s Compare the Two Approaches

1. **Inheritance**:
   - In the **Simple Factory**, we use a single class with a static method. It doesn’t involve inheritance.
   - In the **Factory Method**, we use inheritance. The base class defines a factory method and subclasses override it to create specific instances.
2. **Flexibility and Extensibility**:
   - In the **Simple Factory**, adding a new product requires modifying the factory class, which may violate the Open/Closed Principle.
   - In the **Factory Method**, adding a new product involves creating a new subclass. The base class doesn’t need to change, adhering to the Open/Closed Principle.
3. **Responsibility**:
   - In the **Simple Factory**, the method is responsible for deciding which class to instantiate based on parameters.
   - In the **Factory Method**, the decision of which class to instantiate remains in the subclasses.

## Sources For More Reading

- “Design Patterns: Elements of Reusable Object-Oriented Software” by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (Gang of Four)
- [Microsoft Docs—Factory Method](https://learn.microsoft.com/en-us/dotnet/standard/design-patterns/factory-method)
- [Refactoring Guru—Factory Method](https://refactoring.guru/design-patterns/factory-method)

These examples and explanations should enrich your understanding of both patterns and their differences.

The Factory Method Pattern is the one that we use the most in software development, but you’ll see or use the Simple Factory for time to time.

The Factory Method may look like overkill in terms of boilerplate code you need.

Depending on your codebase and size of the project, you may prefer one method over the other.

Adhering to the Open/Closed Principle may guide your choice.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
