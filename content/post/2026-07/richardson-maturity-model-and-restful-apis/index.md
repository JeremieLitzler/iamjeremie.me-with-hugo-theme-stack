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
---

I’ve called plenty of APIs “RESTful” over the years without stopping to check whether they earned the label. Most of them, it turns out, don’t get past sending POST requests using the RPC format. That’s not a character flaw in the API. It’s just level zero.

The Richardson Maturity Model, proposed by Leonard Richardson in 2008 and popularized by Martin Fowler, gives that spectrum a name. It breaks REST adoption into four levels, each one a superset of the last. One source I’ll use in this article explains why the levels matter, the other shows exactly what to type to climb them.

## Level 0: the Swamp of POX

At the bottom sits what Fowler calls “the swamp of POX”—plain old XML, or these days plain old JSON, all funneled through a single URI. Every call is a POST, and the payload itself describes the operation: create this, update that, delete the other thing. SOAP web services typically live here, and so does more home-grown API code than anyone likes to admit.

To see the difference each level actually makes, I’ll carry one example through all four: canceling order #3. At level 0, that’s a POST to the single endpoint the whole API exposes, with a body that spells out what should happen:

```http
# The request
POST /api/order/cancel HTTP/1.1
Content-Type: application/json

{"action": "cancelOrder", "orderId": 3}
```

```http
# The response
HTTP/1.1 200 OK
Content-Type: application/json

{"success": true, "message": "Order 3 cancelled"}
```

The URI (`/api/order/cancel`) says nothing about what’s being acted on. The body does all the work, and so does the “success” flag buried inside a `200 OK` that would look identical whether the cancellation worked or the whole thing failed.

## Level 1: Resources

The first real step up is giving individual things their own addresses. Instead of one endpoint for everything, `/customers/5` names a specific customer and `/orders/12’ names a specific order. Microsoft’s naming guidance is blunt about the two rules that keep this level honest: use nouns, not verbs, so `/orders`rather than`/create-order`, and use plural nouns for collections, so `/customers`for the set and`/customers/5` for one member of it. The HTTP method is supposed to carry the verb; the URI just points at the noun.

Cancelling order #3 now at least targets the right address:

```http
POST /orders/3 HTTP/1.1
Content-Type: application/json

{"action": "cancel"}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"success": true, "message": "Order 3 cancelled"}
```

The URI has improved. The method and the response shape haven't — it's still a POST carrying an instruction, and still a `200` with a hand-rolled success flag. This still isn't RESTful on its own, since most calls are still POSTs regardless of which resource they touch. But it's the scaffolding everything else builds on.

## Level 2: HTTP Verbs Earn Their Keep

This is where GET, POST, PUT, PATCH, and DELETE start meaning what the HTTP spec says they mean. It's where most production APIs that call themselves RESTful actually sit. A GET should be safe and side-effect-free, which is also what makes it cacheable. A PUT should be idempotent: sending it five times in a row should leave the resource in exactly the same state as sending it once. A PATCH carries only the fields that changed, via a JSON Patch or JSON Merge Patch document, rather than the whole resource.

Cancelling order #3 stops being a disguised instruction and becomes an honest partial update, expressed through the method itself:

```http
PATCH /api/orders/3 HTTP/1.1
Content-Type: application/merge-patch+json

{"status": "cancelled"}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"orderId": 3, "status": "cancelled"}
```

Nobody had to invent an `action` field or a `success` flag. The method (`PATCH`) says what kind of change this is, the body carries only what changed, and the status code (`200`) — not a field inside the JSON — is what tells the client whether it worked. And status codes stop being decoration generally:

| Method | Purpose                                  | Idempotent? | Typical success codes                  |
| ------ | ---------------------------------------- | ----------- | -------------------------------------- |
| GET    | Retrieve a resource or collection        | Yes         | 200, 204, 404                          |
| POST   | Create a resource, or trigger processing | No          | 200, 201 (with `Location` header), 202 |
| PUT    | Replace a resource entirely              | Yes         | 200, 201, 204, 409                     |
| PATCH  | Apply a partial update                   | No          | 200, 400, 409, 415                     |
| DELETE | Remove a resource                        | Yes         | 204, 404                               |

One detail from the Microsoft guide stuck with me: a client should never invent its own URI when creating something. It POSTs to the collection, and the server hands back the new resource's address in a `Location` header, ideally. If a client tries to PUT to a URI that doesn't exist yet expecting the server to create it there, that's a design decision the server has to opt into deliberately, not a default to assume.

Long-running operations get their own pattern here too. Instead of making the client wait on a slow POST, PUT, PATCH, or DELETE, the server returns `202 Accepted` with a `Location` header pointing at a status-polling endpoint. The client checks back until the job finishes, and if it produced a new resource, the status endpoint responds with `303 See Other` pointing at it.

Naming discipline matters just as much as verb discipline at this level. The Microsoft guide's advice on relationships is worth keeping close: reflect them through hierarchy (`/api/customers/5/orders` for a customer's orders), but stop at _collection/item/collection_. Chasing a relationship any deeper, like `/api/customers/1/orders/99/products`, will become tedious to the person who integrates the API—better to let the client fetch `/api/customers/1/orders`, then follow up with `/api/orders/99/products` once it already holds the order reference.

The same source warns against two other habits: building “chatty” APIs out of too many small resources, which forces clients into a pile of round trips, and mirroring your database schema directly in your URIs, which leaks implementation details and expands your attack surface for no benefit to the client.

Pagination, filtering, and partial responses live at this level too. `GET /api/orders?limit=25&offset=50` with a hard upper bound on `limit` keeps both payloads and abuse in check. `GET /api/orders?minCost=100&status=shipped` filters via the query string, though it's worth remembering that filter and sort parameters become part of the cache key, so they can quietly work against HTTP caching rather than for it. And for large binary resources, `Accept-Ranges` and HTTP `HEAD` let a client fetch a file in chunks and get back a `206 Partial Content` instead of the whole thing at once.

## Level 3: Hypermedia Controls

The top level is HATEOAS: Hypertext As The Engine Of Application State. Responses stop just returning data and start returning links describing what the client can do next and which URIs to use for it.

At level 2, the client had to already know that cancelling means sending a PATCH with `{“status”: “canceled”}` to `/api/orders/3’. At level 3, it doesn’t know that in advance—it discovers it, by fetching the order first and reading what the response offers:

The following request:

```http
GET /api/orders/3 HTTP/1.1
```

could respond:

```json
{
  "orderId": 3,
  "status": "open",
  "links": [
    {
      "rel": "cancel",
      "href": "https://api.contoso.com/api/orders/3",
      "action": "PATCH",
      "body": { "status": "cancelled" }
    },
    {
      "rel": "self",
      "href": "https://api.contoso.com/api/orders/3",
      "action": "GET"
    }
  ]
}
```

The client cancels the order by following the `cancel` link exactly as given—same `PATCH` to the same URI as before, but this time nothing about it was hard-coded on the client side. If a returned order has no `cancel` link, that alone tells the client the order can’t be canceled anymore (already shipped, say), without needing a separate rule baked in to explain why.

The payoff is that a client never has to hard-code a URI scheme. It follows links the way a person follows links on a web page, and the server is free to change its URI structure without breaking anyone who was actually following the protocol instead of guessing at URLs. Roy Fielding considers this level the actual precondition for calling an API REST; everything below it, in his view, is merely REST-like. Fowler doesn’t disagree, but he’s careful to frame the whole model as a teaching tool rather than a certification checklist—its job is to show, one step at a time, how REST tackles complexity through resource-orientation, standard verbs, and self-description, not to hand out a passing grade.

## The Parts That Don’t Fit Neatly Into a Level

A few practical concerns cut across all four levels rather than belonging to one of them.

### Versioning

Versioning is the big one, and Microsoft’s guide exposes there is no single correct scheme. No versioning at all works fine for additive changes, as long as clients tolerate fields they don’t recognize, but it breaks the moment you remove or rename something. URI versioning (’/v2/customers/3’) is the easiest to route and cache, but it multiplies URIs over time and complicates HATEOAS, since every link needs its own version segment. Query string versioning (’?version=2’) keeps one URI per resource, at the cost of historically poor caching behavior in older browsers and proxies. Header versioning and media type versioning (`Accept: application/vnd.contoso.v1+json`) keep the URI completely stable and pair best with HATEOAS, but they push more branching logic onto the server and weaken the cache.

### Multitenancy

When one API serves several separate organizations, every request has to say which tenant it’s acting for. That identity can travel three ways:

```http
GET https://acme.api.contoso.com/api/orders/3
```

```http
GET https://api.contoso.com/api/orders/3
X-Tenant-ID: acme
```

```http
GET https://api.contoso.com/api/tenants/acme/orders/3
```

A shared HTTP cache normally keys on the URL alone, and that’s where the three approaches stop being equivalent. The subdomain and path-segment versions bake the tenant into the URL itself, so one URL always means one tenant—a cache can’t confuse Acme’s order 3 with Beta Corp’s order 3. The header version is the risky one: two requests can hit the exact same URL, ’/api/orders/3’, and return entirely different data depending on `X-Tenant-ID`, which is precisely the situation a cache keyed only on the URL gets wrong. There’s a smaller RESTful-purity angle too: putting the tenant in the path treats it as a resource in the hierarchy, which sits more comfortably with REST’s resource-oriented style than tucking it away in a header.

### Distributed Tracing

Once a single client request fans out across several internal services, you need a way to say these calls all belong to the same original request, so you can find them together in your logs afterward. The client sends a correlation header on its way in:

```http
GET /api/orders/3 HTTP/1.1
Correlation-ID: abc-123
```

The order service, while handling that request, calls the customer service for shipping details and passes the same ID along:

```http
GET /api/customers/9 HTTP/1.1
Correlation-ID: abc-123
```

Both services log ’abc-123’ next to whatever they did, and the final response echoes it back to the original caller:

```http
HTTP/1.1 200 OK
Correlation-ID: abc-123
```

If the order later looks wrong, run a search in the logs for ’abc-123’ surfaces every hop the request took, in order, instead of leaving you to guess which of a thousand interleaved log lines belonged to this one call.

### API contracts with OpenAPI

If you rather designed the contract before writing the implementation, the OpenAPI Specification, the project formerly known as Swagger, lets you describe every endpoint, its inputs, and its responses up front:

```yaml
paths:
  /orders/{id}:
    get:
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          description: The requested order
```

Tools can then generate a documentation site and client SDKs straight from that file, before a line of the actual service exists. The cost is that OpenAPI carries its own opinions about how versioning, parameters, and responses should be shaped, so adopting it means bending your design to fit those conventions in exchange for the generated docs and clients.

None of these are levels you climb once and leave behind. They’re decisions you keep making at whichever level you’re already operating at.

## Conclusion

Most APIs I’ve worked with land somewhere in level 0, when working with SOAP and WCF, and level 1, maybe partially level 2, when working on a modern Web API. And that’s a perfectly reasonable place to stop.

The Richardson Maturity Model isn’t a ladder you’re obligated to climb to the top rung. It’s a way of naming what you’ve actually built so that “RESTful” stops being a vague compliment and starts describing something specific. Do your URIs name things instead of actions? Do your verbs mean what HTTP says they mean? Or can a client navigate your entire API having never seen its URI scheme in advance?

The answer is yours.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credits: Photo by Brendan Rühli on Pexels on the topic of maturity (`https://www.pexels.com/photo/close-up-of-a-fresh-green-leaf-on-a-tree-36858597/`).
