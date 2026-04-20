---
title: "Some() and Every() Equivalents With Python"
description: "Python isn’t JavaScript.  This time, I’ll show you an example of the equivalent in Python of Some and Every JavaScript’s functions."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-04-20
categories:
  - Web Development
tags:
  - Python
---

Today, we’ll focus on the equivalent to JavaScript’s `some` and `every`.

The examples I provide handle both primitive values and objects.

## Python Equivalent to JavaScript’s `some()`

Python’s equivalent of JavaScript’s `some()` is `any()`.

```python
# With primitives
nums = [1, 3, 5, 8, 9]
any(n % 2 == 0 for n in nums)  # True (8 is even)

# With objects
users = [{"name": "Alice", "active": False}, {"name": "Bob", "active": True}]
any(u["active"] for u in users)  # True
```

## Python Equivalent to JavaScript’s `every()`

Python’s equivalent of JavaScript’s `every()` is `all()`.

```python
# With primitives
nums = [2, 4, 6, 8]
all(n % 2 == 0 for n in nums)  # True

# With objects
users = [{"name": "Alice", "active": True}, {"name": "Bob", "active": True}]
all(u["active"] for u in users)  # True
```

## Performance considerations

Both short-circuit, just like their JS counterparts:

- `any()` stops at the first truthy result,
- `all()` stops at the first falsy one.

Use generator expressions (parentheses) not list comprehensions (brackets) to get the short-circuit benefit: `all(x > 0 for x in data)` lazily evaluates; `all([x > 0 for x in data])` builds the entire list first, wasting memory and time.

## A Few Caveats to Know

- With empty iterables, remember the following: `any([])` returns `False`, `all([])` returns `True`. This matches JavaScript behavior but catches people off guard — `all([])` being `True` is a vacuous truth.
- No index access in Python, unlike JavaScript counterparts. If you need the index, use `enumerate()` like we have seen for many previous articles on this series: `any(val > 10 for i, val in enumerate(data))`.
- No built-in predicate parameter exists so you always need a generator expression.
- Truthiness differences between Python and JavaScript exist as the two programming languages use different falsy values. `0`, `""`, `None`, `[]`, `{}` are all falsy in Python. In JS, `[]` and `{}` are truthy. This matters if you’re doing bare `any(items)` without an explicit condition.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.
