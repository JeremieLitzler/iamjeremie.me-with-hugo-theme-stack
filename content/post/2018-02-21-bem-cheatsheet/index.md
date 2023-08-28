---
title: A BEM Cheatsheet
description: 'How does BEM work to structure CSS?'
date: 2018-02-21
categories:
  - Web Development
tags:
  - BEM
  - CSS
---

## Sources

- [BEM site](http://getbem.com/naming/)
- [Medium article by Ohans Emmanuel](https://medium.freecodecamp.org/css-naming-conventions-that-will-save-you-hours-of-debugging-35cea737d849)

## Examples for **Blocks**

```css
.stick-man {
  font-family: Roboto;
}
.hash-man {
  font-family: Hastag;
}
```

## Examples for **Elements**

```css
.stick-man__head {
  font-size: 10em;
}
.stick-man__arm {
  font-size: 4em;
}
.stick-man__leg {
  font-size: 5em;
}
```

## Examples for **Modifiers**

```css
.stick-man--red {
  color: red;
}
.stick-man--blue {
  color: blue;
}
```

## Combining Blocks, Elements and Modifiers

Let's make a stick man with a big head and another one with a small head

```css
.stick-man__head--big {
  font-size: large;
}
.stick-man__head--small {
  font-size: small;
}
```
