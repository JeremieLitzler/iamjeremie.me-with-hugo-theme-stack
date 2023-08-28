---
title: CSS Variables
description: Enhance your CSS with variables without LESS or SASS
date: 2018-02-22
categories:
  - Web Fundamentals
  - Web Development
tags:
  - CSS
  - CSS Variables
---

## Sources

[Medium article by Per Harald Borgen](https://medium.freecodecamp.org/learn-css-variables-in-5-minutes-80cf63b4025d)

## Why learn CSS Variables?

- To build a theme where you will reuse a property value many many many times
  - ex: the brand color or the size of a button.
- To build better responsive designs

## Local vs Global

### Global

```css
:root {
  --brand-color: blue;
}
button {
  background-color: var(--brand-color);
}
```

### Local

```css
.alert {
  --alert-color: #ff6f69;
}
.alert p {
  color: var(--alert-color);
  border: 1px solid var(--alert-color);
}
```

## Better responsiveness

```css
:root {
  --main-font-size: 16px;
}
media all and (max-width: 600px) {
  :root {
    --main-font-size: 12px;
  }
}
```

## How to access variables with JavaScript

```js
var root = document.querySelector(':root');
var rootStyles = getComputedStyle(root);
var mainColor = rootStyles.getPropertyValue('--main-color');

root.style.setProperty('--main-color', '#88d8b0');
```
