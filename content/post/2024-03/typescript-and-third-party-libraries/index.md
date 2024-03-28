---
title: "TypeScript and third-party libraries"
description: "I want to share this tip about the technique to use when you want to type the parameters of methods that depend on third-party libraries. Let’s dive into it."
image: images/2024-03-29-code-example.png
imageAlt: "Some code example"
date: 2024-03-29
categories:
  - Web Development
tags:
  - TypeScript
  - Tip Of The Day
---

OK, I have to tell it again: TypeScript isn’t easy, but it’s quite useful.

I want to share a tip about using VeeValidate library with TypeScript.

In the [Masterclass of VueSchool.io](https://vueschool.io/courses/the-vuejs-3-master-class), I used the `@invalid-submit` and in the custom function signature, I needed to type the input argument.

How did I find what to set?

I hovered the emit on the VeeForm component and it gave me this:

![Hovered on `@invalid-submit`](images/2024-03-29-code-example.png)

The code of my method then reads as follows:

```tsx
const handleErrors = (
  context: InvalidSubmissionContext<GenericObject> | undefined
) => {
  if (context === undefined) return;

  const { erreurs, résultats } =
    context as InvalidSubmissionContext<GenericObject>;
  console.log("UserRegister>handleErrors>errors", errors);
  console.log("UserRegister>handleErrors>results", results);
};
```

So here you have it: this is how you can type your method that depends on a third-party library.
