---
title: "How to add cannonical URL to a Hugo blog?"
description: "In SEO, it is good practice to include a canonical link in the head element of each page. Using Hugo static site generator, how do you do it? Let's dive right in."
image: images/2024-03-15-a-smartphone-and-a-pen-on-a-desk.jpg
imageAlt: "A smartphone and a pen on a desk"
date: 2024-03-15
categories:
  - Web Development
tags:
  - SEO
  - Hugo
  - Tip Of The Day
---

I’m using the [Hugo theme stack](https://github.com/CaiJimmy/hugo-theme-stack) from [Jimmy Cai](https://jimmycai.com/).

It already includes in the head template the code to add a canonical link.

But, at one stage, I had to set a link from an article I published on a publishing platform.

Therefore, I couldn’t let the theme generate a canonical link automatically.

## The goal

I wanted to keep the automation for articles first published on my blog.

Then, in some cases, I wanted to republish an article on my blog while it was already available on the Internet.

## Why

In SEO, the best practices are:

- Each webpage must have a canonical link.
- A single webpage with the same content must be published once and only once in the Internet.

If you break those two rules, then the web crawlers won’t index your pages and you will miss out on some traffic.

## Solution using the Hugo theme stack

First I had to find where the canonical link was generated. I found it in `layouts/partials/head/head.html`:

```html
<link rel="canonical" href="{{ .Permalink }}" />
```

Now, how could I specify within the frontmatter of a given article that I wanted the canonical link to be a specific one?

With a little search, I’ve found [this thread on the Hugo forum](https://discourse.gohugo.io/t/how-to-add-cannonical-url-to-a-blog/34670/4).

The frontmatter data is accessible through `.Params` that contains key/value pairs.

The key is the name of the frontmatter property.

In my case, I named the canonical `relcanonical` and the value had to be a string.

It gives you the following:

```yaml
---
relcanonical: https://iamjeremie.me
---
```

The `head.html` line above had to change to the following:

```htm
{{ with .Params.relcanonical }}
<link rel="canonical" href="{{ . | relLangURL }}" itemprop="url" />
{{ else -}}
<link rel="canonical" href="{{ .Permalink }}" itemprop="url" />
{{ end -}}
```

In the above code,

- When the `relcanonical` is set (`{{ with .Params.relcanonical }}`)
- Use its value, which is the `.` in `{{ . }}`.

{{< blockcontainer jli-notice-note "The moustache syntax is used for Go programming within the HTML template">}}

{{< /blockcontainer >}}

I hope you found this useful.

Credit : Photo by [Steve Johnson](https://unsplash.com/@steve_j?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/black-smartphone-beside-pen-rNYCrcjUnOA?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
