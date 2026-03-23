---
title: "Map() Function With Python"
description: "Python isn’t JavaScript. I’ll show you with example of the map function in Python."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-03-23
categories:
  - Web Development
tags:
  - Python
---

Last year, I passed my Mid-Level JavaScript certification and, in parallel, I worked on a Python project.

At one point, I had the need to filter a list and I realized I wasn’t as skilled with Python’s list handling as I did with JavaScript.

So here is the start of a series of articles about the methods of handling lists in Python, starting with the `map()` function.

## Python’s `map()` function

The `map()` function in Python applies a given function, or `lambda` , to each item of an iterable (e.g., list) and returns a map object (iterator).

The syntax is the following: `map(function, iterable)`

## Example of primitives

Let’s start simple with an array of primitives:

```python
# Using map() with a lambda function
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # Output: [1, 4, 9, 16, 25]

# Using map() with a defined function
def cube(x):
    return x**3

cubed = list(map(cube, numbers))
print(cubed)  # Output: [1, 8, 27, 64, 125]
```

## Example of objects

With objects, the logic isn’t much more complex:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [
    Person("Alice", 30),
    Person("Bob", 25),
    Person("Charlie", 35)
]

# Extract names using map()
names = list(map(lambda p: p.name, people))
print(names)  # Output: ['Alice', 'Bob', 'Charlie']

# Increase age by 1 year using map()
def increase_age(person):
    person.age += 1
    return person

updated_people = list(map(increase_age, people))
for person in updated_people:
    print(f"{person.name}: {person.age}")
# Output:
# Alice: 31
# Bob: 26
# Charlie: 36
```

## About Performance

Note that in Python, you often need to convert the map object to a list (or another sequence type) to see the results immediately.

If you don’t need all the results at once, you can iterate over the map object directly, which can be more memory-efficient for large datasets.

Let’s look at an example.

### Memory Efficiency with `map()` Iterators

When you use `map()` in Python, it **returns an iterator object**, not a list. This is a key difference from JavaScript’s `map()` which returns a new array immediately.

```python
numbers = range(1, 1000000)  # A large range of numbers
squared_map = map(lambda x: x**2, numbers)

# Process items one at a time without storing the entire result in memory
for squared in squared_map:
    # Process each squared value individually
    if squared % 1000000 == 0:
        print(f"Found milestone: {squared}")
```

In this example, only one squared value exists in memory at any given time, rather than all one million values.

This following would end up being memory-taxing:

```python
numbers = range(1, 1000000)

# Consumes a lot of memory
squared_list = list(map(lambda x: x**2, numbers))
```

Instead, the following is a memory-efficient approach—processes one item at a time:

```python
# Creates only the iterator
squared_map = map(lambda x: x**2, numbers)
```

### A Practical Use Cases

```python
# Processing a large file line by line
with open("large_file.txt", "r") as file:
    # Apply transformation without loading entire file into memory
    processed_lines = map(lambda line: line.strip().upper(), file)

    for line in processed_lines:
        # Process each line individually
        print(line[:10])  # Print first 10 characters of each line
```

## Important Considerations

You need to understand a few important aspects of `map()`:

1. Map objects are single-use iterators. This is expected. Python behavior—`map()` returns a lazy iterator that gets exhausted after one full traversal. The second loop silently produces no output.

   ```python
   numbers = [1, 2, 3, 4, 5]
   squared_map = map(lambda x: x**2, numbers)

   for num in squared_map:
       print(num)  # Prints 1, 4, 9, 16, 25

   # The iterator is now exhausted
   for num in squared_map:
       print(num)  # Nothing will print
   ```

2. You can combine `map` with other iterators for efficient data processing:

   ```python
   from itertools import islice

   numbers = range(10000000)  # Very large range
   squared_map = map(lambda x: x**2, numbers)

   # Get only the first 5 results without processing all items
   first_five = list(islice(squared_map, 5))
   print(first_five)  # Output: [0, 1, 4, 9, 16]
   ```

   This lazy evaluation approach is particularly valuable when working with datasets too large to fit in memory, as it allows you to process data in a streaming fashion.

## Documentation References

Do you want to go further? Here are a few documentation articles to keep as a reference:

1. [https://www.w3schools.com/python/ref_func_map.asp](https://www.w3schools.com/python/ref_func_map.asp)
2. [https://www.digitalocean.com/community/tutorials/python-map-function](https://www.digitalocean.com/community/tutorials/python-map-function)
3. [https://docs.python.org/3/library/functions.html](https://docs.python.org/3/library/functions.html)
4. [https://www.freecodecamp.org/news/python-map-explained-with-examples/](https://www.freecodecamp.org/news/python-map-explained-with-examples/)

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.
