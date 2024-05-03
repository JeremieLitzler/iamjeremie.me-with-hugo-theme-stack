---
title: "How update state on interval in Vue"
description: "As I learnt about Vue.js and coding applications with the framework, I learnt about updating on intervals the components I dealt with. Let’s see how it works with a detailed example."
image: images/2024-05-03-wood-hourglass.jpg
imageAlt: "A wooden hourglass"
date: 2024-05-03
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Vue
---

## The description

A simple, yet complete, example of the interval in action is a countdown clock. You could also apply the following to a web clock.

Let’s say you want to create a New Year’s countdown app.

```html
<template>
  <div class="app-wrapper">
    <div class="countdown-box">
      <main class="flex justify-center">
        <CountdownSegment data-test="days" label="days" :number="daysLeft" />
        <CountdownSegment data-test="hours" label="hours" :number="hoursLeft" />
        <CountdownSegment
          data-test="minutes"
          label="minutes"
          :number="minutesLeft"
        />
        <CountdownSegment
          data-test="seconds"
          label="seconds"
          :number="secondsLeft"
        />
      </main>
    </div>
  </div>
</template>
```

It should meet the following requirements:

- Use the **`CountdownSegment`** component to display days, hours, minutes, and seconds until 0:00:00 a.m. of January 1st next year.

  ```html
  <template>
    <div class="segment">
      <div class="number-wrapper">
        <span class="number">0</span>
      </div>
      <span class="block pt-2 label">{{ label }}</span>
    </div>
  </template>
  ```

- Each number should update appropriately every second.
- You should update the minutes, seconds, etc. as they tick by.
- The **`CountdownSegment`** component must accept a **`number`** prop and use it to display how much x is left (x being days, minutes, etc.).

So let’s dissect the step to get each value: `daysLeft`, `hoursLeft`, `minutesLeft` and `secondsLeft`.

## What is the time now

Using the Date API, simply use the constructor `new Date()`. It gives you the time _now_.

## Getting the next new year’s date and time

If you’re new to JavaScript, I need to warn you: JavaScript’s `Date` object tracks time in UTC internally, but typically accepts input and produces output in the local time of the computer it’s running on.

When you use the various functions of the `Date` object, the computer applies the local time zone to the internal representation. This is the case for `new Date()` constructor that gives you the date and time on your time zone.

If you initialize, like I did, the next new year’s value with the `new Date(year, monthIndex, day)` constructor, be aware of two caveats:

1. You will have time difference if you aren’t in GMT+1 time zone (London time) since it provides GMT+1 time (UTC is GMT time).
2. Also, as you can read in the `new Date(year, monthIndex, day)`, the second argument is an index and it’s zero-based. So January isn’t _month 1_ but _month 0_.

So, what is the JavaScript code for the new year’s date and correct time for your time zone?

Use `const nextNewYear = new Date('2025-01-01')` constructor as this will work just like the `new Date()` and you’re sure that you aren’t missing or having extra hours depending on your time zone.

## Getting the computed variables

The source will be a `ref` (the now time).

```tsx
const rightNow = ref(new Date());
```

Next, we want to get the time left in seconds until next new year:

```tsx
const ONE_SECOND = 1000;
const timeLeftSeconds = computed(
  () => (nextNewYear.getTime() - rightNow.value.getTime()) / ONE_SECOND
);
```

Then, we can start calculating `daysLeft`, `hoursLeft`, `minutesLeft` and `secondsLeft`:

```tsx
//we extract the rounded number of day from the `timeLeftSeconds`
const daysLeft = computed(() =>
  Math.floor(timeLeftSeconds.value / oneDayInSeconds)
);
//and we calculate the exact number of seconds from the number of days...
const daysLeftSeconds = computed(() => daysLeft.value * oneDayInSeconds);

//so forth with the hours...
const hoursLeft = computed(() =>
  Math.floor((timeLeftSeconds.value - daysLeftSeconds.value) / oneHourInSeconds)
);
const hoursLeftSeconds = computed(() => hoursLeft.value * oneHourInSeconds);
//... and with the minutes...
const minutesLeft = computed(() =>
  Math.floor(
    (timeLeftSeconds.value - daysLeftSeconds.value - hoursLeftSeconds.value) /
      oneMinInSeconds
  )
);
const minutesLeftSeconds = computed(() => minutesLeft.value * oneMinInSeconds);
//... and finally the seconds...
const secondsLeft = computed(() =>
  Math.floor(
    timeLeftSeconds.value -
      daysLeftSeconds.value -
      hoursLeftSeconds.value -
      minutesLeftSeconds.value
  )
);
```

## Animate the countdown

If you print the `computed` in the template, you will get the exact countdown at the moment Vue compiles and loads the application. But the numbers don’t update.

How do you make sure all values updates correctly as time come close to the new year date?

Let’s recall the need: update the minutes, seconds, etc. as they tick by. How do you perform an operation on a time _interval_ with JavaScript?

Yes, I hinted the solution: with `setInterval`.

Let’s do that with the following code:

```tsx
setInterval(() => {
  console.log("one second passed...");

  rightNow.value = new Date();
}, 1000);
```

We reassign `rightNow` to the current date using the constructor on 1000 milliseconds basis.

It’s important to note that a good practice is to assign the return value of `setInterval` to a variable. It holds the identifier of the interval that you use as the argument `clearInterval(id)` to stop the interval.

But, where do you put it when coding a Vue application?

Calling `clearInterval()` in the script setup will stop the interval and the countdown won’t animate...

With Vue, there is a hook that is called on the destruction of the component: `onUnmounted`.

The following is the Vue 3 syntax within a script setup:

```tsx
<script setup>
import { ref, onUnmounted } from 'vue';

const rightNow = ref(new Date());
const interval = setInterval(() => {
  console.log('one second passed...');
  rightNow.value = new Date();
}, 1000);
onUnmounted(() => {
  console.log('cleared interval', interval);
  clearInterval(interval);
});
```

There you have it: a countdown that animates every second until a give date.

When the countdown reach zero on all the variables, simply call the `clearInterval`... You don’t see the countdown going backward then...

Do you know how to do that?

```tsx
watchEffect(() => {
  //make sure to watch the time left up to a second or more...
  //watch to 0 or more will give a broken countdown.
  const someTimeLeft = timeLeftSeconds.value > 1;
  if (!someTimeLeft) {
    clearInterval(interval);
  }
});
```

Credit: Photo by [Kenny Eliason](https://unsplash.com/@neonbrand?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/clear-hour-glass-with-brown-frame-KYxXMTpTzek?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
