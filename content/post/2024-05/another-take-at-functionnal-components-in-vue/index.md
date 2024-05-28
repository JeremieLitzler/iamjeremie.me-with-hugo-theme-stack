---
title: "Another take at Functional components in Vue"
description: "I wrote an article introducing the functional components a while ago and I later discovered that you write it another way."
image: images/2024-05-17-a-kid-building-something-with-lego-blocks.jpg
imageAlt: "A kid building something with LEGO blocks."
date: 2024-05-31
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

## Introduction

Here I’ll show you how to build a functional component using `defineComponent`.

I’ll share an example I came across [in the Vue.js challenge series](https://vuejs-challenges.netlify.app/questions/218-h-render-function/README.html), where I learned to use this functionality.

Do read all the comments in the code below.

## Code example

```tsx
// ./MyButton
// Using TypeScrit
import { h } from "vue";
import { defineComponent } from "vue";

const MyButton = defineComponent(
  // this is the setup method where destructure the context
  // to extract emit and slots
  (props, { emit, slots }) => {
    // this arrow function is similar to the `return {}`
    // that you use in the setup function in a SFC component
    return () => {
      // call the render function
      return h(
        // add a button element
        "button",
        {
          // with the disabled attribute assigned
          // to the disabled prop value
          disabled: props.disabled,
          // bind a click event to custom-click emit
          onClick: () => emit("custom-click"),
        },
        // this pass on the slot content to the element
        slots.default?.()
      );
    };
  },
  // extra options, e.g. declare props and emits
  // like the props, component name and emits
  {
    // component name
    name: "MyButton",
    // definition of the props
    props: {
      disabled: { type: Boolean, default: false },
    },
    // definition of the emits
    emits: ["custom-click"],
  }
);
export default MyButton;
```

Now, you understand Vue.js a bit more in depth.

As for the template, the usage remains unchanged to a regular SFC.

```html
<script setup lang="ts">
  import { ref } from "vue";
  import MyButton from "./MyButton";

  const disabled = ref(false);
  const onClick = () => {
    disabled.value = !disabled.value;
  };
</script>

<template>
  <!-- 
	  :disabled is the same as :disabled="disabled" since Vue 3.4+
	  see https://vuejs.org/guide/essentials/template-syntax.html#same-name-shorthand
  -->
  <MyButton :disabled @custom-click="onClick"> my button </MyButton>
</template>
```

Feel free to contact me if you see any mistakes and if you simply want to [say thank you](../../../page/sponsor-me/index.md).

Credit: Photo by [Kelly Sikkema](https://unsplash.com/@kellysikkema?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/toddlers-playing-building-block-toys-JRVxgAkzIsM?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
