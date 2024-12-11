---
title: "How Do You Save a File With JavaScript?"
description: "Sometimes, it’s handy to save some content directly from JavaScript to a physical file. Here is the code!"
image: do-something-great-sign.jpg
imageAlt: 'A "Do Something Great" sign in the dark'
date: 2024-12-11
categories:
  - Web Development
tags:
  - JavaScript
---

## The Code

It’s simple:

- Create an anchor (`a`) element.
- Append it to the DOM.
- Simulate a click
- Remove the element from the DOM

```javascript
function downloadFile(filename, textData, dataType = "text/plain") {
  const node = Object.assign(document.createElement("a"), {
    href: `data:${dataType};charset=utf-8,${encodeURIComponent(textData)}`,
    download: filename,
    style: "display: none",
  });
  document.body.appendChild(node);
  node.click();
  document.body.removeChild(node);
}
```

## The Live Demo

Here is a live demo [on jsfiddle](https://jsfiddle.net/puzzlout/ehyqajLr/3/).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

<!-- more -->

Credit: photo by [Clark Tibbs](https://unsplash.com/@clarktibbs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/do-something-great-neon-sign-oqStl2L5oxI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
