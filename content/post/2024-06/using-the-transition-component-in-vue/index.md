---
title: "Using the transition component in Vue"
description: "CSS animation is a cool feature natively available since CSS 3 and beyond. But I never had the real opportunity to play with them. With Vue, it is supported with a special built-in component."
image: images/2024-06-28-night-picture-with-light-effects.jpg
imageAlt: Night picture with light effects.
date: 2024-06-28
categories:
  - Web Development
tags:
  - Vue
  - Animation
---

Until I took the Vue.js certification when it tested my understanding of the concept, I hadn’t understood it fully.

So how the `Transition` and `TransitionGroup` work?

## The Use Cases

Well, if you read [the documentation](https://vuejs.org/guide/built-ins/transition.html#transition) properly (take your time), you can understand easily:

> The transition can be triggered by one of the following:
>
> 1. Conditional rendering via `v-if`
> 2. Conditional display via `v-show`
> 3. Dynamic components toggling via the `<component>` special element
> 4. Changing the special `key` attribute

## What does each use case mean

Use cases 1 and 2 are pretty similar: Let’s take this template, with `v-if`:

```html
<button @click="show = !show">Toggle</button>
<Transition>
  <p v-if="show">hello</p>
</Transition>
```

When `show` changes, Vue toggles the paragraph and runs the transition.

You can replace the `v-if` with `v-show` and you get the exact same thing.

What about use case 3? In the scenario of an image swipe, we could have this:

```html
<Transition>
  <li :key="`image-${currentImage.title}`">
    <!-- this is a Scope slot -->
    <slot :item="{ ...currentImage }"></slot>
  </li>
</Transition>
```

When you move from an image to another, the `currentImage.title` updates and so does the `:key` and it triggers the transition.

The use case 4 was the toughest to understand. It has to do with the `<component>` special element that you can use alongside the Vue router. Here is an example:

```htm
<router-link v-slot="{ Component }">
  <transition name="slide">
    <component :is="Component" :key="$route.path"></component>
  </transition>
</router-link>
```

Basically, the transition will run each time the route path changes.

Also, remember that `<Transition>` only supports a single element or component as its slot content. If the content is a component, the component must also have only one single root element.

So this wouldn’t work:

```html
<button @click="show = !show">Toggle</button>
<Transition>
  <p v-if="show">hello</p>
  <p>the world</p>
</Transition>
```

However, this doesn’t mean you can’t cycle through multiple elements like this example:

```html
<Transition>
  <button v-if="docState === 'saved'">Edit</button>
  <button v-else-if="docState === 'edited'">Save</button>
  <button v-else-if="docState === 'editing'">Cancel</button>
</Transition>
```

## Learn More

See the full code for this example in the [SFC Playground](https://play.vuejs.org/#eNqdk8tu2zAQRX9loI0SoLLcFN2ostEi6BekmwLa0NTYJkKRBDkSYhj+9wxJO3ZegBGu+Lhz7syQ3Bd/nJtNIxZN0QbplSMISKNbdkYNznqCPXhcwwHW3g5QsrTsTGekNYGgt/KBBCEsouimDGLCvrztTFtnGGN4QTg4zbK4ojY4YSDQTuOiKwbhN8pUXm221MDd3D11xfJeK/kIZEHupEagrbfjZssxzAgNs5nALIC2VxNILUJg1IpMxWmRUAY9U6IZ2/3zwgRFyhowYoieQaseq9ElDaTRrkYiVkyVWrPiXNdiAcequuIkPo3fMub5Sg4l9oqSevmXZ22dwR8YoQ74kdsL4Go7ZTbR74HT/KJfJlxleGrG8l4YifqNYVuf251vqOYr4llbXz4C06b75+ns1a3BPsb0KrBy14Aymnerlbby8Vc8cTajG35uzFITpu0t5ufzHQdeH6LBsezEO0eJVbB6pBiVVLPTU6jQEPpKyMj8dnmgkQs+HmQcvVTIQK1hPrv7GQAFt9eO9Bk6fZ8Ub52Qiri8eUo+4dbWD02exh79v/nBP+H2PStnwz/jelJ1geKvk/peHJ4BoRZYow==).

There is more about using transitions, like [Transition Modes](https://vuejs.org/guide/built-ins/transition.html#transition-modes), [Transition Between Components](https://vuejs.org/guide/built-ins/transition.html#transition-between-components) or [Dynamic Transitions](https://vuejs.org/guide/built-ins/transition.html#dynamic-transitions), so feel free to check out the documentation.

Credits: the header image is from [Federico Beccari](https://unsplash.com/@federize?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/time-lapse-photography-of-square-containers-at-night-ahi73ZN5P0Y?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
