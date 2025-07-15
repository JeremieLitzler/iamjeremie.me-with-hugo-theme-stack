---
title: "What’s HATEOAS?"
description: "It ensures that client interactions with a RESTful API are driven by hypermedia provided dynamically by the server."
image: 2025-07-07-a-woman-writing-use-apis-on-a-white-board.jpg
imageAlt: "A woman writing ‘Use APIS’ on a white board."
date: 2025-07-07
categories:
  - Web Development
tags:
  - RESTFul API
---

HATEOAS stands for “Hypermedia as the Engine of Application State”. We use it to describe clearly APIs and it provides all the information necessary to consume the API naturally. It’s all about clear and explicit usage.

## Key Concepts of HATEOAS

First, the **Hypermedia** is the combination of hypertext and multimedia. In the context of web APIs, it often means including links and controls in the representations returned by the API.

For example, when a client requests a resource, the server’s response not only includes the data of that resource but also includes links to related resources and actions that can be taken next.

Then comes the **Application State**, managed by the client using the hypermedia provided by the server. This includes the transitions between different states of the application.

The client discovers available actions and resources at runtime by following links provided in the responses.

And finally, we have the **Engine of Application State**. The “engine” part refers to the idea that the hypermedia provided by the server drives the client’s state transitions.

The server tells the client what actions are possible next, and the client acts accordingly.

## The Relationship to RESTful APIs

RESTful APIs are designed based on several constraints, and HATEOAS is one of them. Here’s how HATEOAS relates to RESTful APIs:

1. It provides **Self-Descriptive Messages**, i.e., each message returned by a RESTful API includes enough information for the client to understand how to use it. This includes hypermedia links and metadata.
2. It helps with **Client-Server Interaction**. The client doesn’t need to have hard-coded knowledge of the API structure or endpoints. Instead, it dynamically discovers actions and resources by following links provided in the responses.
3. It **Decouples Client and Server**, allowing them to evolve independently. The client doesn’t rely on a fixed set of URIs or operations; it adapts based on the hypermedia controls provided by the server.
4. It provides **Navigability**. The client starts with a base URI and traverses through various states and resources using the hyperlinks embedded in the responses.

## Example

Consider a RESTful API for a bookstore. When a client requests a book resource, the response might include the book details along with links to related resources:

```json
{
  "title": "Effective Java",
  "author": "Joshua Bloch",
  "price": 45.0,
  "links": [
    {
      "rel": "self",
      "href": "<http://api.bookstore.com/books/1>"
    },
    {
      "rel": "author",
      "href": "<http://api.bookstore.com/authors/joshua-bloch>"
    },
    {
      "rel": "purchase",
      "href": "<http://api.bookstore.com/books/1/purchase>"
    }
  ]
}
```

In this example:

- The client can follow the “author” link to get more information about the author.
- The client can follow the “purchase” link to buy the book.

## Summary

HATEOAS is a fundamental aspect of REST that promotes a dynamic and flexible way for clients to interact with APIs. It allows the server to control the flow of the application.

However, it creates a little complexity on the server side since you need to keep track of the next actions. I’ll try to describe approaches to manage this in another article.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: photo by [ThisIsEngineering](https://www.pexels.com/photo/woman-writing-on-whiteboard-3861943/).
