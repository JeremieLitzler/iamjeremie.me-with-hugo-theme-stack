---
title: "Differences between variable types in JavaScript"
description: "Understanding the following concept will save you a lot of headaches and is considered a key to successfull development."
image: images/2024-03-06-list-of-variable-types.png
imageAlt: "List of variable types"
date: 2024-03-06
categories:
  - Web Development
tags:
  - Tip Of The Day
---

I will take the example of JavaScript in this article, but the same is true in many programming languages, like C#.

Basically, there are two families of variables types: primitives and objects.

Within each, you find the well-known types as list in this top image.

What is important to understand is that you can copy primitives **by value** or you copy object types **by reference**.

## Value types

For example:

```javascript
const greeting = "Hello";
let newGreeting = gretting;

//this assignent doesn't change the value of the variable `gretting`
newGreeting = "Bonjour";
```

Value types store the actual value in memory. And the above code shows that a distinct copy of the value `gretting` is created to initialize `newGreeting`.

**You don't have a link in any way between the two variables.**

## Reference types

When you create an object, it’s stored in memory and the JavaScript uses a reference or _its address in memory_ to find the value.

That reference is used to handling the object.

For example:

```javascript
const greeting = { message: "Hello" };
let newGreeting = gretting;

newGreeting.message = "Bonjour";
```

The last assignment changes the value of the property `gretting.message` because both **variable share the same refence in memory**!

To avoid that, you must create a true copy of `greeting`. That can easily be done with the spread operator (given a flat object only, nested objects require more code...):

```javascript
const greeting = { message: "Hello" };
let newGreeting = { ...greeting };

newGreeting.message = "Bonjour";
```

With `{...greeting}`, we assign a new object and therefore the JavaScript engine creates a new reference to store `newGreeting`.

Consequently, `newGreeting.message = 'Bonjour';` won’t affect the value of `greeting.message`.
