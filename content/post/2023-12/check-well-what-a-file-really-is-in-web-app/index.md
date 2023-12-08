---
title: "Really check what a file is on file upload"
description: "When you build a web application, it is really easy for someone to upload a file that is not what it seems. Let's how to solve this security breach."
#image: images/.jpg
#imageAlt: 
date: 2023-12-08
categories:
  - Web Development
---

Hello everyone,

Do you know the magic number and it is useful for?

You can find it in the first two bytes of a binary file and it tells what file you have in your hands.

It is useful to know about it if you are building web applications where users can upload files.

Did you know that looking up the extension in the file name or the MIME type is not 100% accurate? 
Someone can easily fake a jpeg image when it is an executable in reality…

That’s when the magic number comes in handy!

Here is an implementation example in C# [in this Gist](https://gist.github.com/JeremieLitzler/fb0fb0ec22225947e8bb28817d2ac314)

Who knew about that?
