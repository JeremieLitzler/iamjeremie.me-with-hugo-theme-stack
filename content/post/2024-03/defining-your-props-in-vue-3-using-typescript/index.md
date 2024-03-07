---
title: "Defining your props in Vue 3 using TypeScript"
description: "With Vue 3 and TypeScript, defining your props is different and maybe not intuitive if you’re new to TypeScript. Let’s me show you in detail."
image: images/2024-03-08-example-prop.jpg
imageAlt: "Example of a prop definition"
date: 2024-03-08
categories:
  - Web Development
tags:
  - Vue 3
  - TypeScript
  - Tip Of The Day
---

Here is what I learned from having spent quite a bit of time when trying and using `defineProps` with Vue 3 and TypeScript.

As a remind, using the JavaScript, _props_ are defined the following way:

```javascript
const props = defineProps({ id: String });
```

However, using TypeScript, when the _prop_ is required, it becomes:

```tsx
const props = defineProps<{ id: string }>();
```

Notice the _prop_ type isn’t the same: `String` in JavaScript vs. `string` in TypeScript. It’s important to follow that usage so the code works. And if you don’t, ESLint will make sure to tell when writing in TypeScript.

And when you need to set a _prop_ as non-required (implicitly, they’re required…), use the `?` following the _prop_ name:

```tsx
const props = defineProps<{ id?: string }>();
```

Now, it will get more complex when you need to set defaults.

Before, using JavaScript and the Option API, you would write:

```javascript
props: {
  id: {
    type: String,
    default: null
  }
}
```

Or if you prefer the Composition API, it would look this:

```javascript
const { id } = defineProps({
  id: {
    type: String,
    default: null,
  },
});
```

Note: you can destructure the _props_ easily with `{ propName }` as shown above.

Using TypeScript and the composition API, you will need to use `withDefaults` macro **and** create an interface to define the _props_:

```typescript
interface ThreadEditorPageProps {
  title?: string;
  body?: string;
}

const props = withDefaults(defineProps<ThreadEditorPageProps>(), {
  title: "",
  body: "",
});
```

So let’s break down the code:

1. `title` and `body` are string _props_ and they’re optional.
2. then (1) instantiate the _props_ by providing to the `withDefaults` macro the `defineProps` macro typed with the interface and (2) add an object with all the _props_ you need to define a default value for.

In the example, not providing a default value would mean the _props_ would both equal to `undefined` because of the `?`.

With explicit defaults, they will equal to an empty string.

You don’t have to define a default for all _props_ and they don’t need to be flagged as optional to receive a default value.

Finally, when I recommend to use the interface declaration when you have many _props_ and extract this interface to a separate file that you will simply import in your component. To me, that makes the component’s code cleaner.

Do you have questions on the topic? Read [the official documentation](https://vuejs.org/api/sfc-script-setup.html#defineprops-defineemits) or [ask away!](../../../page/contact-me/index.md)
