---
title: "Creating a store with Vue 3, Pinia and TypeScript"
description: "State management lets you run a faster application. For a while now, Pinia has replaced Vuex in Vue applications. And with Pinia, it’s time to embrace the Composition API, even within the stores."
image: images/2024-03-01-pinia-image-from.jpg
imageAlt: "Image of the Pinia logo made by VueSchool.io"
date: 2024-03-01
categories:
  - Web Development
tags:
  - TypeScript
  - Tip Of The Day
---

Pinia is the recommended state management plugin in Vue applications.

Though you can use it with the “_Option API_” way, if you are using TypeScript, go for the “_Composition API_” way. Yes, even within the stores, you can use the setup pattern.

With JavaScript, you would have, for example:

```jsx
import { ref } from 'vue';
import { defineStore } from 'pinia';
import useSampleData from '@/composables/useSampleData';

const { categoriesData } = useSampleData();

export const useCategoryStore = defineStore('CategoryStore', {
  state: {
    categories = ref(categoriesData);
  },
  getters: {
    getCategoryById = (categoryId) => {
      const match = this.categories.value.find(
        (category: Category) => category.id === categoryId
      );
      if (match === undefined) return {};

      return match;
    }
  }
});
```

With TypeScript, it becomes:

```tsx
import { ref } from "vue";
import { defineStore } from "pinia";
import useSampleData from "@/composables/useSampleData";
import type Category from "@/types/Category";

const { categoriesData } = useSampleData();

export const useCategoryStore = defineStore("CategoryStore", () => {
  //STATE
  const categories = ref(categoriesData);

  //GETTERS
  const getCategoryById = (categoryId: string | undefined): Category => {
    const match = categories.value.find(
      (category: Category) => category.id === categoryId
    );
    if (match === undefined) return {};

    return match;
  };

  return { categories, getCategoryById };
});
```

The arrow function you see after the name of the store uses the function definition with the setup pattern.

Special thanks to :

- [This thread on GitHub](https://github.com/vuejs/pinia/discussions/983#discussioncomment-2045733) for guiding me to understand the technique.
- [VueSchool.io](https://vueschool.io/) for the [hero image](https://github.com/vueschool/pinia-the-enjoyable-vue-store)
