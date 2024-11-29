---
title: "Entity Framework, Repository Pattern and Factory Pattern"
description: "What is Entity Framework and how is it related to the Repository and Factory Patterns: Let’s dive in!"
image: images/2024-11-29-ladder-leaning-on-bookshelf.jpg
imageAlt: Wood ladder leaning on bookshelf
date: 2024-11-29
categories:
  - Web Development
tags:
  - Entity Framework
  - Design Patterns
---

Entity Framework (or EF in short) in C# applications often uses similar principles to the Factory Design Pattern, but it isn’t a direct implementation of the pattern. Instead, we consider EF a good example of Repository Pattern implementation.

EF focuses on Object-Relational Mapping (ORM) to interact with databases, and it abstracts the creation and management of data context and entities, which can be seen as leveraging some factory-like behavior.

## What is the Factory Pattern in Brief

Think of a pizza restaurant with multiple pizza-making stations.

Each station (Concrete Factory) follows a general pizza-making process (Abstract Factory) but can create different types of pizzas.

Whether it’s a Margherita, Pepperoni, or Vegetarian, the basic process remains the same, but the specific ingredients and preparation vary.

The Factory Pattern works very similarly in software design.

It’s a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

Try to think about places in your own code where you might need a flexible object creation process. Where do you see repetitive creation patterns that could benefit from a more abstract approach?

## What is the Repository Pattern in Brief

Think of the Repository Pattern like a library system:

- You (client) request a book
- The librarian (repository) knows exactly where to find it
- You don’t need to know the library’s internal organization
- The librarian handles all the complex retrieval mechanisms

This approach ensures that your application’s core logic remains clean, flexible, and independent of specific data storage implementations.

The Repository Pattern functions like a librarian, abstracting complex data access details. It provides a clean, collection-like interface for:

- Retrieving data
- Adding new entities
- Updating existing entities
- Deleting entities

The benefits are that it:

- Decouples business logic from data access
- Centralizes data access logic
- Simplifies testing and maintenance
- Enables easy switching of data storage technologies

## How Entity Framework Relates to the Factory Pattern While Using the Repository Pattern Heavily

We can consider the _DbContext_ as a Factory that creates instances of entity objects when querying the database. When you perform a query, `DbContext` generates the entities that match the query conditions.

However, EF is used in conjunction with the Repository Pattern, which can encapsulate the creation and access logic, making it resemble the Factory Pattern.

## Usage

### Example of EF

Here’s an example demonstrating how Entity Framework might use similar principles to the Factory Pattern in a C# application.

First we need an _Entity Class_:

```csharp
public class Book
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Isbn { get; set; }
}

```

And a `DbContext Class`:

```csharp
using Microsoft.EntityFrameworkCore;

public class BookContext : DbContext
{
    public DbSet<Book> Books { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer("YourConnectionStringHere");
    }
}

```

Next we define the `IRepository Interface` that all concrete repository class will use:

```csharp
public interface IRepository<T> where T : class
{
    IEnumerable<T> GetAll();
    T GetById(int id);
    void Add(T entity);
    void Delete(T entity);
    void Save();
}

```

For example, the following `BookRepository Class` implements

```csharp
public class BookRepository : IRepository<Book>
{
    private readonly BookContext _context;

    public BookRepository(BookContext context)
    {
        _context = context;
    }

    public IEnumerable<Book> GetAll()
    {
        return _context.Books.ToList();
    }

    public Book GetById(int id)
    {
        return _context.Books.Find(id);
    }

    public void Add(Book entity)
    {
        _context.Books.Add(entity);
    }

    public void Delete(Book entity)
    {
        _context.Books.Remove(entity);
    }

    public void Save()
    {
        _context.SaveChanges();
    }
}

```

### Using the Repository in Client Code

In the client code, you could have this usage:

```csharp
class Program
{
    static void Main()
    {
        using (var context = new BookContext())
        {
            var library = new BookRepository(context);

            // Add a new Book
            var book1 = new Book { Name = "The Handbook of Science and Technology Studies", Isbn = "9780262035682" };
            var book2 = new Book { Name = "Technology Trends for 2024", Isbn = "9781098167950" };
            var book3 = new Book { Name = "Modern Operating Systems", Isbn = "9780137618842" };
            library.Add(book1);
            library.Add(book2);
            library.Add(book3);
            library.Save();

            // Get all products
            var books = library.GetAll();
            foreach (var book in books)
            {
                Console.WriteLine($"Book ID: {book.Id}, Name: {book.Name}, ISBN: {book.Isbn}");
            }
        }
    }
}
```

In the example, there are some factory-like elements:

### DbContext as a Factory

The `BookContext` class serves a factory-like role by:

- Creating Database Connections: Configures database access through `OnConfiguring()` method.
- Managing Entity Sets: Provides `DbSet<T>` properties that allow tracking and querying entities
- Abstracting Database Interaction: Encapsulates the complexity of database operations

### Repository as a Factory Variant

The `IRepository<T>` interface and `BookRepository` class demonstrate the Repository pattern, which shares similarities with the Factory pattern:

- Abstraction: Provides a standardized interface for data access operations
- Decoupling: Separates data access logic from business logic
- Flexibility: Allows easy switching of data sources or ORM implementations

### Factory-Like Characteristics

There are the following:

- Object Creation: the `BookRepository` creates and manages `Book` entity instances. It also provides methods like `Add()`, `GetById()`, and so on that abstract object creation and retrieval.
- Dependency Injection: the repository accepts a `DbContext` in its constructor, enabling flexible configuration. It also supports loose coupling between data access and business logic.
- Abstraction: the `IRepository<T>` interface defines a contract for data access methods. Concrete implementations can vary without affecting client code.

## Summary

While Entity Framework itself isn’t a direct implementation of the Factory Pattern, it does utilize similar principles by abstracting the creation and management of entities and their context.

The Repository Pattern, often used alongside EF, encapsulates data access logic and can further promote factory-like behavior, helping manage object creation and interaction with the database.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Jean Vella](https://unsplash.com/@jean_vella?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/a-ladder-leaning-against-a-bookshelf-filled-with-books-wuQ-2WLVJuo?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
