---
title: "Extract arrays from a list of objects into a single array."
description: "Have you ever needed to put arrays from a list of objects into the single array? JavaScript provides a native API to do it and it’s simple."
image: images/2024-03-13-shoes-sorted-into-trays.jpg
imageAlt: "Shoes sorted into trays"
date: 2024-03-13
categories:
  - Web Development
tags:
  - JavaScript
  - Tip Of The Day
---

It’s simple: use the `Array.prototype.flatMap()` method along with the object destructuring.

For example, you have this array of objects. Each object contains an array of primitive values:

```json
"categories": [
    {
      "forums": [
        "-KpOx5Y4AqRr3sB4Ybwj",
        "-KsjO4_W3W9Q2Z2UmuPr"
      ],
      "name": "Feedback & Information",
      "slug": "feedback-and-information",
      "id": "-KpR7vRkiRPpbUd_TVAR"
    },
    {
      "forums": [
        "-KsjPat5MWCx-dkjNVg8",
        "-KsjPjasLh0TFtZmffEo",
        "-Kvd1Vg_ankLYgrxC50F",
        "-KvdCowY9mDvM0EH8Pvs",
        "-KvhkEl6F673igPtnbso"
      ],
      "name": "Discussions",
      "slug": "discussions",
      "id": "-KsjPKA6hDuHlQK_lJWO"
    },
    {
      "forums": [
        "-Kvclvu_Qd9QdS9ciqUl",
        "-KvcmOcppNYK8NCesmB9"
      ],
      "name": "Comedy",
      "slug": "comedy",
      "id": "-KvclpNRjpI5W-j0JQGU"
    }
  ],
```

If you want to get the forum strings, using object destructuring and `flatMap` will provide you the solution:

```tsx
const forums = categories.flatMap(({ forums }) => forums);
```

The result will give you:

```json
[
  "-KpOx5Y4AqRr3sB4Ybwj",
  "-KsjO4_W3W9Q2Z2UmuPr",
  "-KsjPat5MWCx-dkjNVg8",
  "-KsjPjasLh0TFtZmffEo",
  "-Kvd1Vg_ankLYgrxC50F",
  "-KvdCowY9mDvM0EH8Pvs",
  "-KvhkEl6F673igPtnbso",
  "-Kvclvu_Qd9QdS9ciqUl",
  "-KvcmOcppNYK8NCesmB9"
]
```

[Check out the JSFiddle demo](https://jsfiddle.net/puzzlout/98w7h4xL/) to prove it.

Enjoy!

Credit : Photo by [Alev Takil](https://unsplash.com/@alevisionco?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/assorted-color-sneakers-d-1FY75fh_s?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
