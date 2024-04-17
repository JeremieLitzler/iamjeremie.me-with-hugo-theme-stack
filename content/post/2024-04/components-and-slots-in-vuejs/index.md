---
title: "Components and scoped slots in Vue.js"
description: "I took me many examples and a lot of practice to understand slots. Whether it’s simple slots, named slots or scoped slots, you will find that it’s a powerful feature in Vue. Let’s dive into it."
image: images/2024-04-22-a-red-slots-sign-on-the-dark.jpg
imageAlt: "A red slots sign on the dark."
date: 2024-04-22
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

## The challenge

At the end of last month, I attempted to solve a small project while learning Vue.js concepts.

The project required to build a photo slider that used 2 child components in the `App.vue`. The `SwiperSlide` below finds itself in a scoped slot.

The slot resides in the `Swiper` component as you see with `v-slot="{ item }"`.

```html
<!-- App.vue template -->
<template>
  <section>
    <Swiper
      :list="images"
      :index="index"
      v-slot="{ item }"
      @change="index = $event"
    >
      <SwiperSlide v-bind="item" />
    </Swiper>
  </section>
</template>
```

The challenge that I struggled with was to implement the code so:

- the `App.vue` provided the markup (I didn’t have to change `App.vue`)
- the `SwiperSlide` child component would be and didn’t need modification:

```html
<!-- SwiperSlide.vue template -->
<template>
  <img :src="image" :alt="`Image ${title}`" width="400" height="200" />
</template>

<script setup>
  defineProps({
    image: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  });
</script>
```

I couldn’t understand how I had to code the `Swiper` component without touching `App.vue` and `SwiperSlide` component.

I read a few times [this section of the documentation](https://vuejs.org/guide/components/slots.html#scoped-slots) that described the use case.

## How did I make it work

With the following, I completed the task:

```html
<template>
  <section class="container">
    <Transition>
      <ul ref="ulElement">
        <li>
          <slot :item="{ ...currentImage }"></slot>
        </li>
      </ul>
    </Transition>
    <button v-show="showPrev" class="prev-slide" @click="prevImage"><</button>
    <button v-show="showNext" class="next-slide" @click="nextImage">></button>
  </section>
</template>

<script setup>
  import { ref, computed, onMounted } from "vue";
  const props = defineProps({
    list: { type: Array, required: true },
    index: { type: Number, required: true },
  });
  const emits = defineEmits(["@change"]);
  const currentImage = computed(() => props.list[props.index]);
  const currentImageIndex = computed(() => props.index + 1);

  const ulElement = ref(null);
  const translate = ref(null);

  const showPrev = computed(() => currentImageIndex.value > 1);
  const showNext = computed(() => currentImageIndex.value < props.list.length);
  const prevImage = () => {
    emits("@change", props.index - 1);
    translate.value = `-${ulElement.value.offsetWidth}px`;
  };
  const nextImage = () => {
    emits("@change", props.index + 1);
    translate.value = `${ulElement.value.offsetWidth}px`;
  };
</script>
```

First, the _prop_ name on the `<slot>` element is key: it must match what the parent provides to the slot, in our case it is `v-slot="{ item }"`. So the _prop_ must be named `:item`.

Second, the actual image object must be destructured so that the _props_ definition in `SwiperSlide` receive them individually.

If I’m mistaken somewhere, [tell me](../../../page/contact-me/index.md) so I can correct the wording, but after trying it out, I’m pretty sure that I now understand how scoped slots work.

Thanks for reading this article.

Credit: Photo by [Aarón González](https://unsplash.com/@aarez?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/red-and-white-love-neon-light-signage-qyxcwb54yHk?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
