---
title: "Building an HTML accordion without JavaScript"
description: "JavaScript isn’t always essential. Sometimes, just using HTML and a little CSS is enough. Let’s take a look at a concrete use case."
image: images/2024-02-11-a-vintage-accordeon.jpg
imageAlt: "A vintage accordeon"
date: 2024-03-11
categories:
  - Web Development
tags:
  - HTML
  - CSS
  - Tip Of The Day
---

Do you know the `details` and `summary` HTML element?

You should.

To create an accordion with no JavaScript, they are your friends.

But you may want to customize the look.

Using the `::after` pseudo-class on the `summary` element, you can add some content with the `content` property.

What about changing the content based on the state of the `details` element (e.g. opened or closed)?

Apply a different style when the accordion is open using the `details[open]` selector.

Here is the live demo I use on my blog [on JSFiddle](https://jsfiddle.net/puzzlout/j09efgpn/).

Enjoy!

Credit : Photo by [Gaelle Marcel](https://unsplash.com/@gaellemarcel?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/brown-chest-near-wall-MwMmOtj6z2c?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
