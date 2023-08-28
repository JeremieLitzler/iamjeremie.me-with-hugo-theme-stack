---
title: How to debug a Nodejs project in VSC
description: Debugging is at the heart of software development. Enable it today in your favorite IDE.
date: 2021-02-12
image: '/images/2021-02-12-debugging-in-nodejs-and-vsc.jpg'
imageAlt: A robot connected to a computer on a soccer field.
categories:
  - Web Development
tags:
  - NodeJS
  - Visual Studio Code
  - Configure IDE
---

Debugging is the life of any developper. It allows you to check when your code doesn't behave... because you gave it the wrong instructions.

Let's dive into how to enable it in Visual Studio Code. It will be quick.

## Pre-requisites

- Have a NodeJS-enabled project (for that was [this one](https://github.com/JeremieLitzler/iamjeremie.me)).
- Have Visual Studio Code installed.

## How to enable debugging

It can be found of the official [Visual Studio Code website](https://code.visualstudio.com/docs/nodejs/nodejs-debugging#_javascript-debug-terminal).

### Step 1

![Create a new JavaScript Debug Terminal](/images/debugging-in-nodejs-and-vsc-create-debug-terminal.png)

### Step 2

Run the command to run your application, in my case:

```sh
npm run dev
```

You should see this:

![A running debugger](/images/debugging-in-nodejs-and-vsc-running-debugger.png)

Photo by [C M](https://unsplash.com/@ubahnverleih?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash.
