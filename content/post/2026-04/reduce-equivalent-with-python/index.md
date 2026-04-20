---
title: "Reduce() Equivalent With Python"
description: "Python isn’t JavaScript.  This time, I’ll show you an example of the equivalent in Python of Reduce JavaScript's function."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-04-10
categories:
  - Web Development
tags:
  - Python
---

Today, we’ll focus on the equivalent to JavaScript’s `reduce`.

The examples I provide handle both primitive values and objects.

## Python Equivalent to JavaScript’s `reduce()`

### History Around It

In Python, there is a history around `reduce`. **Guido van Rossum, creator of Python, actively discourages `reduce`**—it was removed from built-ins in Python 3 (moved to `functools`). The Pythonic preference is explicit loops or comprehensions for anything nontrivial, since they’re more readable and often faster.

In Python 2, `reduce` was a built-in—you could use it directly like `sum()` or `len()`. In Python 3, Guido intentionally moved it to `functools` to discourage casual use because he felt most `reduce` calls are harder to read than the alternatives.

His argument: “When you read a `reduce`, you have to mentally simulate the loop to understand what it does”. Compare the following syntax:

```python
# reduce — you have to trace through the logic
result = reduce(lambda acc, x: acc if acc > x else x, numbers)

# built-in — intent is immediately clear
result = max(numbers)
```

For cases without a built-in equivalent, with a list of `dict` for example:

```python
# reduce
result = reduce(lambda acc, o: {**acc, o["product"]: acc.get(o["product"], 0) + o["amount"]}, orders, {})

# explicit loop — same logic, easier to follow
result = {}
for o in orders:
    result[o["product"]] = result.get(o["product"], 0) + o["amount"]
```

The loop version is longer but you can read it top-to-bottom without mental gymnastics. It’s also faster (no function call overhead per iteration, no `dict` copy).

So, `reduce` isn’t deprecated or “bad”—it’s just not idiomatic Python the way it’s in JS. Use it for simple, obvious reductions (like chaining operations). For anything where the lambda gets complex, a loop or comprehension is preferred in Python culture.

### Python’s equivalent In Python 3

With primitives:

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum with initial value
total = reduce(lambda acc, x: acc + x, numbers, 0)  # 15

# JS equivalent: [1,2,3,4,5].reduce((acc, x) => acc + x, 0)
```

With objects:

```python
orders = [
    {"product": "A", "amount": 50},
    {"product": "B", "amount": 30},
    {"product": "A", "amount": 20},
]

# Group and sum by product
result = reduce(
    lambda acc, o: {**acc, o["product"]: acc.get(o["product"], 0) + o["amount"]},
    orders,
    {}
)
# {'A': 70, 'B': 30}
```

### Performance considerations

First, note that `{**acc, ...}` creates a new `dict` every iteration, which leads to `O(n²)` complexity for large collections. Mutating the accumulator is faster but less “functional”:

```python
def merge(acc, o):
    acc[o["product"]] = acc.get(o["product"], 0) + o["amount"]
    return acc

result = reduce(merge, orders, {})  # O(n)
```

Next, for numeric reductions, **built-ins like `sum()`, `min()`, `max()`, `math.prod()` are faster** than `reduce`—they’re implemented in C.

Finally, `reduce` has **no short-circuit**. It’ll always process every element. If you need an early exit, use a loop.

## A Few Caveats to Know

Where you handle an **empty iterable** and have **no initial value**, you will get a `TypeError`. Always pass an initial value (the third argument) to be safe.

Unlike JS, **`reduce` doesn’t provide the index or the original array** to the callback. If you need them, use `enumerate` inside a loop instead.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.
