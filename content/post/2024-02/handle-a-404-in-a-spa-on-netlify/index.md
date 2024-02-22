---
title: "How to handle a 404 in a Single Page Application deployed to Netlify?"
description: "Handling the HTTP 404 errors is important. Showing a page that is user friendly is a must in terms of UX. Without it, you may loose a customer."
image: images/2024-02-14-404-page-displayed-on-laptop.jpg
imageAlt: 404 page displayed on laptop
date: 2024-02-14
categories:
  - Web Development
tags:
  - Netlify
  - Tip Of The Day
relcanonical: https://www.linkedin.com/pulse/how-handle-404-single-page-application-deployed-netlify-litzler-5amnc
---

Out of the box, Single Page Application (SPA) handle what we call _soft 404_. When you deploy to Netlify, we will see a page like this one:

![Netlify 404 _Not Found_ page](images/netlify-404-page.png)

To avoid that, it is as simple as adding a `_redirects` file in the `public` directory of the application and adding the following:

```txt
/* /index.html 200
```

This lets the SPA handle the 404 as a soft 404.

See [this forum thread](https://answers.netlify.com/t/support-guide-i-ve-deployed-my-site-but-i-still-see-page-not-found/125) for more usecases.

Credit: banner image by [Erik Mclean](https://unsplash.com/@introspectivedsgn?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/black-asus-laptop-computer-showing-3-00-sxiSod0tyYQ?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)
