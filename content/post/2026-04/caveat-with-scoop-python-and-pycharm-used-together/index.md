---
title: "Caveat with Scoop, Python and PyCharm Used Together"
description: "Scoop is awesome to install portable software. Python is a nice programming language to learn. PyCharm provides all you need for Python programming. However, I have to share something when you use the three together."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-04-29
categories:
  - Web Development
tags:
  - Python
  - Scoop
  - PyCharm
---

I ran into an issue where I had created a `.venv` through the “Python interpreter“ setting windows and, for some reason, it had picked up a specific version rather than the “current” version.

What happened next?

## The Problem

The “current” version changes as you update the Scoop package, while the specific version could disappear if you run the Scoop cleanup command.

Also, I couldn’t run any tests because PyCharm told me: `No python.exe found at C:\Users\jlitzler\scoop\apps\python312\3.12.7\`

## How Did I Recover From the Situation?

1. I deleted the `.venv` folder
2. I went back to the “Python interpreter“setting windows and added a new interpreter, making sure the path to the Python executable was set to `C:\Users\jlitzler\scoop\apps\python312\current\`.
3. I applied the changes.
4. I ran the command `pip install -r requirements.txt` in the Terminal to reinstall the project’s packages.

And tada, I could run the tests!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.
