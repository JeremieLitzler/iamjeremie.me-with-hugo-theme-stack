---
title: "Using useLazyAsyncData on a Nuxt app"
description: "In March 2024, I introduced myself with Nuxt while preparation my Vue certification. Here is what I learned about a particular feature."
image: images/2024-05-10-a-black-dog-resting-on-a-bench.jpg
imageAlt: "A black dog resting on a bench."
date: 2024-05-10
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Nuxt
---

This is another scenario that helped me figure out how asynchronous operations works and to implement my code around it.

As I was going through the Nuxt 3 Fundamentals course on [Vueschool.io](http://Vueschool.io) in March 2023, in a lesson, we are introduced to `useAsyncData`. It provides an option to work in a lazy mode.

In the Nuxt docs, I’ve found this example that I didn’t follow all the way, my bad, but it allowed me to understand the mechanism.

## The example

Let’s take this example:

```tsx
import { ref } from "vue";
const nuxtApp = useNuxtApp();

/**
 * Contains a Search property
 */
import type ApiSearchResponse from "@@/types/ApiSearchResponse";
import type Movie from "@@/types/Movie";

const pending = ref(false);
const query = ref("Steel");
const page = ref(1);
const movies = ref<Movie[]>([]);

const search = async () => {
  const { pending: fetchIsPending, data: apiSearchResponse } =
    await useLazyAsyncData<ApiSearchResponse>(
      `/movies-search/${query.value}`,
      (): Promise<ApiSearchResponse> => {
        return $fetch(
          `${import.meta.env.VITE_OMDBAPI_URL}&page=${page.value}&s=${
            query.value
          }`
        );
      },
      {
        default: () => null,
        getCachedData(key) {
          const data = nuxtApp.static.data[key] || nuxtApp.payload.data[key];
          if (!data || data === undefined) {
            return;
          }
          return data;
        },
      }
    );
  pending.value = !fetchIsPending.value;
  movies.value = [...(apiSearchResponse.value?.Search || [])];
};
```

I used it on a movie search page and each time I browsed to it directly, it worked, loading the movies.

If I browser first to the home page for example and then the search page, I would get a blank page…

Why is that?

## The solution

The problem is at the last line of the `search` method.

If you log in the console `fetchIsPending` and `apiSearchResponse`, the first equals to `true` and the second equals to `undefined`.

It makes sense since it is lazy loading the data requested.

When the `fetchIsPending` will turn into a truthy value `apiSearchResponse` will contain an instance of `ApiSearchResponse`.

How do you _watch_ for that change?

Like so:

```tsx
watch(apiSearchResponse, (finalResponse) => {
  movies.value = [...(finalResponse?.Search || [])];
});
```

However, you may have noticed the option `getCachedData` used on `useLazyAsyncData`.

If you stop by adding the `watch` and navigate to another page and come back the search page, it will be blank.

In fact, Nuxt returns the cached response, but the code doesn’t use this cached value.

So you need to add a check:

```tsx
if (!fetchIsPending.value) {
  movies.value = [...(apiSearchResponse.value?.Search || [])];
}
```

There you have it: you handle both first request and cached request and the user is happy to use your application!

Credit: Photo by [Priscilla Du Preez](https://unsplash.com/@priscilladupreez?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/black-pug-puppy-on-brown-wooden-chair-dOnEFhQ7ojs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
