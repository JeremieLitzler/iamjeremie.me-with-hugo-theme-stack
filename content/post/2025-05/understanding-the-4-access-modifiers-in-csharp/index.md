---
title: "Understanding the 4 Access Modifiers in C#"
description: "Do you know them? What would you use one over another? Let’s look at it in detail."
image: 2025-05-09-a-private-sign.jpg
imageAlt: A sign post with the word "Private"
date: 2025-05-09
categories:
  - Software Development
tags:
  - Csharp
---

In C#, accessors define the visibility and accessibility of members (fields, properties, methods, etc.) within a class or struct. The main accessors in C# are `private`, `public`, and `protected`. Here’s a detailed explanation of each.

## What Are The Accessors

### Private Accessor

The members declared with the `private`accessor are accessible only within the same class or struct.

You can use `private`to encapsulate data and restrict its access from outside the class. It helps to maintain control over the data and ensures that you can’t modify or access it directly from other parts of the code.

In the example below, the `name`field is private and can only be accessed or modified through the `SetName`and `GetName`methods.

The convention is also to prefix the field with `_`.

```csharp
class Person
{
    private string _name;

    public void SetName(string name)
    {
        this._name = name;
    }

    public string GetName()
    {
        return this._name;
    }
}

```

### Public Accessor

The members declared with the `public`accessor are accessible from any other code. There are no restrictions on their accessibility.

You use `public`when you want to expose members to be accessible from outside the class or struct, such as in a library or API where you need to provide access to certain functionality.

In the example below, the `Name`property is public and can be accessed and modified directly from outside the `Person`class.

```csharp
namespace Some.Library;

public class Person
{
    public string Name { get; set; }
    public Person() {}
}

using Some.Library;
namespace Some.Project.Using.The.Library;
class Polite {
    void Greet()
    {
        var person = new Person()
        person.Name = "Jeremie";
        Console.WriteLine($"Hello, my name is {person.Name}.");
    }
}
```

### Protected Accessor

The members declared with the `protected`accessor are accessible within the same class or struct, and in derived classes (subclasses).

You use `protected`when you want to allow access to members in the base class and any derived classes but restrict access from other parts of the code.

In the example below, the `species`field is protected and can be accessed in the `Animal`class and the `Dog`class, which is derived from `Animal`.

```csharp
class Animal
{
    protected string species;

    public void SetSpecies(string species)
    {
        this.species = species;
    }
}

class Dog : Animal
{
    public void DisplaySpecies()
    {
        Console.WriteLine($"This dog belongs to the species: {species}");
    }
}
```

### Additional Access Modifiers

C# also provides other access modifiers like `internal`and `protected internal`:

`internal` makes members accessible within the same assembly, but not from another assembly.

```csharp
internal class InternalClass
{
    internal int InternalProperty { get; set; }
}

```

`protected internal` makes members accessible within the same assembly and a related class in the assembly.

```csharp
protected internal class ProtectedInternalClass
{
    protected internal int ProtectedInternalProperty { get; set; }
}

```

## What about the implicit access modifiers in the class

You may wonder in the examples above what happens when you don't specify the access identifier on the class, method or property.

The access modifier of a class itself is important and can affect how the class is accessed. In C#, if a class doesn’t specify an explicit access modifier, it defaults to `internal`.

## Important Notes

- **For Top-Level Classes**: In C#, top-level classes (i.e., those that aren’t nested within another class) can only have `public`or `internal`access modifiers. They can’t be `private`or `protected`.
- **For Nested Classes**: When a class is nested within another class, it can have any access modifier (`public`, `private`, `protected`, `internal`, `protected internal`).

### Example with Nested Classes

```csharp
public class OuterClass
{
    private class InnerPrivateClass
    {
        // Accessible only within OuterClass
    }

    protected class InnerProtectedClass
    {
        // Accessible within OuterClass and derived classes
    }

    internal class InnerInternalClass
    {
        // Accessible within the same assembly
    }

    public class InnerPublicClass
    {
        // Accessible from any other assembly
    }
}

```

In this example:

- `InnerPrivateClass`is accessible only within `OuterClass`.
- `InnerProtectedClass`is accessible within `OuterClass`and derived classes.
- `InnerInternalClass`is accessible within the same assembly.
- `InnerPublicClass`is accessible from any assembly.

## Conclusion

Understanding and using class access modifiers correctly helps in designing your code’s architecture, controlling access levels, and ensuring proper encapsulation and security.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Tim Mossholder](https://www.pexels.com/photo/black-and-white-wooden-sign-behind-white-concrete-3690735/)
