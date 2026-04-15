---
title: "Equivalent of Find() and FindIndex() Functions With Python"
description: "Python isn’t JavaScript.  This time, I’ll show you with example of the equivalents Find and FindIndex function in Python."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-04-03
categories:
  - Web Development
tags:
  - Python
---

Here is a Python cheat sheet for handling lists, specifically focusing on methods equivalent to JavaScript’s `find` and `findIndex`.

The examples I provide handle both primitive values and objects.

## Python Equivalent to JavaScript’s `find()`

In Python, you can use the `next()` function with a generator expression to find the first element in a list that satisfies a condition.

### Primitive Example for `find()` Equivalent

```python
# Find the first odd number in the list
numbers = [2, 4, 6, 7, 8]
result = next(
    (x for x in numbers if x % 2 != 0), # iterator
    None # default value to return
)
print(result)  # Output: 7
```

In this code, `None` is the **default value** passed as the second argument to `next()`.

`next()` takes two arguments:

1. An iterator (here, a generator expression that yields odd numbers)
2. A default value to return **if the iterator is exhausted** (i.e., no items match)

So if the list had no odd numbers—say `[2, 4, 6, 8]`—instead of raising a `StopIteration` exception, `next()` would quietly return `None`, or anything you provide.

With this list `[2, 4, 6, 7, 8]`, an odd number _is_ found (7), so `None` is never used.

{{< blockcontainer jli-notice-warning "">}}

Forgetting this may result in a `StopIteration` exception.

{{< /blockcontainer >}}

### Object Example for `find()` Equivalent

```python
# Find the first object with a specific attribute value
people = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}, {"name": "Charlie", "age": 35}]
result = next((person for person in people if person["age"] > 30), None)
print(result)  # Output: {'name': 'Charlie', 'age': 35}
```

I’d like to mention some important caveats:

- `None` default can be ambiguous. If `None` is a _legitimate_ value in your list, you can’t distinguish “not found” from “found `None`.” A common pattern is to use a sentinel:

  ```python
  _NOT_FOUND = object()
  result = next((p for p in people if p["age"] > 100), _NOT_FOUND)
  if result is _NOT_FOUND:
      print("No match")
  ```

- Missing keys raise `KeyError`. If any `dict` in the list is missing the `"age"` key, you get an error—not a skip. Guard with `.get()`:

  ```python
  result = next((p for p in people if p.get("age", 0) > 30), None)
  ```

- Only the _first_ match is returned. This is by design, but easy to forget. If you need all matches, use a list comprehension instead:

  ```python
  results = [p for p in people if p["age"] > 30]
  ```

## Python Equivalent to JavaScript’s `findIndex`

To find the index of the first element satisfying a condition, use `next()` with `enumerate()`.

### Primitive Example for `findIndex()` Equivalent

```python
# Find the index of the first odd number in the list
numbers = [2, 4, 6, 7, 8]
result = next(
    (
        i for i,
        x in enumerate(numbers) if x % 2 != 0
    ), -1)
print(result)  # Output: 3

```

### **Object Example**

```python
# Find the index of the first object with a specific attribute value
people = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}, {"name": "Charlie", "age": 35}]
result = next((i for i, person in enumerate(people) if person["age"] > 30), -1)
print(result)  # Output: 2
```

## Performance Considerations

### Efficiency of Generator Expressions

Generator expressions (for example `(x for x in numbers if x % 2 != 0)`) are memory-efficient because they produce values on demand rather than creating a new list in memory, as would happen with list comprehensions.

This is particularly beneficial when working with large datasets

For example, using `next((x for x in numbers if x % 2 != 0), None)` avoids creating a temporary list, saving both time and memory.

### Early Exit Behavior

Both `find` and `findIndex` equivalents stop iterating as soon as a match is found.

This makes them efficient for finding the first matching element, as they don’t process the entire list unnecessarily.

### Algorithmic Complexity

The time complexity is `O(n)` in the worst case, where `n` is the length of the list. This occurs when no match is found, requiring iteration through the entire list.

### Impact of Data Volume

For small to medium-sized datasets, the performance difference between generator expressions and other methods (e.g., list comprehensions) may be negligible.

However, as data size increases, generators perform better due to reduced memory usage and better cache utilization.

### Profiling for Bottlenecks

If performance is critical, use profiling tools like `cProfile` or `perf` to identify bottlenecks.

Optimizing these functions may not yield significant gains unless they’re part of a performance-critical loop or process.

### **When to Optimize**

- Optimize only if profiling indicates that these functions are a bottleneck.
- For one-off searches or small datasets, focus on code readability rather than micro-optimizations.
- Use generators for large datasets where memory efficiency is critical.

## Other Caveats

Because Python’s nature, be careful with mutable objects, like dictionaries within lists, and ensure that changes to these objects don’t affect subsequent iterations unexpectedly.

If you frequently need to find elements or indices in large datasets, consider using more advanced data structures, like dictionaries or indexed tables for faster lookups. For example,

- `set` has `O(1)` average complexity because it tests via hash tables. Use it when you only need to check existence, not store associated values.

- `dict` also has `O(1)` average key lookup. Why? Python `dict` are insertion-ordered (since version 3.7+) and highly optimized. For inverse lookups (value→key), maintain a reverse `dict`.

- `collections.defaultdict` has the same `O(1)` lookup but autoinitializes missing keys. It becomes useful for grouping/indexing: `defaultdict(list)` builds an index of items by some key in one pass.

- `sortedcontainers.SortedList` / `SortedDict` is a third-party module, but it’s the gold standard for maintaining a sorted order with `O(log n)` on insert, delete, and lookup. It supports slicing, indexing, and range queries. Much more ergonomic than manually using `bisect`, another third-party module.

So when to pick what?

- Need “is X in here?” → `set`
- Need “what’s the value for X?” → `dict`
- Need “what’s closest to X?” or range queries → `SortedList`
- Need multi-attribute search → build inverted indices with `defaultdict`

The biggest win is usually just switching from `x in my_list` (O[n]) to `x in my_set` (O[1]). Profile before reaching for anything fancier. Let me show you with an example:

```python
import time

data = list(range(1_000_000))
lookup_targets = [999_999, 500_000, 42, -1]  # mix of found/not found

# Slow: O(n) per lookup
start = time.perf_counter()
for target in lookup_targets:
    _ = target in data
print(f"list: {time.perf_counter() - start:.4f}s")

# Fast: O(1) one-time conversion cost, then O(1) per lookup
data_set = set(data)

start = time.perf_counter()
for target in lookup_targets:
    _ = target in data_set
print(f"set:  {time.perf_counter() - start:.8f}s")
```

On my laptop (Intel i3, 20 GB de RAM, disk SSD), I got this output:

```plaintext
list: 0.0184s
set:  0.00000690s
```

The `set` conversion itself is `O(n)`, so it only pays off when you do multiple lookups against the same data. If you’re only checking once, the list scan might be fine. But if you’re checking membership inside a loop, the difference is dramatic:

```python
# Common anti-pattern
blacklist = ["spam", "scam", "phish", ...]  # even 100 items

for msg in millions_of_messages:
    if msg.sender in blacklist:  # O(n) * millions = slow
        flag(msg)

# Fix: one line
blacklist = set(blacklist)
# now each `in` check is O(1)
```

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.
