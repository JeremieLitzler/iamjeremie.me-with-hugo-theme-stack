---
title: "Functionnal components in Vue"
description: "I discovered functionnal components while training for the level 1 certification of Vue.js. While I might not use it every day as it is very verbose, I’d like to share an example in this article."
image: images/2024-05-01-neon-sign-saying-do-something-great.jpg
imageAlt: "A neon sign displaying “Do Something Great”"
date: 2024-05-01
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

I’ll be 100% honest: functional component is another level. It uses the render function `h()` in Vue.js.

I believe it’s what Vue uses under the hood to convert your SFC (Single File Component) or In-Template code to _Virtual DOM_ nodes.

I’ll share an example I came across [in the Vue.js challenge series](https://vuejs-challenges.netlify.app/questions/21-functional-component/README.html), where I learned to use this functionality.

Do read all the comments in the code below .

```tsx
//Using TypeScrit and Composition API
import { ref, h } from "vue";

// To type the list of items
type User = {
  name: String;
};
// To type the props
type Props = {
  list: User[];
  activeIndex: number;
};
// To type the events ( e.g. emit)
type Events = {
  toogle(index: number): void;
};

/**
 * The challenge > Implement a functional component :
 *   1. Render the list elements (ul/li) with the list data
 *   2. Change the list item text color to red when clicked.
 */
const ListComponent = (props: Props, { emit }) => {
  return h(
    "ul", // create a ul element
    props.list.map((item: User, index) =>
      h(
        // loop the list prop (equivalent to v-for)
        "li", // ... to create an li element for each element
        {
          // ... with the mandatory key attribute
          key: index,
          // ...  with the inline style to set the text to red
          // when the current index is equal to activeIndex prop
          style: index == props.activeIndex ? { color: "red" } : null,
          // ... with the assignment of the node `innerText` value
          innerText: item.name,
          // ... and attaching the onclick handler with the toggle emit
          onClick: () => emit("toggle", index),
        }
      )
    )
  );
};

// This lists the props of the component,
// but doesn't define it. See above type.
ListComponent.props = ["list", "active-index"];
// This lists the events handled by the component,
// but doesn't define it. See above type.
ListComponent.emits = ["toggle"];

const list: User[] = [
  {
    name: "John",
  },
  {
    name: "Doe",
  },
  {
    name: "Smith",
  },
];
const activeIndex = ref(0);

function toggle(index: number) {
  activeIndex.value = index;
}
```

Now, you understand Vue.js a bit more in depth.

As for the template, the usage is unchanged to a regular SFC.

```html
<template>
  <list-component :list="list" :active-index="activeIndex" @toggle="toggle" />
</template>
```

Feel free to [contact me](../../../page/contact-me/index.md) if you see any mistakes and if you simply want to [say thank you](../../../page/sponsor-me/index.md).

Credit: Photo by [Clark Tibbs](https://unsplash.com/@clarktibbs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/do-something-great-neon-sign-oqStl2L5oxI?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
