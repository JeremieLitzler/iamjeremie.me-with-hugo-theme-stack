---
title: "Good SEO with Vuepress 2"
description: "One thing that I needed on my blogs was to make my articles SEO-effecient. Let’s look at how I did it with Vuepress 2."
image: images/2024-08-07-scrabble-letters-forming-the-word-seo.jpg
imageAlt: 'Scrabble letters forming the word "SEO"'
date: 2024-08-07
categories:
  - Web Development
tags:
  - SEO
  - Vue
  - Static Site Generators
  - JAMStack
---

When it comes to writing articles, I always needed something simple and easy to work with.

I tried WordPress. But you’ll end up paying either for a plugin or an expert to reach nearly 100 on Lighthouse scores, **in all categories**.

Today, I’ll share the experience I acquired using Vuepress to build a blog that performs and provides naturally good SEO.

## Background

### What is Vuepress

Vuepress is the SSG (Static Site Generator) engine based on Vue and Vite (for version 2).

It’s maintained by [_Mr Hope_](https://github.com/Mister-Hope) and [_meteorlxy_](https://github.com/meteorlxy) mainly (website: https://v2.vuepress.vuejs.org/) and I’ve used it for several simple projects:

- [A website built for a quinoa producer in Normandy](https://inflorescences-quinoa.fr/)
- [A personal project to teach about energy consumption and production](https://passonslecap.fr/)

Previously, my blogs used Vuepress, but I switched to Hugo for performance reason.

Why? When you reach a certain number of pages and articles, the Node-based Vuepress show its limitations (more about it in [this discussion](https://github.com/orgs/vuepress-theme-hope/discussions/2887)).

### What can Vuepress do

It simply takes Markdown content and parses it to generate HTML files using a JavaScript theme, in the case of Vuepress, it’s built on top of Vue 3.

Vuepress extends through plugins or fully fledged themes, like Mr Hope’s theme, adding really cool Markdown syntax extensions to your Markdown.

Feel free to visit [this page](https://theme-hope.vuejs.press/) for more details.

## How to use frontmatter for SEO purposes

Now, I’ll share a use case using Mr Hope’s theme. Maybe other themes will or won’t support this.

So, first, good SEO starts with a good `title` tag ([up to 60 characters](https://www.google.com/search?q=seo+title+length+limit)) and a `description` meta ([up to 150–160 characters](https://www.google.com/search?q=seo+description+length+limit)).

{{< blockcontainer jli-notice-note "About the metrics">}}

Those metrics aren’t rules that apply to all titles or descriptions.

I like [this article about the pixel size](https://medium.com/@masaharuhayataki/busting-the-seo-myth-title-length-limit-is-not-50-60-characters-1debab9acbb3) when rendered on the screen.

{{< /blockcontainer >}}

You can achieve this by using the following frontmatter:

```yaml
---
title: "How to run a NodeJS REST API on Cloudways?"
description: "I am developping a custom search API from VuePress static websites and I needed to host it. Since I have a Cloudways VPS, let's see how to run the REST API."
---
```

Then, you have the Canonical link:

```yaml
head:
  - [
      link,
      {
        rel: canonical,
        href: https://iamjeremie.me/2023/07/how-to-run-a-nodejs-rest-api-on-cloudways,
      },
    ]
```

Then, OpenGraph metas:

```yaml
head:
  - [
      meta,
      { "og:type": article },
      meta,
      { "og:title": "Mon retour d'expérience avec le kit Bafang VAE 250 W" },
      meta,
      {
        "og:description": "Voilà plus de 5 ans que je roule en VAE, au début en Scott CX Comp de 2011, puis sur un Raleigh Brazil. Je vous explique le pourquoi, comment et mon ressenti.",
      },
      meta,
      {
        "og:image": /images/2023-07-25-le-raleigh-brazil-300-ex-en-mode-vae.jpg,
      },
    ]
```

Or the Twitter, a.k.a X, meta tags:

```yaml
head:
  - [
      meta,
      { "og:type": article },
      meta,
      {
        "twitter:title": "Mon retour d'expérience avec le kit Bafang VAE 250 W",
      },
      meta,
      {
        "twitter:description": "Voilà plus de 5 ans que je roule en VAE, au début en Scott CX Comp de 2011, puis sur un Raleigh Brazil. Je vous explique le pourquoi, comment et mon ressenti.",
      },
      meta,
      {
        "twitter:image": /images/2023-07-25-le-raleigh-brazil-300-ex-en-mode-vae.jpg,
      },
      meta,
      { "twitter:card": "summary_large_image" },
    ]
```

With `og:*` and `twitter:*` meta tags, you get rich previews on all platforms (I’ve tested on LinkedIn, X, Substack and Facebook).

It’ll help your page or article when sharing it on social media.

## Limitations

It’s quite verbose to write frontmatter that generates the appropriate meta tags in the HTML. Plus, you repeat some values for different meta tags, for example `description` vs `og:description` vs `twitter:description`.

So I crafted a snippet to fill the frontmatter more quickly. Here is the example of `og:*`:

```json
{
  "FM Template for OpenGraph meta": {
    "scope": "yaml",
    "prefix": "set og:metas",
    "body": [
      "meta,",
      "{ \"og:type\": article },",
      "meta,",
      "{ \"og:title\": \"\" },",
      "meta,",
      "{",
      "  \"og:description\": \"\",",
      "},",
      "meta,",
      "{",
      "  \"og:image\": /images/.jpg,",
      "},"
    ],
    "description": "Set prev and next articles"
  }
}
```

You can use it directly in your frontmatter to add the meta tags to your convenience.

You could add to the snippet the `canonical` link, recommended on all pages and the `twitter` meta tags.

## Conclusion

There, you have it. No fancy plugin nor complex setup. You can use Vuepress and Mr Hope’s theme and build today your blog with good SEO out-of-the-box!

I’ve built a boilerplate [here](https://github.com/Puzzlout/TemplateVuepress) for English speakers and [there](https://github.com/JeremieLitzler/mon-site-demo-tutoriel) for French speakers.

Start building!

Credit: Photo by [Pixabay](https://www.pexels.com/photo/three-white-and-black-scrabble-tiles-on-brown-wooden-surface-270637/)
