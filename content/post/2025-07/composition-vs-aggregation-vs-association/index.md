---
title: "Composition vs Aggregation vs Association"
description: "Let’s dive into the three object-oriented programming concepts.."
image: 2025-07-14-a-notebook-with-wireframes.jpg
imageAlt: A notebook with wireframes
date: 2025-07-14
categories:
  - Software Development
tags:
  - Design Patterns
---

These concepts describe relationships between objects in a class hierarchy.

We’ll break them down one by one below.

### Association

_Association_ represents a “uses-a” or “has-a” relationship between two separate classes where one class uses the other. It defines a relationship between objects where one object can access another.

For example, in C#:

```csharp
public class Driver
{
    public string Name { get; set; }
}

public class Car
{
    public string Model { get; set; }
    public Driver Driver { get; set; }  // Association with Driver class
}

public class Program
{
    public static void Main()
    {
        Driver driver = new Driver { Name = "John" };
        Car car = new Car { Model = "Toyota", Driver = driver };

        Console.WriteLine($"{car.Driver.Name} drives a {car.Model}");
    }
}
```

### Aggregation

_Aggregation_ is a specialized form of _Association_ with a “whole-part” relationship, but the lifetimes of the parts are independent of the whole. In other words, the part can exist without the whole.

For example

```csharp
public class Department
{
    public string Name { get; set; }
}

public class Company
{
    public string Name { get; set; }
    public List<Department> Departments { get; set; } = new List<Department>(); // Aggregation

    public void AddDepartment(Department department)
    {
        Departments.Add(department);
    }
}

public class Program
{
    public static void Main()
    {
        Department d1 = new Department { Name = "HR" };
        Department d2 = new Department { Name = "Finance" };

        Company company = new Company { Name = "TechCorp" };
        company.AddDepartment(d1);
        company.AddDepartment(d2);

        Console.WriteLine($"{company.Name} has the following departments:");
        foreach (var dept in company.Departments)
        {
            Console.WriteLine(dept.Name);
        }
    }
}

```

### Composition

_Composition_ is a stronger form of _Aggregation_ with a “part-whole” relationship where the part can’t exist without the whole. If the whole is destroyed, the parts are also destroyed.

**Example:**

```csharp
public class Engine
{
    public string Model { get; set; }

    public Engine(string model)
    {
        Model = model;
    }
}

public class Car
{
    public string Model { get; set; }
    public Engine Engine { get; set; } // Composition

    public Car(string model, string engineModel)
    {
        Model = model;
        Engine = new Engine(engineModel);
    }
}

public class Program
{
    public static void Main()
    {
        Car car = new Car("Toyota", "V8 Engine");

        Console.WriteLine($"Car model: {car.Model}, Engine model: {car.Engine.Model}");
    }
}

```

### Summary

- **_Association_** represents a general relationship where one class uses another. There is no ownership implied. In the example: a `Car`has a `Driver`.
- **_Aggregation_** defines a specialized form of _Association_ with a “whole-part” relationship where the part can exist independently of the whole. In the example, a `Company`has `Departments`, but `Departments`can exist without the `Company`.
- **_Composition_** describes a strong form of _Aggregation_ where the part cannot exist independently of the whole. If the whole is destroyed, the parts are also destroyed. In the example, a `Car`has an `Engine`and that `Engine`cannot exist independently of the `Car`.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [picjumbo.com](https://www.pexels.com/photo/notebook-beside-the-iphone-on-table-196644/).
