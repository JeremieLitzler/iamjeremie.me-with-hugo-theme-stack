---
title: "Caveat about destructuring Vue props"
description: "Destructuring objects in JavaScript is a really cool feature. Using it along with Vue can, however, take on a spin… Let’s dive into one caveat on the topic."
image: images/2024-04-03-a-box-of-lego-blocks.jpg
imageAlt: "A box of LEGO blocks"
date: 2024-04-03
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

I will explain my use case: I had a `PostList` component on a forum application. I used this component is two places:

- one needed the posts to be ordered in the ascending order,
- the other needed the contrary.

While working on that, I declared my _props_ this way:

```tsx
interface PostListProps {
  posts: Post[];
  orderBy: OrderByDirection;
}

const { posts, orderBy } = withDefaults(defineProps<PostListProps>(), {
  orderBy: OrderByDirection.Asc,
});
```

Then, I used a computed to order the posts as needed:

```tsx
const orderedPosts = computed(() => {
  if (orderBy === OrderByDirection.Asc) {
    return posts;
  }
  return [...posts].sort((first, next) =>
    first.publishedAt! < next.publishedAt! ? 1 : -1
  );
});
```

When I went to test this code, adding a new post worked but it didn’t show in the list.

Using Vue DevTools, I saw the Pinia state updating and the parent component of `PostList` component did provide the full list…

Why didn’t the new post appear?

Destructuring the _props_ object broke the reactivity and `computed` requires a reactive dependency!

So the valid code became:

```tsx
const props = withDefaults(defineProps<PostListProps>(), {
  orderBy: OrderByDirection.Asc,
});
const orderedPosts = computed(() => {
  if (props.orderBy === OrderByDirection.Asc) {
    return props.posts;
  }
  return [...props.posts].sort((first, next) =>
    first.publishedAt! < next.publishedAt! ? 1 : -1
  );
});
```

## Using `toRefs`

If you insist to destructure the _props_, make sure to _reactive_ them.

For that, Vue provides a nice utility: `toRefs`.

The code would like that:

```tsx
import { toRefs } from "vue";

const props = withDefaults(defineProps<PostListProps>(), {
  orderBy: OrderByDirection.Asc,
});

// `posts` and `orderBy` are now reactive.
const { posts, orderBy } = toRefs(props);

const orderedPosts = computed(() => {
  if (orderBy === OrderByDirection.Asc) {
    return posts;
  }
  return [...posts].sort((first, next) =>
    first.publishedAt! < next.publishedAt! ? 1 : -1
  );
});
```

## Conclusion

Destructuring is great, but with Vue, use it carefully, especially with `computed` 🙂. Thank you, `toRefs`!

Credit: Photo by [Scott McNiel](https://www.pexels.com/photo/lego-blocks-on-white-plastic-container-7662317/) on [Pexels](https://www.pexels.com/).
