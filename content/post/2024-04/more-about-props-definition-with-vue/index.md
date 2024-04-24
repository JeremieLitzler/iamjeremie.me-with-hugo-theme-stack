---
title: "More about props definition with Vue.js"
description: "Declaring props with Vue.js can include more than just the definition of the data passed from the parent to the child component. Let’s see how a more complex validation is declared."
image: images/2024-04-26-hands-ready-to-receive.jpg
imageAlt: "Hands ready to receive"
date: 2024-04-24
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

Thought I wrote on [Vue _props_ feature with TypeScript](../../2024-03/defining-your-props-in-vue-3-using-typescript/index.md), I showcased only a simple example where the props were primitives.

But what about reference types? And what about _props_ validation? And using TypeScript syntax in that context?

{{< blockcontainer jli-notice-note "In the examples below, I use the Composition API only.">}}

{{< /blockcontainer >}}

With JavaScript, it’d look like this:

```jsx
defineProps({
  type: {
    // first you define your validation rule,
    // below, the `validValues` are represented by a string array.
    // see https://vuejs.org/guide/components/props.html#prop-validation
    validator(value) {
      const validValues = [
        "primary",
        "ghost",
        "dashed",
        "link",
        "text",
        "default",
      ];
      // if the value provided exists in the array of valid values,
      // then the prop is accepted.
      return validValues.includes(value);
    },
    // omit the following the prop is required with no default value.
    default() {
      return "default";
    },
  },
});
```

With TypeScript, it’d look like this:

```tsx
import { PropType } from "vue";

defineProps({
  type: {
    // PropType is used to annotate a prop with more
    // advanced types when using runtime props declarations.
    type: String as PropType<
      "primary" | "ghost" | "dashed" | "link" | "text" | "default"
    >,
    default: "default",
    validator: (prop: string) =>
      ["primary", "ghost", "dashed", "link", "text", "default"].includes(prop),
  },
});
```

Credits to:

- **[@webfansplz](https://github.com/webfansplz)** who built the [Vue.js challenges app](https://vuejs-challenges.netlify.app/) and challenged me to find the solution**.**
- [Orbis](https://stackoverflow.com/users/17603999/orbis) on [this Stackoverflow answer](https://stackoverflow.com/a/70565332)
- Photo by [Andrew Moca](https://unsplash.com/@mocaandrew?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/persons-hand-forming-heart-olmY3NkTY_M?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
