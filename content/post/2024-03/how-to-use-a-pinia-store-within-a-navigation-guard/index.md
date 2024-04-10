---
title: "How to use a Pinia store within a navigation guard"
description: "Navigation guards allow you to execute some logic at certain stages of the navigation. To use Pinia on those guards requires a little trick of implementation. Let’s dive into it."
image: images/2024-03-01-pinia-image-from.jpg
imageAlt: "Image of the Pinia logo made by VueSchool.io"
date: 2024-03-04
categories:
  - Web Development
tags:
  - Pinia
  - Tip Of The Day
---

If you are building a medium-sized application, you will end up using navigation guards to browse the different pages of your application.

The basic use case is when you want to check an element exists before loading its details (for example on `beforeEnter`).

Now, if you are building the application with Vue 3 and Pinia, you will do this by querying a store.

However, the application doesn’t load Pinia until the `mount` call and you load the router before that…

Therefore, Pinia will throw an error _“getActivePinia()” was called but there was no active Pinia. Are you trying to use a store before calling “app.use(pinia)”? See https://pinia.vuejs.org/core-concepts/outside-component-usage.html for help. This will fail in production._

What is the solution? I followed the steps of [this Stackoverflow answer](https://stackoverflow.com/a/70714477).

1. Create a `pinia.ts` file to create the Pinia instance. Place it in the same location that you put your stores.
2. Import it and call `use` on the application instance in `main.ts`
3. Import it in `src/router/index.ts` and provide it to your store instance: `const store = useStore( pinia )`

The signature of the store `useStory` doesn’t need to change. Providing the `pinia` instance to the `useStore()` is sufficient to make it work.

If you want to learn Pinia, [VueSchool.io](https://vueschool.io/courses/) has [a great course](https://vueschool.io/courses/pinia-the-enjoyable-vue-store) on the subject! I recommend it.

Credit: image from VueSchool's course on Pinia.
