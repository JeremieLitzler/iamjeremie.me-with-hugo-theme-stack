---
title: "Good SEO with Hugo"
description: "One thing that I needed on my blogs was to make my articles SEO-effecient. Let’s look at how I did it with Hugo and Jimmy Cai’s theme."
image: images/2024-08-07-scrabble-letters-forming-the-word-seo.jpg
imageAlt: 'Scrabble letters forming the word "SEO"'
date: 2024-08-14
categories:
  - Web Development
tags:
  - SEO
draft: true
---

I wrote [an article last week](../good-seo-with-vuepress-2/index.md) about the SEO topic with the SSG Vuepress 2 when using Mr Hope's awesome theme.

Well, in the Hugo SSG side, Jimmy Cai has built a great theme as well.

When it comes to writing articles, I always needed something simple and easy to work with.

I tried Hugo for performance reasons.

Today, I’ll share the experience I acquired using Huo to build a blog that performs and provides naturally good SEO.

## Background

### What is Hugo

Hugo is the SSG (Static Site Generator) engine based on Go.
Hugo is the SSG framework based on Go.

It is maintened by [bep](https://github.com/bep) and [jmooring](https://github.com/jmooring) mainly (website: https://gohugo.io/) and I use it for my blogs:

- [My French blog](https://jeremielitzler.fr/)
- [My English blog](https://iamjeremie.me/), where you currently are.

Formely, my blogs used Vuepress, but I switched to Hugo because it reached a point where it was taxing on my Netlify build minutes… I explain why in the VuePress article quoted above.

Why? When you reach a certain number of pages and articles, the Node-based Vuepress show its limitations (more about it in [this discussion](https://github.com/orgs/vuepress-theme-hope/discussions/2887)).

### What can Hugo do

Similarly to Vuepress, it takes simply takes Markdown content and parse it to generate an HTML file.

You use a theme to apply a template to the generate HTML content.

It is extendable through shortcodes written in HTML and Go: Also, you can find fully-fledged themes like Jimmy Cai's that is just perfect for blogging. Feel free to [visit this page for more details](https://github.com/CaiJimmy/hugo-theme-stack) and [his starter project](https://github.com/CaiJimmy/hugo-theme-stack-starter).

## How to use frontmatter for SEO purposes

Now, when it comes to SEO, it starts the same way as with Vuepress: a `title` tag and a `description` meta.

You can achieve this by using the same frontmatter you would with Vuepress:

```yaml
---
title: "How to run a NodeJS REST API on Cloudways?"
description: "I am developping a custom search API from VuePress static websites and I needed to host it. Since I have a Cloudways VPS, let's see how to run the REST API."
---
```

Then, it deverges for the rest.

### For semantic HTML

In some places, I had to adjust the heading elements to comply with the rules of good semantic HTML, important for SEO as well as best practices.

For example, in the `layouts\_default\archives.html`, I had a `h2` instead of `h1` for the first heading of the page.

It happened to be the same on `ayouts\page\search.html` page and many partial view like `layouts\partials\article\components\details.html` which renders the details of all articles.

I worked quite a bit on the left menu as well so that it wouldn't display the `h1` and `h2` for the site name and description when browsing a page or an article. The exception remains the homepage where the list of article use a `h2` while the site name is a `h1`.

This was a very tricky part to modify sincne the partial views used were the same between the home page and the categories, tags, search and archives pages.

However, I felt I had a good opportunity to get started and mess up, in a good way, with Hugo and Go programming.

### For the canonical link

I updated the theme itself in a local copy (I don't use Jimmy's theme as a live template because once, it broke my Netlify build).

So in the `head.html`, I added this:

```html
<!-- https://discourse.gohugo.io/t/how-to-add-cannonical-url-to-a-blog/34670/4 -->
{{ with .Params.relcanonical }}
<link rel="canonical" href="{{ . | relLangURL }}" itemprop="url" />
{{ else -}}
<link rel="canonical" href="{{ .Permalink }}" itemprop="url" />
{{ end -}}
```

What it means is that if the frontmatter contains the `relcanonical` property, then use it. Otherwise, the actual page or article link is used.

I rarely use `relcanonical`, but it is handy to have available.

For example, I had a LinkedIn post that I published before the article here:

```yaml
---
relcanonical: https://www.linkedin.com/pulse/making-unused-method-argument-compliant-typescript-eslint-litzler-uiktf/
---
```

### For head image in articles

By default, I couldn't set a custom image alt text to the head image in the article.

To use the following, I have to modify `layouts\partials\article\components\header.html`, which represents the top section of all articles.

```yaml
title: "Good SEO with Hugo"
description: "One thing that I needed on my blogs was to make my articles SEO-effecient. Let’s look at how I did it with Hugo and Jimmy Cai’s theme."
image: images/2024-08-07-scrabble-letters-forming-the-word-seo.jpg
imageAlt: 'Scrabble letters forming the word "SEO"'
```

In the partial view template, I modified the code from:

```go
<img src="{{ $Permalink }}"
                        {{ with $Srcset }}srcset="{{ . }}"{{ end }}
                        width="{{ $Width }}"
                        height="{{ $Height }}"
                        loading="lazy"
                        alt="Featured image of post {{ .Title }}" />
```

to

```go
<img src="{{ $Permalink }}"
                        {{ with $Srcset }}srcset="{{ . }}"{{ end }}
                        width="{{ $Width }}"
                        height="{{ $Height }}"
                        alt="{{ .Params.imageAlt }}"
						            title="{{ .Params.imageAlt }}" />
```

You might see another difference with the `loading="lazy"` attribute missing. Well, that's because you don't need it on the images in the viewport on page load.

### For OpenGraph metas

It is taken care of by the `layouts\partials\head\opengraph\provider\base.html`. It reads the frontmatter `title` and `description` of the page or article. So, unlike Vuepress, you don't need to specify them and it lightens the Markdown a lot, doesn't it?

Similarly, `hugo-theme-stack-master\layouts\partials\head\opengraph\provider\twitter.html` processes the addition of the Twitter meta tags.

## Conclusion

There, you have it. No fancy plugin, no dependency (except for Go and Hugo), no complex setup. You can use Hugo and Jimmy’s theme and build today your blog with good SEO out-of-the-box!

I’ve yet to built a boilerplate. [Let me know if you need help](../../../page/contact-me/index.md).

Start blogging today and forget WordPress!

Credit: Photo by [Pixabay](https://www.pexels.com/photo/three-white-and-black-scrabble-tiles-on-brown-wooden-surface-270637/)
