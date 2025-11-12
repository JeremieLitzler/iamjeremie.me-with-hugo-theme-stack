---
title: "Python - Remove the first item in a list"
description: "You can remove the first item in 3 ways."
image: /quick-tips/images/a-real-python.jpg
imageAlt: A real python
date: 2025-11-10
categories:
  - Web Development
tags:
  - Python
---

To remove the first item in a list in Python, you can use one of these methods:

## Using the `pop()` method

```python
my_list = [1, 2, 3, 4, 5]
first_item = my_list.pop(0)
```

## Using list slicing

```python
my_list = [1, 2, 3, 4, 5]
my_list = my_list[1:]
```

## Using the `del` statement

```python
my_list = [1, 2, 3, 4, 5]
del my_list[0]
```

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Pixabay](https://www.pexels.com/photo/green-snake-45246/).
