---
title: "Richardson Maturity Model and RESTFul APIs"
description: "When designing and organizing resources in a Web API, following best practices ensures clarity, scalability, and maintainability."
image: 2026-07-27-a-little-branch-growing-out-of-a-trunk.jpg
imageAlt: A little branch growing out of a trunk
date: 2026-07-27
categories:
  - Software Development
tags:
  - REST
  - API Design
draft: true
---

I've called plenty of APIs "RESTful" over the years without stopping to check whether they earned the label. Most of them, it turns out, don't get past sending POST requests to a handful of URLs with a JSON blob describing what they actually want to happen. That's not a character flaw in the API. It's just level zero.

The Richardson Maturity Model, proposed by Leonard Richardson in 2008 and popularized by Martin Fowler, gives that spectrum a name. It breaks REST adoption into four levels, each one a superset of the last, and reading through it next to Microsoft's own Azure Architecture Center guide to API design turned into a useful exercise: one source explains why the levels matter, the other shows exactly what to type to climb them.

## Level 0: the swamp of POX

At the bottom sits what Fowler calls "the swamp of POX" — plain old XML, or these days plain old JSON, all funneled through a single URI. Every call is a POST, and the payload itself describes the operation: create this, update that, delete the other thing. It's remote procedure calls wearing an HTTP costume. SOAP web services typically live here, and so does more home-grown API code than anyone likes to admit.

## Level 1: resources

The first real step up is giving individual things their own addresses. Instead of one endpoint for everything, `/customers/5` names a specific customer and `/orders/12` names a specific order. Microsoft's naming guidance is blunt about the two rules that keep this level honest: use nouns, not verbs, so `/orders` rather than `/create-order`, and use plural nouns for collections, so `/customers` for the set and `/customers/5` for one member of it. The HTTP method is supposed to carry the verb; the URI just points at the noun.

This still isn't RESTful on its own, since most calls are still POSTs regardless of which resource they touch. But it's the scaffolding everything else builds on.

## Level 2: HTTP verbs earn their keep

This is where GET, POST, PUT, PATCH, and DELETE start meaning what the HTTP spec says they mean, and it's where most production APIs that call themselves RESTful actually sit. A GET should be safe and side-effect-free, which is also what makes it cacheable. A PUT should be idempotent: sending it five times in a row should leave the resource in exactly the same state as sending it once. A PATCH carries only the fields that changed, via a JSON Patch or JSON Merge Patch document, rather than the whole resource. And status codes stop being decoration:

| Method | Purpose                                  | Idempotent? | Typical success codes                  |
| ------ | ---------------------------------------- | ----------- | -------------------------------------- |
| GET    | Retrieve a resource or collection        | Yes         | 200, 204, 404                          |
| POST   | Create a resource, or trigger processing | No          | 200, 201 (with `Location` header), 202 |
| PUT    | Replace a resource entirely              | Yes         | 200, 201, 204, 409                     |
| PATCH  | Apply a partial update                   | No          | 200, 400, 409, 415                     |
| DELETE | Remove a resource                        | Yes         | 204, 404                               |

One detail from the Microsoft guide stuck with me: a client should never invent its own URI when creating something. It POSTs to the collection, and the server hands back the new resource's address in a `Location` header. If a client tries to PUT to a URI that doesn't exist yet expecting the server to create it there, that's a design decision the server has to opt into deliberately, not a default to assume.

Long-running operations get their own pattern here too. Instead of making the client wait on a slow POST, PUT, PATCH, or DELETE, the server returns `202 Accepted` with a `Location` header pointing at a status-polling endpoint. The client checks back until the job finishes, and if it produced a new resource, the status endpoint responds with `303 See Other` pointing at it.

Naming discipline matters just as much as verb discipline at this level. The Microsoft guide's advice on relationships is worth keeping close: reflect them through hierarchy (`/customers/5/orders` for a customer's orders), but stop at _collection/item/collection_. Chasing a relationship any deeper, like `/customers/1/orders/99/products`, turns brittle fast — better to let the client fetch `/customers/1/orders`, then follow up with `/orders/99/products` once it already holds the order reference. The same document warns against two other habits: building "chatty" APIs out of too many small resources, which forces clients into a pile of round trips, and mirroring your database schema directly in your URIs, which leaks implementation details and expands your attack surface for no benefit to the client.

Pagination, filtering, and partial responses live at this level too. `GET /orders?limit=25&offset=50` with a hard upper bound on `limit` keeps both payloads and abuse in check. `GET /orders?minCost=100&status=shipped` filters via the query string, though it's worth remembering that filter and sort parameters become part of the cache key, so they can quietly work against HTTP caching rather than for it. And for large binary resources, `Accept-Ranges` and HTTP `HEAD` let a client fetch a file in chunks and get back a `206 Partial Content` instead of the whole thing at once.

## Level 3: hypermedia controls

The top level is HATEOAS: Hypertext As The Engine Of Application State. Responses stop just returning data and start returning links describing what the client can do next and which URIs to use for it. Here's the shape Microsoft uses for an order that links to its customer:

```json
{
  "orderID": 3,
  "productID": 2,
  "quantity": 4,
  "orderValue": 16.6,
  "links": [
    {
      "rel": "customer",
      "href": "https://api.contoso.com/customers/3",
      "action": "GET"
    },
    {
      "rel": "customer",
      "href": "https://api.contoso.com/customers/3",
      "action": "PUT"
    }
  ]
}
```

The payoff is that a client never has to hard-code a URI scheme. It follows links the way a person follows links on a web page, and the server is free to change its URI structure without breaking anyone who was actually following the protocol instead of guessing at URLs. Roy Fielding considers this level the actual precondition for calling an API REST; everything below it, in his view, is merely REST-like. Fowler doesn't disagree, but he's careful to frame the whole model as a teaching tool rather than a certification checklist — its job is to show, one step at a time, how REST tackles complexity through resource-orientation, standard verbs, and self-description, not to hand out a passing grade.

## The parts that don't fit neatly into a level

A few practical concerns cut across all four levels rather than belonging to one of them.

Versioning is the big one, and Microsoft's guide is refreshingly honest that there's no single correct scheme. No versioning at all works fine for additive changes, as long as clients tolerate fields they don't recognize, but it breaks the moment you remove or rename something. URI versioning (`/v2/customers/3`) is the easiest to route and cache, but it multiplies URIs over time and complicates HATEOAS, since every link needs its own version segment. Query string versioning (`?version=2`) keeps one URI per resource, at the cost of historically poor caching behavior in older browsers and proxies. Header versioning and media type versioning (`Accept: application/vnd.contoso.v1+json`) keep the URI completely stable and pair best with HATEOAS, but they push more branching logic onto the server and weaken cache-key locality.

Multitenancy is another cross-cutting concern: tenant identity can travel via a subdomain, a header like `X-Tenant-ID`, or a path segment, and each choice trades off differently against caching and RESTful purity. Distributed tracing asks for a correlation header, something like `Correlation-ID` or `X-Request-ID`, propagated through the request and echoed back in the response so a single call can be followed across however many services it touches. And if you'd rather design the contract before writing the implementation, adopting the OpenAPI Specification (the project formerly known as Swagger) buys you generated documentation and client libraries, in exchange for conforming to its own opinions about what a REST API should look like.

None of these are levels you climb once and leave behind. They're decisions you keep making at whichever level you're already operating at.

## Conclusion

Most APIs I've worked with land somewhere in level 2 and stop, and for a lot of systems that's a perfectly reasonable place to stop. The Richardson Maturity Model isn't a ladder you're obligated to climb to the top rung; it's a way of naming what you've actually built, so that "RESTful" stops being a vague compliment and starts describing something specific: whether your URIs name things instead of actions, whether your verbs mean what HTTP says they mean, and whether a client could navigate your entire API having never seen its URI scheme in advance.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credits: Photo by Brendan Rühli on Pexels on the topic of maturity (`https://www.pexels.com/photo/close-up-of-a-fresh-green-leaf-on-a-tree-36858597/`).
