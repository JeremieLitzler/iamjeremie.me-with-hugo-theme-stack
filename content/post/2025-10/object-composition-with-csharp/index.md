---
title: "Object composition with C#"
description: "Object composition is a design principle in which one class is composed of one or more objects of other classes."
image: 2025-10-27-a-building-with-orange-and-blue-parts.jpg
imageAlt: A building with orange and blue parts
date: 2025-10-27
categories:
  - Software Development
tags:
  - Design Patterns
  - Csharp
---

It allows modularity in a class design and make it reusable, promoting the “has-a” relationship rather than an “is-a” relationship that inheritance implies.

Here’s a simple example of object composition in C#:

```csharp
using System;

namespace ObjectCompositionExample
{
    // Engine class
    public class Engine
    {
        public void Start()
        {
            Console.WriteLine("Engine started.");
        }

        public void Stop()
        {
            Console.WriteLine("Engine stopped.");
        }
    }

    // Radio class
    public class Radio
    {
        public void TurnOn()
        {
            Console.WriteLine("Radio is on.");
        }

        public void TurnOff()
        {
            Console.WriteLine("Radio is off.");
        }
    }

    // Car class that is composed of Engine and Radio
    public class Car
    {
        private Engine _engine;
        private Radio _radio;

        public Car()
        {
            // Engine and Radio start to exist only
            //  when the Car is created
            _engine = new Engine();
            _radio = new Radio();
        }

        public void Start()
        {
            _engine.Start();
            _radio.TurnOn();
            Console.WriteLine("Car started.");
        }

        public void Stop()
        {
            _radio.TurnOff();
            _engine.Stop();
            Console.WriteLine("Car stopped.");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Car myCar = new Car();
            myCar.Start();
            myCar.Stop();
        }
    }
}

```

**`Engine` Class** represents the engine of a car. It has methods to start and stop the engine.
**Radio Class** represents the radio in a car. It has methods to turn on and turn off the radio.
**Car Class** represents a car and uses composition to include a `Engine` and a `Radio`. It has methods to start and stop the car, which internally starts/stops the engine and turns on/off the radio.

In this example, the `Car` class is composed of `Engine` and `Radio` objects, demonstrating how object composition allows a class to use the functionality of other classes to perform its duties. This approach provides flexibility and promotes code reuse.

## Alternative with Loose Coupling of `Car` from `Engine` and `Radio`

The previous is OK, but best practices recommend this tight coupling between the classes `Car`, `Engine` and `Radio`

To achieve loose coupling, we can use interfaces to define the behavior expected from the `Engine` and `Radio` classes.

This way, the `Car` class doesn’t depend on the concrete implementations of `Engine` and `Radio` classes but rather on their interfaces. This promotes loose coupling and makes the system more flexible and easier to extend, modify or test.

Here is an example using interfaces for loose coupling:

```csharp
using System;

namespace LooseCouplingExample
{
    // Engine interface
    public interface IEngine
    {
        void Start();
        void Stop();
    }

    // Radio interface
    public interface IRadio
    {
        void TurnOn();
        void TurnOff();
    }

    // Concrete implementation of IEngine
    public class Engine : IEngine
    {
        public void Start()
        {
            Console.WriteLine("Engine started.");
        }

        public void Stop()
        {
            Console.WriteLine("Engine stopped.");
        }
    }

    // Concrete implementation of IRadio
    public class Radio : IRadio
    {
        public void TurnOn()
        {
            Console.WriteLine("Radio is on.");
        }

        public void TurnOff()
        {
            Console.WriteLine("Radio is off.");
        }
    }

    // Car class that uses IEngine and IRadio
    public class Car
    {
        private readonly IEngine _engine;
        private readonly IRadio _radio;

        // This is also called dependency injection
        public Car(IEngine engine, IRadio radio)
        {
            _engine = engine;
            _radio = radio;
        }

        public void Start()
        {
            _engine.Start();
            _radio.TurnOn();
            Console.WriteLine("Car started.");
        }

        public void Stop()
        {
            _radio.TurnOff();
            _engine.Stop();
            Console.WriteLine("Car stopped.");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            IEngine engine = new Engine();
            IRadio radio = new Radio();

            Car myCar = new Car(engine, radio);
            myCar.Start();
            myCar.Stop();
        }
    }
}

```

**Interfaces `IEngine` and `IRadio`** define the behavior that the `Engine` and `Radio` classes must implement. This ensures that the `Car` class interacts with these interfaces, not the concrete implementations.

**Concrete Implementations of `Engine` and `Radio`** implement the `IEngine` and `IRadio` interfaces. They provide the actual behavior for starting/stopping the engine and turning on/off the radio.

**Car Class** uses `IEngine` and `IRadio` interfaces instead of the concrete `Engine` and `Radio` classes, consequently decoupling the `Car` class from specific implementations and allows for any implementation of `IEngine` and `IRadio` to be used.

In the **Program Class**, we now create instances of `Engine` and `Radio`, pass them to the `Car` constructor, and start/stop the car.

The output remains the same, but the code has become much more scalable. For example, you could create mock implementations for testing purposes or swap in different engines or radio types as needed.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Nothing Ahead](https://www.pexels.com/photo/modern-architectural-abstract-with-shadows-34434121/).
