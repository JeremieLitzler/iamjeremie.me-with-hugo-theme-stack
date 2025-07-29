---
title: "How Are ‘virtual’, ‘partial’, ‘override’ Used in C#?"
description: "And what are they in the C# programming language. Let’s review that together."
image: 2025-07-28-a-sign-open-hanging-on-a-door.jpg
imageAlt: An “open” sign hanging on a wood door
date: 2025-07-28
categories:
  - Software Development
tags:
  - CSharp
  - DotNet
---

`virtual`, `partial`, `override` are keywords that provide each a specific functionality to classes, method or properties.

Let’s start with `partial`.

## `partial` Keyword

The `partial` keyword allows a class or struct to be split into multiple files, though I’ve mainly used it with classes. This can be useful for organizing code, especially in large projects or when working with code generators.

For example

- File 1: `Person.Part1.cs`

```csharp
public partial class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
}

```

- File 2: `Person.Part2.cs`

```csharp
public partial class Person
{
    public int Age { get; set; }

    public void PrintFullName()
    {
        Console.WriteLine($"{FirstName} {LastName}");
    }
}

```

In this example, the `Person` class is split into two parts. The compiler will combine these partial classes into one class at compile time.

In my experience, it’s a very useful feature when you want to refactor legacy code on which you can’t apply the _S.O.L.I.D._ principles right away. See that keyword has the gateway to _S.O.L.I.D._ principles by breaking down into smaller pieces your legacy code to reveal how you can refactor it into clean code.

## `virtual` Keyword

The `virtual` keyword is used to mark a method or property in a base class that can be overridden by derived classes. It allows derived classes to provide a specific implementation for the method or property.

For example:

```csharp
public class Animal
{
    public virtual void Speak()
    {
        Console.WriteLine("The animal makes a sound.");
    }
}

```

Here, the `Speak` method is marked as `virtual`, meaning it can be overridden in any class that inherits from `Animal`.

That leads us to the third keyword

## `override`Keyword

The `override` keyword is used to extend or modify the virtual/abstract method or property defined in a base class. When a method is marked with `override`, it provides a new implementation for a method inherited from a base class.

For example, taking our previous `Animal` class:

```csharp
public class Dog : Animal
{
    public override void Speak()
    {
        Console.WriteLine("The dog barks.");
    }
}

```

In this example, the `Dog` class overrides the `Speak` method of the `Animal` base class. When `Speak` is called on an instance of `Dog`, it will execute the overridden method in the `Dog` class.

## Combined Example

Let’s combine all three concepts in one example for better understanding.

```csharp
// File 1: Vehicle.Part1.cs
public partial class Vehicle
{
    public string Make { get; }
    public string Model { get; }
}

// File 2: Vehicle.Part2.cs
public partial class Vehicle
{
    public FuelType FuelType { get; }
    public Color Color { get; }
}

// Base class
public abstract class Vehicle
{
    public virtual int WheelCount { get; }

    public Vehicule (string make, string model, FuelType fuelType, Color color)
    {
        Make = make;
        Model = model;
        FuelType = fuelType;
        Color = color;
    }

    public virtual void DisplayInfo()
    {
        Console.WriteLine($"Make: {Make}, Model: {Model}");
    }
}

// Derived class
public class Car : Vehicle
{
    public override int { get { return 4; } }

    public Car(string make, string model, FuelType fuelType, Color color) : base(make, model, fuelType, color) {}

    public override void DisplayInfo()
    {
        Console.WriteLine($"Make: {Make}, Model: {Model}, Fuel: {FuelType}, Color: {Color}");
    }
}

// Usage
public class Program
{
    public static void Main()
    {
        Car myCar = new Car(make: "Toyota", model: "Yaris", fuelType: FuelType.Hybrid, color: Color.White);
        myCar.DisplayInfo(); // Output: Make: Toyota, Model: Yaris, Fuel:Hybrid, Color: White
    }
}

```

In this combined example:

- The `Vehicle` class is split into two partial files.
- The `Vehicle` class has a `virtual` method `DisplayInfo` and a `virtual` property `WheelCount`.
- The `Car` class inherits from `Vehicle` and
  - overrides the `DisplayInfo` method with the `override` keyword.
  - overrides the `WheelCount` property to set a value.

When `DisplayInfo` is called on an instance of `Car`, it uses the overridden method from the `Car` class.

## Caveats when using virtual and override

Using `virtual` and `override` in C# provides powerful mechanisms for creating flexible and extensible object-oriented designs. However, there are some caveats that can affect code maintainability and understanding, especially for new developers. Here are some potential issues:

### Complexity and Indirection

When using `virtual` and `override`, the actual implementation of a method might not be in the class where it’s called. This can make the code harder to follow, as developers need to understand the class hierarchy and locate the overridden methods.

In the `Animal` and `Dog` example, `myDog.Speak()` calls the overridden `Speak` method in `Dog`, not in `Animal`. Understanding this requires knowledge of both the base class and the derived class.

### Maintenance Overhead

As the hierarchy of classes grows, maintaining the code can become challenging. Changes in the base class can have unintended effects on derived classes. Developers must carefully consider the impact of modifying `virtual` methods.

### Hidden Behavior

Overridden methods can sometimes hide important behavior from the base class, leading to unexpected results or bugs that are hard to trace.

For example:

```csharp
using System;

// Base class with important validation logic
public class BankAccount
{
    protected decimal balance;

    public virtual void Withdraw(decimal amount)
    {
        // Critical validation logic
        if (amount > balance)
            throw new InvalidOperationException("Insufficient funds");

        Console.WriteLine($"Base: Validating withdrawal of ${amount}");
        balance -= amount;
        Console.WriteLine($"Base: New balance: ${balance}");
    }
}

// Derived class that overrides without calling base
public class PremiumAccount : BankAccount
{
    public override void Withdraw(decimal amount)
    {
        // CAVEAT: Overridden method completely bypasses base validation!
        Console.WriteLine($"Premium: Withdrawing ${amount} without validation");
        balance -= amount; // Direct access - no validation!
        Console.WriteLine($"Premium: New balance: ${balance}");
    }
}

// Better approach - calling base method
public class SafePremiumAccount : BankAccount
{
    public override void Withdraw(decimal amount)
    {
        // Calls base validation first
        base.Withdraw(amount);
        Console.WriteLine("Premium: Added premium processing");
    }
}

class Program
{
    static void Main()
    {
        Console.WriteLine("=== Dangerous Override (bypasses validation) ===");
        var dangerous = new PremiumAccount();
        dangerous.Withdraw(1000); // No validation - allows overdraft!

        Console.WriteLine("\n=== Safe Override (preserves validation) ===");
        var safe = new SafePremiumAccount();
        try
        {
            safe.Withdraw(1000); // Validation still occurs
        }
        catch (InvalidOperationException ex)
        {
            Console.WriteLine($"Caught: {ex.Message}");
        }
    }
}
```

In this example, the `PremiumAccount` class’s `Withdraw` method doesn’t call the base class’s `BankAccount` method, missing important behavior (e.g., validation logic) defined in the base class.

### Fragile Base Class Problem

The “fragile base class” problem occurs when changes to a base class break the functionality of derived classes. This can happen if derived classes rely on specific behaviors of base class methods that are modified.

### Increased Testing Efforts

Testing becomes more complex because you need to test both the base class and each derived class’s behavior. This is especially true if the `virtual` methods have complex logic.

### What Can You Do To Mitigate These Issues

First, clearly document the purpose and expected behavior of `virtual` methods and their overrides. This helps new developers understand the intended use.

Then, follow design principles like S.O.L.I.D. to create more maintainable and understandable code. For instance, the Liskov Substitution Principle (LSP) can guide you in ensuring that derived classes can replace base classes without causing issues.

Next, ensure that overridden methods call the base method, when necessary, to maintain expected behavior.

Also, use the `sealed` keyword on overrides to prevent further overriding in derived classes when appropriate.

Finally, avoid deep and complex class hierarchies where possible. Favor composition over inheritance if it makes the design simpler and more understandable.

## More About `sealed` Keyword And Composition

### The `sealed` Keyword

In C#, it’s used to prevent a class from being inherited or a method from being overridden further.

When applied to a class, it indicates that the class can’t serve as a base class.

When applied to a method that overrides a virtual method, it prevents further overriding of that method by derived classes.

```csharp
  public sealed class FinalClass
  {
      public void Display()
      {
          Console.WriteLine("This is a sealed class.");
      }
  }

  // The following will cause a compile-time error
  public class DerivedClass : FinalClass { }
```

- Sealed Method: in a derived class, it prevents further overriding of the method.

  ```csharp
  public class BaseClass
  {
      public virtual void Display()
      {
          Console.WriteLine("Base class display method.");
      }
  }

  public class DerivedClass : BaseClass
  {
      public sealed override void Display()
      {
          Console.WriteLine("Derived class display method.");
      }
  }

  // The following will cause a compile-time error
  public class SubDerivedClass : DerivedClass
  {
    public override void Display() { }
  }

  ```

### Composition

Composition is a design principle where a class is composed of one or more objects of other classes, rather than inheriting from them. It’s a “has-a” relationship as opposed to inheritance’s “is-a” relationship. Composition provides greater flexibility and promotes code reuse.

For example:

- Example 1: Simple Composition

  ```csharp
  public class Engine
  {
      public void Start()
      {
          Console.WriteLine("Engine started.");
      }
  }

  public class Car
  {
      private Engine _engine = new Engine();

      public void StartCar()
      {
          _engine.Start();
          Console.WriteLine("Car started.");
      }
  }

  public class Program
  {
      public static void Main()
      {
          Car myCar = new Car();
          myCar.StartCar(); // Output: Engine started. Car started.
      }
  }

  ```

In this example, the `Car` class uses an instance of the `Engine` class. The car “has an” engine, demonstrating composition.

- Example 2: Interface-Based Composition (or what you may know Dependency Injection, generally preferred to the example 1 code)

  ```csharp
  public interface IEngine
  {
      void Start();
  }

  public class ElectricEngine : IEngine
  {
      public void Start()
      {
          Console.WriteLine("Electric engine started.");
      }
  }

  public class GasolineEngine : IEngine
  {
      public void Start()
      {
          Console.WriteLine("Gasoline engine started.");
      }
  }

  public class Car
  {
      private IEngine _engine;

      public Car(IEngine engine)
      {
          _engine = engine;
      }

      public void StartCar()
      {
          _engine.Start();
          Console.WriteLine("Car started.");
      }
  }

  public class Program
  {
      public static void Main()
      {
          IEngine electricEngine = new ElectricEngine();
          Car myElectricCar = new Car(electricEngine);
          myElectricCar.StartCar(); // Output: Electric engine started. Car started.

          IEngine gasolineEngine = new GasolineEngine();
          Car myGasolineCar = new Car(gasolineEngine);
          myGasolineCar.StartCar(); // Output: Gasoline engine started. Car started.
      }
  }

  ```

In this example, the `Car` class is composed with an `IEngine` interface, allowing it to use different engine implementations. This demonstrates the flexibility of composition.

## Sources for This Article

You can read more on the topic with the following resources. What I shared here is only the tip of the iceberg and feel free dive deeper.

- **Microsoft Documentation**: The official documentation provides detailed explanations of C# keywords and design principles.
  - [`partial`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/partial)
  - [`virtual`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/virtual)
  - [`override`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/override)
  - [`sealed`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/sealed)
- **Design Patterns**: The book “Design Patterns: Elements of Reusable Object-Oriented Software” by Erich Gamma et al. provides insights into composition and other design principles.
- **SOLID Principles**: Various online resources and articles explain SOLID principles, such as the Liskov Substitution Principle, which relates to inheritance and composition.

These sources offer a comprehensive foundation for understanding the use of these keywords and design techniques in C#.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Đan Thy Nguyễn Mai](https://www.pexels.com/photo/open-sign-on-rustic-door-inviting-entry-33179717/)
