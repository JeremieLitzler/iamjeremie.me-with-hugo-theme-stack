---
title: "Custom Directives with Vue 3 and TypeScript"
description: "Sometimes, it’s useful to create custom directives with Vue.js. Let’s see how you can do that using TypeScript."
image: images/2024-03-22-example-of-a-custom-directive.png
imageAlt: "Example of a custom directive"
date: 2024-03-22
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue.js
---

I learn every day to use and improve my usage of TypeScript.

Today, I’ll share the case where I converted from JavaScript to TypeScript for a custom directive in Vue 3.

The JavaScript code was the following:

```tsx
const ClickOutsideDirective = {
  mounted(el, binding) {
    el.__clickOutsideHandler__ = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.body.addEventListener("click", el.__clickOutsideHandler__);
  },
  unmounted(el) {
    document.body.removeEventListener("click", el.__clickOutsideHandler__);
  },
};
export default (app) => {
  app.directive("click-outside", ClickOutsideDirective);
};
```

This first thing to deal with is the two arguments of the `mounted` hook and the argument of the `unmounted` hook.

It isn’t well documented [in the official documentation](https://vuejs.org/guide/reusability/custom-directives.html), but if you dig into the Vue.js code (or [find the Stackoverflow threads](https://stackoverflow.com/a/76337333/3910066) 😁), you can find more about the interface.

You need to type the custom directive object with `<Directive<T, V>>` where:

- `T` is the type of the DOM element where the directive is used
- `V` is the type of the value passed to the directive in the template.

So in my case, `T` is `HTMLElement` and `V` is a `Function`.

It took me a moment to understand the type `V`. But I found it by pressing `F12` on `value` in the line `binding.value(event);`.

You can then see the definition of the `DirectiveBinding` interface and `value` has the generic type `V`.

But how do you know the type based on a different use case?

Just look at what you pass as the value to your custom directive. In my example, I’m passing a function:

```html
<!-- closeDropdown is a method defined in the component -->
<a @click.prevent="toggleMenu" v-click-outside="closeDropdown" href="#"
  >Toggle
</a>

<!-- or an anonymous function -->

<a
  @click.prevent="toggleMenu"
  v-click-outside="() => menuOpened = false"
  href="#"
  >Toggle
</a>
```

Next, the best practice of building a custom directive is to define a custom event listener to the DOM element. Therefore you need to define a custom interface (within the custom directive file since you’ll use it only there):

```tsx
interface ClickOutsideDirectiveHTMLElement extends HTMLElement {
  __clickOutsideHandler__: EventListener;
}
```

You have one property typed with `EventListener` that is the name of the custom event listener. You must make sure the interface extends the type `T`, in our case a `HTMLElement`.

Next, you simply type:

- The event argument in the definition of the custom event listener as `Event`.
- The `[event.target](https://developer.mozilla.org/en-US/docs/Web/API/Event/target)` must be casted to a `Node` where you check if the element contains the target.
- The `app` argument on the final export.

The final code is the following:

```tsx
import { App } from "vue";

interface ClickOutsideDirectiveHTMLElement extends HTMLElement {
  __clickOutsideHandler__: EventListener;
}

import { Directive } from "vue";

const ClickOutsideDirective = <
  Directive<ClickOutsideDirectiveHTMLElement, Function>
>{
  mounted(el, binding) {
    el.__clickOutsideHandler__ = (event: Event) => {
      if (!(el === event.target || el.contains(event.target as Node))) {
        binding.value(event);
      }
    };
    document.body.addEventListener("click", el.__clickOutsideHandler__);
  },
  unmounted(el) {
    document.body.removeEventListener("click", el.__clickOutsideHandler__);
  },
};
export default (app: App) => {
  app.directive("click-outside", ClickOutsideDirective);
};
```

Now, you’re ready. Go make your own Vue 3 directives with TypeScript!
