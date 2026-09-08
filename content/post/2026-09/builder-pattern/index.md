---
title: "Builder Pattern in 2 Flavors"
description: "You understand patterns by using them and then you see what one style bring over another."
image: 2026-09-07-childrens-hands-play-with-colorful-toy-blocks-on-a-table.jpg
imageAlt: Children’s hands play with colorful toy blocks on a table inside a room in East Java, Indonesia.
date: 2026-09-07
categories:
  - Software Development
tags:
  - Design Patterns
---

**Description:**

I used to think I knew what the Builder Pattern was and how to use it. I’ve learned that there is a different flavor.

**Content:**

On a project last year, I came across some code that did use the builder pattern.

I didn’t understand the implementation and a more senior colleague explained to me the ins and outs.

Then I shared with him what I understood about the topic from my experience.

## My Experience Wasn’t the Builder Pattern

It was the Assembler Pattern. Here is the idea with an example:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Builder.In.One.Flavour
{
      internal class Program
      {
            internal static void Main(string[] args)
            {
                  var productId = 2;
                  var tariff = new LibraryTariffs().GetTariffs().FirstOrDefault(element => element.id == productId);
                  var label = new ApiProductLabels().GetLabels().FirstOrDefault(element => element.id == productId);
                  var builder = new Builder(productId)
                        .BuildPart(tariff)
                        .BuildPart(label);
                  Console.WriteLine(builder.Item.ToString());
            }
            internal class LibraryTariffs
            {
                  internal LibraryTariffs() { }
                  internal List<(int id, decimal price)> GetTariffs() =>
                        new List<(int id, decimal price)>()
                        {
                        (id: 1, price: 1000m ),
                        (id: 2, price: 1.99m ),
                        (id: 3, price: 10m ),
                        (id: 4, price: 100m ),
                        };
            }
            internal class ApiProductLabels
            {
                  internal ApiProductLabels() { }
                  internal List<(int id, string name, string desc)> GetLabels() =>
                        new List<(int id, string name, string desc)>()
                        {
                        (id: 1, name: "Gold bar", desc: "You wish you had one..."),
                        (id : 2, name : "Banana", desc: "Miam"),
                        (id: 3, name: "Netflix Sub", desc: "Do you really need it?!" ),
                        (id : 4, name : "Basic Smartphone", desc : "It is cheap but it works"),
                        };
            }
            internal class Item
            {
                  public Item(int productId) => Id = productId;

                  public int Id { get; }
                  public string Name { get; set; }
                  public string Description { get; set; }
                  public decimal Price { get; set; }
            }

            internal class Builder
            {
                  internal Item Item { get; }

                  internal Builder(int productId) => Item = new Item(productId);

                  internal Builder BuildPart((int productId, decimal productPrice) productTariff)
                  {
                        Item.Price = productTariff.productPrice;
                        return this;
                  }
                  internal Builder BuildPart((int productId, string name, string description) productLabels)
                  {
                        Item.Name = productLabels.name;
                        Item.Description = productLabels.description;
                        return this;
                  }
            }
      }
}
```

Yes, that smells like a _god object_ but that was what we could do to build the item object with the resource (mainly time and budget) that the project granted us.

### Improvements

1. Yes, we can add better error handling: the code above will throw `NullReferenceException` if `tariff` or `label` aren’t found:

   ```csharp
   var builder = new Builder(productId)
                   .BuildPart(tariff) // Could be null!
                   .BuildPart(label); // Could be null!
   ```

2. Yes, the method of naming having multiple `BuildPart` methods with different signatures works but isn’t expressive. We could consider: `WithPricing(...)` and `WithLabels(...)`
3. Yes, we can improve immutability. The `Item` class has a read-only `Id` but leaves other properties mutable. We could make the class properties fully immutable for thread safety and clearer intent.

## Using Fluent Builder Pattern Instead

On the project from last year, we had the following, and it lived almost entirely in the unit tests.

I assumed that I could use it in the business logic too, but a senior colleague challenged the idea: the fluent builder earns its keep in tests, where you build the same object over and over with tiny variations. Production code usually already has a constructor, a factory, or a mapper doing that job.

Let’s imagine a `CartItemBuilder`:

```csharp
using System;
using System.Collections.Generic;
using Bogus;

namespace Builder.In.Another.Flavour.Tests.Helper
{
      internal class Item
      {
            internal int Id { get; set; }
            internal string Name { get; set; }
            internal string Description { get; set; }
            internal decimal Price { get; set; }
      }

      internal class CartItemBuilder
      {
            private static readonly Faker Faker = new Faker();

            private int _quantity = 0;
            private int _id = Faker.Random.Int(1, 9999);
            private string _name = "";
            private string _desc = "";
            private decimal _price = 0m;

            // The action delegate allows to simplify the fluent method
            private CartItemBuilder Do(Action<CartItemBuilder> action)
            {
                  action(this);
                  return this;
            }

            private CartItemBuilder() { }

            // You could build an item at once, though it will be unique to the Gold bar item
            internal static CartItemBuilder AGoldBar() => new CartItemBuilder()
                  .Do(x =>
                  {
                        x._id = 1;
                        x._name = "Gold bar";
                        x._desc = "You wish you had one...";
                        x._price = 1_000.00m;
                  });

            // You can otherwise initialize the object
            internal static CartItemBuilder ACartItem() => new CartItemBuilder();

            // And then fluently set the properties one by one
            internal CartItemBuilder WithId(int id) =>
                Do(x => x._id = id);

            internal CartItemBuilder WithPrice(decimal price) =>
                Do(x => x._price = price);

            internal CartItemBuilder WithQuantity(int quantity) =>
                  Do(x => x._quantity = quantity);

            // Or related properties together
            internal CartItemBuilder WithLabels(string name, string desc) => Do(x =>
                  {
                        x._name = name;
                        x._desc = desc;
                  });

            internal AddProductToCartCommand Build() =>
                  new AddProductToCartCommand(
                        quantity: _quantity,
                        item: new Item
                        {
                              Id = _id,
                              Name = _name,
                              Description = _desc,
                              Price = _price,
                        });
      }
}
```

This pattern is called a fluent interface but we’ll find names like method chaining pattern or self-chaining builder method. The `Do` method executes an action on the current `CartItemBuilder` instance and then returns that same instance, enabling the fluent syntax.

Let’s continue the example with the following cart business logic:

```csharp
      internal class CartItem
      {
            public CartItem(Item item, int quantity)
            {
                  Item = item;
                  Quantity = quantity;
            }

            internal int Quantity { get; }
            internal Item Item { get; }
      }

      internal class Cart
      {
            public List<CartItem> CartItems { get; }
            public Cart() => CartItems = new List<CartItem>();
            public void AddToCart(AddProductToCartCommand command)
                  => CartItems.Add(command.ToCartItem());
      }
      
      internal static class AddProductToCartCommandExtensions
      {
            internal static CartItem ToCartItem(this AddProductToCartCommand command)
                  => new CartItem(command.Item, command.Quantity);
      }

      internal class AddProductToCartCommand
      {
            internal AddProductToCartCommand(int quantity, Item item)
            {
                  Quantity = quantity;
                  Item = item;
            }

            internal int Quantity { get; }
            internal Item Item { get; }
      }

```

And now, let’s use it — in the unit tests, where it belongs. Each test builds only the part of the cart item it actually cares about; every other field falls back to the builder’s defaults, so the noise stays out of the test body:

```csharp
using System.Linq;
using Xunit;
using Builder.In.Another.Flavour.Tests.Helpers;

namespace Builder.In.Another.Flavour.Tests
{
    public class CartShould
    {
        [Fact]
        public void AddGoldBarToCartWithAQuantity()
        {
            var cart = new Cart();
            var addGoldBars = CartItemBuilder
                .AGoldBar()
                .WithQuantity(10)
                .Build();

            cart.AddToCart(addGoldBars);

            var line = Assert.Single(cart.CartItems);
            Assert.Equal(10, line.Quantity);
            Assert.Equal("Gold bar", line.Item.Name);
            Assert.Equal(1_000.00m, line.Item.Price);
        }

        [Fact]
        public void AddBothItemToCart()
        {
            var cart = new Cart();

            cart.AddToCart(CartItemBuilder.AGoldBar().WithQuantity(1).Build());
            cart.AddToCart(CartItemBuilder
                .ACartItem()
                .WithId(2) // Can be randomized
                .WithLabels("Banana", "A ripe one") // Can be randomized
                .WithPrice(1.99m)
                .WithQuantity(5)
                .Build());

            Assert.Equal(2, cart.CartItems.Count);
            Assert.Equal(6, cart.CartItems.Sum(line => line.Quantity));
        }
    }
}
```

Some developers also refer to this specific technique as:

- Tap pattern—borrowed from functional programming (similar to Ruby’s tap method)
- Side-effect chaining—since it executes a side effect and returns the object
- Action chaining—since it accepts an Action delegate

## Why Builders Live in the Test Suite

When my colleague explained why the fluent builder belongs in the tests, he pointed me at a short page by Kent Beck: [Test Desiderata](https://kentbeck.github.io/TestDesiderata/). It lists twelve properties a test should have. You can rarely maximize all of them at once, but applying most of them makes good tests. A few are worth calling out here:

- **Readable** — a reader should see at a glance why the test exists. `CartItemBuilder.ACartItem().WithPrice(1.99m).WithQuantity(5)` states the two values under test and hides the rest.
- **Writable** — tests should be cheap to write compared with the code they cover. Assembling a valid `AddProductToCartCommand` by hand in every test is friction; `ACartItem()` removes it.
- **Structure-insensitive** — a test shouldn’t break when the shape of the code changes but its behavior doesn’t. Add a field to `Item` and you fix one default in the builder, not fifty `new Item { ... }` literals.
- **Fast** and **Deterministic** — the builder does a plain in-memory assignment, so nothing here reaches for a clock, a database, or the network.

It also reframes something I used to get wrong: chasing every possible input value. A useful test checks that a piece of your domain behaves as you expect, with a few representative cases — not the full cartesian product of every field. The builder keeps those few cases short enough that the intent stays visible.

## Conclusion

The fluent builder remains useful—often in the tests, where arranging objects with minimal ceremony becomes the job.

This pattern comes in particularly useful when you want to conditionally apply multiple scenarios or perform complex setup logic while maintaining the fluent builder pattern.

It’s a way to make the builder more flexible without having to define a separate method for every possible configuration combination.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by sofamuzaqi (`https://www.pexels.com/photo/children-building-with-colorful-blocks-indoors-38781113/`).
