---
title: "How to call an external API with valid CORS?"
description: "Have you ever needed to call a third party API that resides on a different domain? You probably had CORS issues."
image: images/2024-08-02-matrix-like-background.jpg
imageAlt: Matrix-like background
date: 2024-08-02
categories:
  - Web Development
tags:
  - Security
---

## The problem

I tested the LLM from Infomaniak the other day and I struggled with the CORS (Cross-Origin Resource Sharing) issue again.

It is a recurring issue when you host your app on the `https://my-app.com` and it requests an api on `https://api.example.com`.

The browser will prevent you from doing so unless the backend allows the frontend explicitly with the `Access-Control-Allow-Origin` header, hopefully not `*`.

MDN describes in detail [the concept on their website](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

## The Solution

If you use Netlify, you can use two methods:

### `netlify.toml` file

As a Netlify forum thread states, you need to define a rewrite rule:

```toml
# This is the rule to query the API without CORS
[[redirects]]
  from = "/api/*"
  to = "https://api.example.com/:splat"
  status = 200
  force = true

# This is the rule you set to handle soft 404 in your SPA
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

{{< blockcontainer jli-notice-tip "">}}

The `:splat` placeholder represents everything after `https://api.example.com/`.

{{< /blockcontainer >}}

### A `_redirects` File

This option is the same as above, but you write it differently:

```txt
/api-llm https://api.example.com/:splat 200
/\* /index.html 200
```

Also, be sure to name the file `_redirects` and place it in the `public` directory.

Credits: Photo by [Markus Spiske](https://unsplash.com/@markusspiske?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/matrix-movie-still-iar-afB0QQw?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
