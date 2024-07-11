---
title: "My cheatsheet of JavaScript functions"
description: "And the list will grow over time. Bookmark the link for future reading."
image: images/2024-07-11-javascript-code-sample.jpg
imageAlt: "JavaScript code sample"
date: 2024-07-11
categories:
  - Web Development
tags:
  - Tip Of The Day
  - JavaScript
---

Below, you’ll find a few code samples of JavaScript that I often use and would like to save a quick reference.

## Does an array contains a value

Use `includes` if the value to find matches the type of each value in the array.

```tsx
const arrayContains = (anArray, myValue) =>
  anArray.includes((item) => item === myValue);
```

## Does an array contains only truthy values

Use `reduce` with the initial value to true and if all value are `true` then the result is true too.

```tsx
const allButtonsDisabled = (anArrayOfHtmlButton) =>
  anArrayOfHtmlButton.reduce(
    (accumulator, next) => accumulator && next.disabled,
    true
  );
```

## Sum up values

Again, use `reduce` for this scenario:

```tsx
const sum = (anArrayOfNumbers) =>
  anArrayOfNumbers.reduce((total, next) => total + next, 0);
```

Of course, make sure all values are numbers or floats to avoid issues. For that:

- use the hard way by checking the `next` variable type and exclude it if not a number (NaN is a number…).
- use the future-proof way with TypeScript to make sure nothing else than a number to be pushed into the array.

## Remove an item from an array

Use `splice`: it is quick and simple to understand.

```tsx
const removeItem = (anArray, target) => {
  const targetIndex = anArray.findIndex((itemF) => itemF === target);
  anArray.splice(targetIndex, 1);
};
```

## Extract one property from a list of objects

Use `flatMap`:

```tsx
const extractValuesOfProp = (objectArray, prop) =>
  objectArray.flatMap((object) => object[prop]);
```

If `prop`, the `value` is `undefined`.

## Shuffle values of an array

```jsx
const shuffle = (source) => {
  for (let i = source.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [source[i], source[j]] = [source[j], source[i]]; // Swap elements
  }
  return source;
};
```

## More to come…

Save this page as I’ll add more as I practice and work on projects.

Thanks for reading.

Credit: Photo by [Sudharshan TK](https://unsplash.com/@shantk18?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/text-mM9vVJ2oDeI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
.
