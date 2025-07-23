---
title: "Understanding the Open/Closed Principle"
description: "The Open/Closed Principle (OCP) is one of the S.O.L.I.D principles of object-oriented design, in particular the letter “O”"
image: 2025-07-21-opened-lock.jpg
imageAlt: Opened lock
date: 2025-07-21
categories:
  - Software Development
tags:
  - Design Pattern
  - Clean Code
---

The principle states that software entities (classes, modules, functions, etc.) should be open for extension but closed for modification. This means you should be able to add new functionality to an existing class without changing its existing code.

## Example of OCP Violation

Let’s consider a simple example where we have a `Shape` class with a `Draw` method. We want to support drawing different types of shapes, such as circles and rectangles.

The following example violates OCP:

```csharp
public class Shape
{
    public enum ShapeType
    {
        Circle,
        Rectangle
    }

    public ShapeType Type { get; set; }
    public double Radius { get; set; }
    public double Width { get; set; }
    public double Height { get; set; }

    public void Draw()
    {
        if (Type == ShapeType.Circle)
        {
            // Draw circle
            Console.WriteLine("Drawing Circle with Radius: " + Radius);
        }
        else if (Type == ShapeType.Rectangle)
        {
            // Draw rectangle
            Console.WriteLine("Drawing Rectangle with Width: " + Width + " and Height: " + Height);
        }
    }
}

```

In this example, if we want to add a new shape, we need to modify the `Shape` class and the `Draw` method. This violates the Open/Closed Principle because the class isn’t closed for modification.

## Fixing the Violation With Abstract and Derived Classes

To fix this violation, we can use polymorphism and abstract classes/interfaces to ensure that we can extend the functionality without modifying existing code.

```csharp
// Fixing Open/Closed Principle
public abstract class Shape
{
    public abstract void Draw();
}

public class Circle : Shape
{
    public double Radius { get; set; }

    public Circle(double radius)
    {
        Radius = radius;
    }

    public override void Draw()
    {
        Console.WriteLine("Drawing Circle with Radius: " + Radius);
    }
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }

    public Rectangle(double width, double height)
    {
        Width = width;
        Height = height;
    }

    public override void Draw()
    {
        Console.WriteLine("Drawing Rectangle with Width: " + Width + " and Height: " + Height);
    }
}

```

Now, if we want to add a new shape, such as a `Triangle`, we can do so without modifying the existing `Shape` class or the `Circle` and `Rectangle` classes.

```csharp
public class Triangle : Shape
{
    public double Base { get; set; }
    public double Height { get; set; }

    public Triangle(double @base, double height)
    {
        Base = @base;
        Height = height;
    }

    public override void Draw()
    {
        Console.WriteLine("Drawing Triangle with Base: " + Base + " and Height: " + Height);
    }
}

```

### Usage With Inheritance

Here’s how you can use the shapes:

```csharp
public class Program
{
    public static void Main(string[] args)
    {
        Shape circle = new Circle(5);
        Shape rectangle = new Rectangle(4, 6);
        Shape triangle = new Triangle(3, 4);

        List<Shape> shapes = new List<Shape> { circle, rectangle, triangle };

        foreach (Shape shape in shapes)
        {
            shape.Draw();
        }
    }
}

```

In this revised example, the `Shape` class is open for extension (you can add new shapes by inheriting from it) but closed for modification (you don’t need to change existing shape classes to add new functionality). This adheres to the Open/Closed Principle.

## Alternatives to Inheritance

Now, inheritance isn’t the single option. Here’s how the **Shape** abstraction and derived classes could be reimagined using other methods for implementing the Open/Closed Principle (OCP).

### Using Interfaces, Strategy Pattern and Dependency Injection

Replace the abstract base class with an **interface**:

```csharp
public interface IShape
{
    void Draw();
}
```

Then, we have the concrete classes to implement the interface:

```csharp
public class Circle : IShape
{
    // ... as before
    public void Draw()
    {
        Console.WriteLine("Drawing Circle with Radius: " + Radius);
    }
}

// Similarly, Rectangle and Triangle class would be implemented
```

Finally, using dependency injection, we can use the shape classes:

```csharp
public class ShapeBuilder
{
    private readonly IEnumerable<IShape> _shapes;

    public ShapeBuilder(IEnumerable<IShape> shapes) {
        _shapes = shapes;
    }

    public void Build()
    {
        foreach (var shape in _shapes) {
            shape.Draw();
        }
        ;
    }
}
```

In the program, we instantiate the shapes and provide them the `ShapeBuilder` constructor:

```csharp
public class Program
{
    public static void Main(string[] args)
    {
        IShape circle = new Circle(5);
        IShape rectangle = new Rectangle(4, 6);
        IShape triangle = new Triangle(3, 4);

        List<IShape> shapes = new List<IShape> { circle, rectangle, triangle };

        new ShapeBuilder(shapes).Build()
    }
}
```

With this structure, adding a new shape type (e.g., Hexagonal) only requires creating a new class that implements `IShape`, without modifying `ShapBuilder`, since we’ll provide it in the list of shapes that its constructor accepts.

But when should we use Abstract over Interface? Well, we could use both at the same time and that’ll depend on the project’s complexity.

Create base abstract shape class only when you have duplicated code in several IShape implementors, e.g., `Rectangle` and `Square` shapes would fall into that scenario.

When you create an abstract class (place where you move duplicated code), you shouldn’t change interface, because contract stays the same. Just inherit your base class from the original IShape interface.

## Conclusion

We reviewed the Open/Closed Principle with some basic examples and different ways to solve the problem. The one you pick will depend on your business case.

Also, you may have noticed we also use the Dependency Inversion Principle (the “D” of S.O.L.I.D) and the Single Responsibility Principle (the “S” of S.O.L.I.D). Often, several principles will go together and today’s article highlights that fact.

But, remember, like a Tech Lead once said to me:

> Think about the “What” first to pick the appropriate “How” afterwards.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Athena Sandrini](https://www.pexels.com/photo/metal-lock-on-deck-of-boat-6782753/).
