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
  - Go
  - Hugo
  - Static Site Generators
  - JAMStack
---

I wrote [an article last week](../good-seo-with-vuepress-2/index.md) about the SEO topic with the SSG Vuepress 2 when using Mr Hope’s awesome theme.

Well, on the Hugo SSG side, Jimmy Cai has built a great theme as well.

When it comes to writing articles, I always needed something simple and easy to work with.

I tried Hugo for performance reasons.

Today, I’ll share the experience I acquired using Hugo to build a blog that performs well and provides naturally good SEO.

## Background

### What is Hugo

Hugo is the SSG (Static Site Generator) engine based on Go.

[bep](https://github.com/bep) and [jmooring](https://github.com/jmooring) maintain Hugo with the help of other contributors (website: https://gohugo.io/) and I use it for my blogs:

- [My French blog](https://jeremielitzler.fr/)
- [My English blog](https://iamjeremie.me/), where you currently are.

Formally, my blogs used Vuepress, but I switched to Hugo because it reached a point where it was taxing on my Netlify build minutes… I explain why in the VuePress article quoted above.

### What can Hugo do

Similarly to Vuepress, it simply takes Markdown content and parse it to generate an HTML file.

You use a theme to apply a template to the generate HTML content.

It’s extendable through shortcodes written in HTML and Go. Also, you can use fully fledged themes like Jimmy Cai’s that is just perfect for blogging. Feel free to [visit this page for more details](https://github.com/CaiJimmy/hugo-theme-stack) and [his starter project](https://github.com/CaiJimmy/hugo-theme-stack-starter).

## How to use frontmatter for SEO purposes

Now, when it comes to SEO, it starts the same way as with Vuepress: a `title` tag and a `description` meta.

You can achieve this by using the same frontmatter you would with Vuepress:

```yaml
---
title: "How to run a NodeJS REST API on Cloudways?"
description: "I am developping a custom search API from VuePress static websites and I needed to host it. Since I have a Cloudways VPS, let's see how to run the REST API."
---
```

Then, it diverges for the rest.

### For semantic HTML

In some places, I had to adjust the theme’s heading elements to comply with the rules of good semantic HTML, important for natural SEO as well as best practices.

For example, in the `layouts\_default\archives.html`, I had a `h2` instead of `h1` for the first heading of the page.

Same thing in `layouts\page\search.html` page and many partial views like `layouts\partials\article\components\details.html` which renders the details of all articles.

Why was that?

Well, in the left menu, the site name was the `h1`, which is fine on the homepage. However, in my opinion, it didn’t apply to the other pages, in particular the articles, other custom pages or generated page for categories and tags. I worked quite a bit on the left menu so that it wouldn’t display the `h1` and `h2` for the site name and description when browsing to any page that wasn’t the homepage.

This ended up as a very tricky part to modify since the partial views used were the same between the homepage and the categories, tags, search and archives pages.

However, I feel like I took the opportunity to get started and mess up, in a good way, with Hugo and Go programming.

### For the canonical link

I updated the theme itself in a local copy. I don’t use Jimmy’s theme as a live template because, once, it broke my Netlify build on an automatic update. This is how it’s set up if you use his starter repository).

So in the `head.html`, I added this:

```html
<!-- https://discourse.gohugo.io/t/how-to-add-cannonical-url-to-a-blog/34670/4 -->
{{ with .Params.relcanonical }}
<link rel="canonical" href="{{ . | relLangURL }}" itemprop="url" />
{{ else -}}
<link rel="canonical" href="{{ .Permalink }}" itemprop="url" />
{{ end -}}
```

What does it mean? If the frontmatter contains the `relcanonical` property, then use it. Otherwise, the actual page or article link generated by Hugo is used.

I rarely use `relcanonical`, but it’s handy to have available.

For example, I had a LinkedIn post that I published before the article once:

```yaml
---
relcanonical: https://www.linkedin.com/pulse/making-unused-method-argument-compliant-typescript-eslint-litzler-uiktf/
---
```

This tells the web crawlers that the original content is the canonical link.

### For head image in articles

By default, I couldn’t set a custom image alt text to the head image in the article. To me, it was a must-have.

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

You might notice another difference with the `loading="lazy"` attribute missing. Well, that’s because you don’t need it on the images in the _viewport_ on page loads.

I had to modify the article list view for example so that the first three article tiles didn’t use the `loading="lazy"` attribute, but the following did.

For that, I need to pass on to the article list tile header the index of the article in the list.

But how did I get the `pageIndex`?

In the `index.html`, I modified the _for loop_ and set the variable which I passed through the `.Scratch.Set` method:

```go
    <section class="article-list">
        {{ range $index, $element := $pag.Pages }}
			      {{ .Scratch.Set "pageIndex" $index }}
            {{ partial "article-list/default" . }}
        {{ end }}
    </section>
```

Then, I read the index in the article list tile header view using `.Scratch.Get` and calculated the `outOfVisibleViewPort` variable:

```go
 {{- $pageIndex := .Scratch.Get "pageIndex" }}
 {{- $outOfVisibleViewPort := ge (int $pageIndex) 3 }}
```

Finally, in the `<img>` element, I told Hugo to render the `loading="lazy"` is the`$outOfVisibleViewPort` equaled to `true`:

```go
     <img src="{{ $Permalink }}"
        {{ with $Srcset }}srcset="{{ . }}"{{ end }}
        width="{{ $Width }}"
        height="{{ $Height }}"
				{{ with $outOfVisibleViewPort }}
          loading="lazy"
				{{ end }}
        alt="{{ .Params.imageAlt }}" />
```

### For OpenGraph and Twitter meta tags

The theme takes care of it out of the box, through the `layouts\partials\head\opengraph\provider\base.html` view. It reads the frontmatter `title` and `description` of the page or article. So, unlike Vuepress, you don’t need to specify them. It lightens the frontmatter a lot, doesn’t it? 😁

Similarly, `hugo-theme-stack-master\layouts\partials\head\opengraph\provider\twitter.html` processes the addition of the Twitter meta tags.

## Conclusion

There, you have it. No fancy plugin, no dependency (except for Go and Hugo), no complex setup. You can use Hugo and Jimmy’s theme and build today your blog with good SEO out-of-the-box!

I have yet to build a boilerplate. [Let me know if you need help](../../../page/contact-me/index.md).

Start blogging today and forget WordPress!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Pixabay](https://www.pexels.com/photo/three-white-and-black-scrabble-tiles-on-brown-wooden-surface-270637/)
