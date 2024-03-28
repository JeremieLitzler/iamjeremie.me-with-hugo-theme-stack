---
title: "How to create an alias for a Vue component?"
description: "Sometimes, you use third-party libraries who develop useful components. It was the case for me with VeeValidate. But the names of the component may not suit you or your linter. Let’s see how solve either of these issues."
image: images/2024-03-27-code-example-demonstrating-the-concept.jpg
imageAlt: "Code example demonstrating the concept"
date: 2024-03-27
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

I’ve found myself using VeeValidate library in the [Masterclass of VueSchool.io](https://vueschool.io/courses/the-vuejs-3-master-class).

While they taught the course in JavaScript, I decided to complete it in TypeScript. What a challenge!

At one point, we had to import the `Form` and `Field` component of the library the following way using JavaScript and the Options API:

```jsx
import { Form, Field } from "vee-validate";
export default {
  components: {
    VeeForm: Form,
    VeeField: Field,
  }
```

But, how do you do it using TypeScript in the Composition API?

Simple: use the import aliases.

```jsx
import { Form as VeeForm, Field as VeeField } from "vee-validate";
```

While you could have used the same with the Options API, you must use this technique with the Composition API to:

- Follow the style guide rules of Vue
- Name the library component as you wish.

Then, I could use the components in the template:

```tsx
<template>
      <vee-form @submit="register" class="card card-form">
        <h1 class="text-center">Register</h1>
        <div class="form-group push-top">
          <label for="name">Full Name</label>
          <vee-field
            name="name"
            v-model="form.name"
            id="name"
            type="text"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <vee-field
            name="email"
            v-model="form.email"
            id="email"
            type="email"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <vee-field
            name="password"
            v-model="form.password"
            id="password"
            type="password"
            class="form-input"
          />
        </div>
          <label for="username">Username</label>
          <vee-field
            name="username"
            v-model="form.username"
            id="username"
            type="text"
            class="form-input"
          />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-blue btn-block">Register</button>
        </div>
      </vee-form>
</template>
```
