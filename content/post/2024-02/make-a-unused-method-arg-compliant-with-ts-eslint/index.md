---
title: "Making a unused method argument compliant with TypeScript and ESLint"
description: "I continue learning about TypeScript and ESLint checking. Today I wanted to share about unused argument in a method."
image: images/2024-02-16-typescript-code-sample.png
imageAlt: TypeScript code sample
date: 2024-02-16
categories:
  - Web Development
tags:
  - TypeScript
  - Tip Of The Day
relcanonical: https://www.linkedin.com/pulse/making-unused-method-argument-compliant-typescript-eslint-litzler-uiktf/
---

I am pretty new to TypeScript, as I am going through the [VueSchool curiculum](https://vueschool.io/courses).

I like what TypeScript brings to the code and how it makes you think more how to write your code.

As I progressed, I wondered about something: how would you solve the TypeScript linting error when an argument in a method is not used but is mandatory ?

Fun fact, I quickly came across this usecase.

![Code example failing to comply with ESLint and TypeScript](images/code-example.png)

In this case, I had no choice. The navigation guard `beforeEnter` requires the second argument to be `from`, even if I don't use it...

How did I fix it? Simple: listen to what ESLint has to say. Sometimes, it provides a quick fix.

In my case, it suggested me to mark the unused argument with a underscore and tada, ESLint became happy.
