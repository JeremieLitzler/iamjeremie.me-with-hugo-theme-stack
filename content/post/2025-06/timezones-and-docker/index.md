---
title: "Timezones and Docker"
description: "Depending on your business need, setting the appropriate timezone is critical. Let’s see how to do that."
image: 2025-06-13-4-clocks-for-london-new-york-moscow-and-tokyo-time.jpg
imageAlt: Four clocks for London, New-York, Moscow and Tokyo time
date: 2025-06-13
categories:
  - Software Development
tags:
  - Docker
  - Timezones
---

## The Context

Last year, I worked on a Python application deployed onto Microsoft Azure. This app included a set of recurring tasks that were configured with a [CRON](https://en.wikipedia.org/wiki/Cron) schedule using the _APScheduler_ package.

However, quickly after deployment, I noticed that the task was running 2 hours behind my current time (GMT+2).

Though it wasn’t a big problem at the time, after the hour change on October 27, 2025, it became an issue…

In fact, the application was responsible for sending SMS reminders for an on-call schedule to a team of people. However, following the time change, these notifications about a person’s current status as being “on call” or the end of their session were delayed by one full day.

## The Reason

I had configured the scheduler to execute the tasks at 8:15 a.m. my time, which was equivalent to 6:15 a.m. UTC.

However, when the time changed from summer time to winter time, the task would run at 7:15 AM.

Since the on-call sessions always started at 6:00 PM and ran to 7:59 AM the next day, when the scheduled task would run, it’d send the reminder for the session that had started almost a day before…

## The Fix

A colleague, more experienced on Docker, asked: “Do you tell Docker the time zone when mounting the image?” I didn’t!

I fixed my Dockerfile with the following:

```docker
# Install timezone data first
# It might not be include in your base image
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

# Then set timezone
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

After releasing the new version, the task could be updated to the actual time I needed it to run.

More importantly, I didn’t need to worry about the hour change in the following March.

## Conclusion

Did you know about this caveat?

I didn’t and I’m glad I ran into this situation. However, it was through experience that the situation presented itself, having never, until this project, worked with time zones.

Also, it forced me to write unit tests to make the scheduler work as expected.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/london-new-york-tokyo-and-moscow-clocks-48770/).
