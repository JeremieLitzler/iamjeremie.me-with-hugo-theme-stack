---
title: "Calisthenic Programming - Wrapping Primitives"
description: "Also known as 'Primitive Obsession'."
image: 2026-11-16-a-sophisticated-gift-box-wrapped-with-a-brown-ribbon-on-a-rich-blue-surface.jpg
imageAlt: A sophisticated gift box wrapped with a brown ribbon on a rich blue surface.
date: 2026-11-16
categories:
  - Software Development
tags:
  - Object Calisthenics
---

Sometimes, a primitive, e.g., a string, a number, etc\., holds more meaning than you think. That’s when wrapping it becomes useful to isolate its logic.

Let’s see with an example I worked on earlier in the year in the banking sector.

## The Starting Point

The QA team found a bug: adding a beneficiary didn’t work when the end user would input the IBAN of a bank account that was internal the client’s bank. The current form at the time required the SWIFT code of the bank. However, the business logic filtered out the bank SWIFT code and the user couldn’t select it.

So, since the IBAN was internal, the discussed solution was to provide the frontend team an endpoint to tell them a string value\. Here, an IBAN was an internal IBAN value.

And, by the way, the database stored parameters defining the regular expression to identify if the string represented an internal IBAN.

## The Problem that Made Me Understand Primitive Obsession

I designed the code solution. I added the new endpoint with its query to check a string value was an internal IBAN value. Then I updated the business logic of the `AddBeneficiaryCommand` to check conditionally the SWIFT code provided.

If the IBAN was an internal IBAN, the SWIFT object was read directly from a SWIFT code constant (a bank’s SWIFT code doesn’t change once it is assigned). Otherwise, the command would check the SWIFT code provided by the frontend application.

While implementing the “Is the IBAN string an internal IBAN?”, I thought: “That’s repeating the same logic I did in the new query. And there’s this query listing beneficiaries where we use the logic as well. How can I extract the logic in common place?”

The constraint: the commands and queries were in separate projects (a decision made before I joined the project), so the common code couldn’t go into either project because we wanted to keep the segregation of commands from queries.

So, where should I put the common logic?

## Wrapping Primitive in an Object

The code calisthenic rules say, “encapsulate all the primitives within objects in order to avoid the Primitive Obsession anti-pattern.” (source: William Durant)

This is especially true when the primitive holds a **behavior**.

What’s the code solution in the current scenario?

First, create a class in the Domain project that both command and query projects reference:

```csharp
namespace My.Bank.Domain.IBANs
{
  public class Iban
  {
    public string Value { get; }

    public Iban(string value)
    {
      Value = value;
    }
  }
}
```

The string representing an IBAN is now an object and we can work on it:

Then, we enrich the class with the logic needed:

- add the using `using System.Text.RegularExpressions;` on top
- declare the readonly property `public bool IsInternal { get; }` to store the information “Is an internal IBAN”
- add the regular expression parameter as a `Regex` to the constructor
- assign `IsInternal` using the `Regex` object with `internalRegex.IsMatch(Value);`

The final code becomes:

```csharp
using System.Text.RegularExpressions;

namespace My.Bank.Domain.IBANs
{
  public class Iban
  {
    public string Value { get; }
    public bool IsInternal { get; }

    public Iban(string value, Regex internalRegex)
    {
      Value = value;
      IsInternal = internalRegex.IsMatch(Value);
    }
  }
}
```

You can use it as follows:

```csharp
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using MediatR;

namespace My.Bank.Application.Queries.IBANs
{
  public class IsInternalIbanQuery: IRequest<bool>
  {
    public string Iban {  get; }
    public IsInternalIbanQuery(string iban) => Iban = iban;
  }

  public class IsInternalIbanQueryHandler : IRequestHandler<IsInternalIbanQuery, bool>
  {
    public Task<bool> Handle(IsInternalIbanQuery request, CancellationToken cancellationToken)
      => Task.FromResult(
        new Domain.IBANs.Iban(
          request.Iban,
        // InternalIBAN is read from the database
        new Regex(My.Bank.Common.BLL.Parameters.InternalIBAN))
      .IsInternal
      );
   }
}
```

## Conclusion

Of course, the example of IBAN validation isn’t complete. An IBAN is more than just its value; it follows a pattern and you associate it with a SWIFT code.

I’d like to share another principle: “Do what matters at the present time, not more, not less\.” Back when I dealt with the bug, checking if the IBAN was an internal IBAN to the client’s bank was the requirement, not rewriting the whole validation logic of the primitive string representing an IBAN.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Mirа Fialkova (`https://www.pexels.com/photo/elegant-gift-box-with-brown-ribbon-on-blue-background-35768601/`)
