---
title: "Use the proper type when typing a prop in Vue.js"
description: "TypeScript enables you to learn every line of code you write. Here is another tip about typing adequately the props with Vue 3."
image: images/2024-02-28-eslint-typescript-error-details.jpg
imageAlt: "The details of a TypeScript error detected by ESLint"
date: 2024-02-28
categories:
  - Web Development
tags:
  - TypeScript
  - Tip Of The Day
---

Once again, I didn’t take me long to understand what I was missing, as ESLint errors are explicit.

I encountered this when I was coding [the lesson 35](https://vueschool.io/lessons/introducing-categories-collections-of-forums) of the masterclass about Vue.js provided by the awesome team of VueSchool.io.

When you type a prop, don’t use `String` but use `string` primitive type.

The first is a wrapper object, but to make ESLint happy, you must use the primitive.

For example, you should avoid this declaration:

```typescript
const props = defineProps<{ id?: String; edit?: boolean }>();

//eslint will complain on `props.id`
if (props.id) {
  return getUserById(props.id);
}
```

The same goes for:

- `number` and `Number`.
- `boolean` and `Boolean`.
