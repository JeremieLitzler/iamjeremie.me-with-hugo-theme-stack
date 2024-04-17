---
title: "Reducing Hugo build time by 2 on Netlify"
description: "When you start to have a lot of articles on a Hugo-powered website, the number of images processed can slow down the generation to reach the default timeout. Though you can increase it, this is not enough to avoid overconsuming build minutes on Netlify."
image: images/2024-04-15-still-shot-at-night-in-a-city.jpg
imageAlt: "Still shot at night in a city"
date: 2024-04-15
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Hugo
  - Netlify
---

Suddenly, one day, my blog Netlify build started to fail. The reason: a timeout…

At first, I thought it was caused by the fact that I extracted the theme from a git module to a standalone folder in my repository. I did that because the auto-update feature using a git module broken the build the day before I encountered this other build issue.

I searched and after a few days of resetting the theme changes and validating that the build was working locally, I carefully read the Netlify logs.

On my PC (i3 and 8GB), the Hugo command ran in less than 10s.
For the exact same repository and commit, it ran at 36s on Netlify.

Here is the error I got from Netlify:

```log
8:12:14 PM: hugo v0.123.8-5fed9c591b694f314e5939548e11cc3dcb79a79c+extended linux/amd64 BuildDate=2024-03-07T13:14:42Z VendorInfo=gohugoio
8:12:48 PM: ERROR render of "page" failed: "/opt/build/repo/themes/hugo-theme-stack/layouts/_default/single.html:27:7": execute of template failed: template: _default/single.html:27:7: executing "main" at <partial "article/article.html" .>: error calling partial: partial "article/article.html" timed out after 30s. This is most likely due to infinite recursion. If this is just a slow template, you can try to increase the "timeout" config setting.
8:12:48 PM: Total in 33961 ms
8:12:48 PM: Error: error building site: render: failed to render pages: render of "page" failed: "/opt/build/repo/themes/hugo-theme-stack/layouts/_default/single.html:27:7": execute of template failed: template: _default/single.html:27:7: executing "main" at <partial "article/article.html" .>: error calling partial: partial "article/article.html" timed out after 30s. This is most likely due to infinite recursion. If this is just a slow template, you can try to increase the "timeout" config setting.
```

The build statistics of my blog repository were the following:

```log
8:25:17 PM:                    |  EN
8:25:17 PM: -------------------+-------
8:25:17 PM:   Pages            |  347
8:25:17 PM:   Paginator pages  |   68
8:25:17 PM:   Non-page files   |  499
8:25:17 PM:   Static files     |  113
8:25:17 PM:   Processed images | 1331
8:25:17 PM:   Aliases          |  110
8:25:17 PM:   Cleaned          |    0
8:25:17 PM: Total in 36602 ms
```

Thinking it was related to the theme, I asked CaiJimmy [in this discussion](https://github.com/CaiJimmy/hugo-theme-stack/discussions/975) on his theme repository.

He recommended [using this plugin](https://github.com/cdeleeuwe/netlify-plugin-hugo-cache-resources#readme), because the image processing is what takes the most resources during the build.

The plugin basically caches, on the post-build event, the `resources` folder, if not cached already. This is where Hugo puts the processed images. Then, on subsequent builds, it uses the cache on the pre-build event.

The build time became:

```log
6:01:03 AM:                    |  EN
6:01:03 AM: -------------------+-------
6:01:03 AM:   Pages            |  365
6:01:03 AM:   Paginator pages  |   72
6:01:03 AM:   Non-page files   |  517
6:01:03 AM:   Static files     |  113
6:01:03 AM:   Processed images | 1396
6:01:03 AM:   Aliases          |  114
6:01:03 AM:   Cleaned          |    0
6:01:03 AM: Total in 1072 ms
```

An improvement of 36 times isn’t bad, is it? 😁 When I say _reduce by 2_ the build time in the title, I'm talking about the total time that Netlify logs. The 36 times above is for the Hugo build only.

The important thing to keep in mind: the first build will still be slow so you must have the `timeout` setting that you can set the `config/_default/config.toml` file with:

```toml
# default is 30s
# see https://gohugo.io/getting-started/configuration/#timeout
timeout = "60s"
```

If you do a `Clear cache and deploy site`, you will see a slow build time.

{{< blockcontainer jli-notice-note "You can actually reproduce this locally">}}

If you remove the `public` and `resources` folder that aren't versionned on repository, you will get:

```log
                   |  EN
-------------------+-------
  Pages            |  366
  Paginator pages  |   72
  Non-page files   |  517
  Static files     |  113
  Processed images | 1399
  Aliases          |  114
  Cleaned          |    0

Total in 54072 ms
```

{{< /blockcontainer >}}

Thanks for reading this article.

Credit: Photo by [Marc-Olivier Jodoin](https://unsplash.com/@marcojodoin?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/long-exposure-photography-of-road-and-cars-NqOInJ-ttqM?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
