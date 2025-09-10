---
title: "The Design Patterns And Software Architectures I’ve encountered"
description: "While it is a vast topic that authors have described in many books and articles, I’d like to review what design patterns and architectures I’ve encountered in my career so far."
image: 2025-08-04-architecte-building-with-triangle-shapes.jpg
imageAlt: Architecte building with triangles shapes
date: 2025-08-04
categories:
  - Software Development
tags:
  - Design Patterns
---

Before I start, let’s define software architectures and design patterns.

Software architectures represent high-level structure, components, and their relationships that guide the design of software systems.

Design patterns represent reusable solutions to common problems encountered when designing and developing large-scale software systems for businesses. Patterns help architects and developers create robust, scalable, and maintainable applications.

Let’s review what I’ve encountered so far.

## The Architectures

Here’s a concise overview of some key architectures I came across, often not knowing their name until much later:

### Layered Architecture

This is the most common architecture. It divides the application into distinct layers (e.g., presentation, business logic, data access) to improve modularity and separation of concerns.

However, layered applications don’t mean decoupled layers. You can have a data layer coupled with the business layer and the web layer coupled with the business layer. Though it isn’t what we should go for.

And tight coupling means difficulty to test, especially on many legacy solutions I’ve worked on.

### Model-View-Controller (MVC)

Surely, you know that one. It’s a very popular pattern that separates an application into three interconnected layers for better code organization and reusability.

The Model layer represents your entity definitions. For example, if your application models a car, the models would be a car, an engine, a wheel, a suspension, etc.

The View layer is the representation of the car, how it looks.

Finally, the Controller layer connects the Model to the View with the business logic to make your car run and become “drivable”.

### Microservices

In recent years, this pattern has received a lot of hype. It decomposes a system into small, independent services that can be developed, deployed, and scaled separately.

It is, however, important to break down your system into the proper number of pieces, e.g., microservices, so it stays manageable and easy to use. In other words, finding the best compromise between a monolithic and too many microservices is the challenge.

I can say that is similar to event-driven architecture because microservices talks to each other through a bus of messages (e.g., events).

### Clean Architecture

I came across this architecture last April as I was preparing my interviews for a new job.

I went ahead and followed a small course on the topic that encourages using [Ardalis’s template](https://github.com/ardalis/CleanArchitecture) which I liked straight away.

As a succinct summary, the clean architecture in an onion-layered architecture where all layers are decoupled from each other, allowing easier testing of each layer.

The layers come as follows:

- in the center, the _Domain_ layer where your entities live.
- the next outer layer contains the _Use Cases_ which is the business logic.
- the next outer layer contains the _Infrastructure_ to access the data layer with EF Core or any external API like emailing, logging and so on.
- the top layer contains the _Web_ part, which in the case of an API would be the Web API, controllers, etc.

It uses the [Mediator](#mediator) pattern heavily and though it’s built to be future proof, it requires to understand the abstractions in place to understand the communication between layers.

It’s the architecture that I’m very likely to use going forward.

Please [check out all the decisions made by Ardalis](https://github.com/ardalis/CleanArchitecture/tree/main/docs/architecture-decisions) to craft the above template as he did.

## The Design Patterns

### Repository

It abstracts the data access layer, providing a more object-oriented view of the persistence layer.

Through DTO classes, you create a communication layer between the business and the data layers.

The goal is that the business doesn’t know about the data layer details and therefore is loosely coupled to it.

This makes testing the business logic easier.

### Command Query Responsibility Segregation (CQRS)

This one has come into my radar in the last couple of years and I finally came to work with it on a mission since last month.

It gained a lot of popularity in the last 5 years, though the pattern was defined a long time ago as Bertrand Meyer coined the concept in 2985. Martin Flowler details this [in his article](https://martinfowler.com/bliki/CommandQuerySeparation.html) on the topic.

It separates read and write operations for the better separation of concerns, performance and scalability.

Some use a single relational database, whereas others use a No-SQL database for the read operations and a relational database to write operations. However, this implies that you put in place a synchronization from the writable database to the readable database and that can add a significant complexity to your system.

To me, the separation of concerns is the feature that brings the most value.

### Singleton

This is a creational pattern to persist only one instance during the lifetime of the application.

We often use it for logging and caching functionalities that needs to exist as long as the application runs.

### Prototype

It’s also a creational pattern but through cloning objects instead of creating them from constructors.

### Factory Method

I wrote about this pattern. Again, we’re dealing with creational pattern that, through inheritance, but more often an interface, allow us to create objects.

### Strategy

You want to avoid `if…else` chaos through a common interface that is implemented by classes following the Single Responsibility principle? You have a match!

For example, I had a global exception handler in .NET 4.8 to build. Using a reflective registry (one exception = one exception problem details builder), I was able to code a exception handler to catch all exceptions and handle them in a single manner per exception, implementing the [Problem Details RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html).

### Chain of responsibility

I used it in the middlewares in .NET Core or .NET Framework with OWIN package.

Basically, the concept is that the chain of middlewares is like a Russian doll where the top middleware passes the request to the next middleware in the pipeline to handle it.

In short, each handler in the pipeline has a chance to process the request or pass it to the next.

### Adapter

I’ve used it to make two incompatible interfaces work together.

For example, transferring data from a C or C++ library with a C# wrapper to the REST API uses an adapter.

### Mediator

In the CQRS pattern, Mediator handles the request to retrieve the result based on a query or command by dispatching the event to the target handler.

The latter executes the business logic and then returns a result.

In .NET, it looks like this:

```csharp
// I am deliberately omitting the using statements, as they are not important in this code snippet.

public MyAwesomeQuery : IRequest<MyAwesomeResult> {
  // You define your input data here and the constructor
  // that the controller calls.
}

public MyAwesomeResult {
  // You define your output data.
}

public MyAwesomeQueryHandler : IRequestHandler<MyAwesomeQuery, MyAwesomeResult> {
  public Task<MyAwesomeResult> Handle(MyAwesomeQuery request, CancellationToken cancellationToken) {
    // business logic goes here

    return Task.FromResult(new MyAwesomeResult());
  }
}
```

### Builder

The pattern helps separate the construction of a complex object from its representation.

I used at Conduent to build a ticketing product where the data sources were either API, library and binary files.

Using `BuildPart` methods having each a distinct signature, we were filling the object step-by-step.

Each `buildPart` returns the instance of the object being filled to enable method chaining and avoid, once more, `if…else` trees.

### More About Patterns

I recommend reading this series of articles from [Maxim Gorin](https://maxim-gorin.medium.com/list/design-patterns-b183b417384c). Maxim has done an amazing describing each pattern with a non-technical example and a technical example, providing for each pros and cons to use a pattern or not.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
