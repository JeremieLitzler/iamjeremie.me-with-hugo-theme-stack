---
title: "Filter() Function With Python"
description: "Python isn’t JavaScript. I’ll show you with example of the filter function in Python."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-03-23
categories:
  - Web Development
tags:
  - Python
---

Last week, we started a new series to explore functions, like [`map()`](../map-function-with-python/index.md) to manipulate arrays or lists in Python.

Today, let’s look at the `filter()` function with some examples.

## Python `filter()` Function Cheatsheet

The `filter()` function in Python creates an iterator from elements of an iterable for which a function returns true. It’s equivalent to JavaScript’s `array.filter()` method.

## Basic Syntax

```python
filter(function, iterable)

```

The function takes two parameters:

- `function`: A function, often called `lambda`, that tests if elements of an iterable return true or false
- `iterable`: The iterable to be filtered

## Filtering Primitive Values

### Filtering Numbers

```python
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # Output: [2, 4, 6]

```

You can also use a named function instead of lambda for more clarity:

```python
def is_even(num):
    return num % 2 == 0

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even_numbers = list(filter(is_even, numbers))
print(even_numbers)  # Output: [2, 4, 6, 8]

```

### Filtering Strings

```python
text = "HeLLo ReadER!"
capital_letters = list(filter(lambda letter: letter.isupper(), text))
print(capital_letters)  # Output: ['H', 'L', 'L', 'R', 'E', 'R']

```

Strings are iterable in Python, so `filter()` (like `map()`, `for` loops, etc.) automatically iterates over them, character by character.

The code:

1. `filter()` goes through each character of `"HeLLo ReadER!"` one by one
2. The lambda keeps only characters where `.isupper()` returns `True`
3. `list()` collects the results → `['H', 'L', 'L', 'R', 'E', 'R']`

No explicit splitting needed!

### Filtering Falsy Values

```python
mixed_values = [0, 1, [], 4, 5, "", None, 8]
truthy_values = list(filter(None, mixed_values))
print(truthy_values)  # Output: [1, 4, 5, 8]
```

When you pass `None` as the filter function, Python uses each element’s own truthiness to decide whether to keep it.

So it’s equivalent to:

```python
filter(lambda x: bool(x), mixed_values)
```

The falsy values that get dropped:

- `0` is falsy
- `[]` is an empty list, so falsy
- `""` is empty string, so falsy
- `None` is falsy

The rest (`1, 4, 5, 8`) are truthy, so we keep them.

Finally, `filter(None, iterable)` is essentially a quick way to strip all falsy values from a list.

## Filtering Objects

### Filtering Dictionaries

```python
grades = {'stu1': 'A', 'stu2': 'B', 'stu3': 'A', 'stu4': 'C'}

def has_a_grade(pair):
    key, value = pair # Destructuring pair into two variables
    return value == 'A'

a_students = dict(filter(has_a_grade, grades.items()))
print(a_students)  # Output: {'stu1': 'A', 'stu3': 'A'}
```

`grades.items()` returns key-value pairs as tuples: `[(’stu1', 'A'), (’stu2', 'B'), ...]`

`filter()` passes each tuple to `has_a_grade`, which:

1. Destructures the tuple into `key, value` — e.g. `('stu1', 'A')` into `key='stu1'’ and `value='A’’
2. Returns `True` only if `value == 'A'`

The key part to understand is `grades.items()` — without it you'd just be iterating over keys. `.items()` is what gives you the pairs to filter on values.

### Filtering List of Dictionaries

In the following, the filtered results are a **whole dict objects**, not just keys or values — so you get the full creature info, not just the matched field.

```python
creatures = [
    {"name": "sammy", "species": "shark", "tank": 11, "type": "fish"},
    {"name": "ashley", "species": "crab", "tank": 25, "type": "shellfish"},
    {"name": "jo", "species": "guppy", "tank": 18, "type": "fish"},
    {"name": "jackie", "species": "lobster", "tank": 21, "type": "shellfish"},
    {"name": "charlie", "species": "clownfish", "tank": 12, "type": "fish"}
]

# Filter to find only fish
fish_only = list(filter(lambda x: x["type"] == "fish", creatures))
print(fish_only)
# Output: [{"name": "sammy", "species": "shark", "tank": 11, "type": "fish"},
#          {"name": "jo", "species": "guppy", "tank": 18, "type": "fish"},
#          {"name": "charlie", "species": "clownfish", "tank": 12, "type": "fish"}]
```

### More Complex Filtering with Custom Function

```python
def filter_by_search(creatures, search_string):
    def iterator_func(creature):
        for value in creature.values():
            if str(search_string) in str(value):
                return True
        return False
    return filter(iterator_func, creatures)

# Find creatures with '1' in any value
results = list(filter_by_search(creatures, '1'))
print(results)
# Output will include creatures with '1' in any field
```

Remember that `filter()` returns an iterator, so you need to convert it to a list, tuple, or other collection type to see all results at once.

The key difference is the filter function now searches **across all values** of each dict, not just one specific field.

`iterator_func` loops through every value in a creature dict (`name, species, tank, type`) and returns `True` as soon as it finds a match — short-circuiting the rest.

For search string `’1'’, it would match:

- `sammy` of tank `11`
- `jo` of tank `18` because `'1'` is in `'18'`)
- `jackie` of tank ’21` because (`'1'`is in`’21'’)
- `charlie` of tank `12` because (`'1'` is in `'12'`)

`str(value)` is the important detail — it converts ints (like tank numbers) to strings so `in` comparison works uniformly on everything.

Compared to the previous example, which was `x["type"] == "fish"` (exact match on one field), this is a **partial string search across all fields** — much more flexible, like a search bar.

## Performance Considerations

There are several performance considerations when using Python’s `filter()` function, similar to `map()`.

### Efficiency Benefits

The `filter()` function offers some performance advantages:

- It’s implemented in C and highly optimized, making its internal loop potentially more efficient than regular Python loops in terms of execution time ([^2]).
- It returns an iterator (a `filter` object) that yields values on demand, promoting lazy evaluation, which is more memory efficient than creating entire new collections at once. It’s particularly beneficial when working with larger datasets, as it doesn’t create a new list in memory but instead holds a reference to the original iterable, the function, and an index (see [^1]).

### Performance Comparison with Generators

However, recent benchmarks suggest that generator expressions might be outperforming `filter()`, but I haven’t gone into verifying the sources.

## Caveats When Using `filter()`

When using `filter()`, keep these caveats in mind:

- The `filter()` function returns an iterator, not a list. You need to convert it to a list, tuple, or other collection type to see all the results at once. This will come with lower performance, since you will loop through the iterator once and probably a second time for the list where it’s used.

  ```python
  # Recommend syntax to convert a filter() iterator to a list
  numbers = [1, 2, 3, 4, 5, 6]
  even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
  ```

- Similar to `map()`, the returned iterator is consumed once you iterate through it. If you need to use the filtered results multiple times, convert it to a list first.

- In Python 2, `filter()` returned a list, but in Python 3 it returns an iterator, which might cause compatibility issues in older code [^2].

- For complex filtering operations, defining a regular function might be more readable than using lambda functions with `filter()` [^1].

For optimal performance, choose between `filter()` and generator expressions based on your specific use case and Python version, with generator expressions potentially being the better choice in newer Python versions.

We’ll look into generators in a future article.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.

[^1]: [https://www.digitalocean.com/community/tutorials/how-to-use-the-python-filter-function](https://www.digitalocean.com/community/tutorials/how-to-use-the-python-filter-function)

[^2]: [https://realpython.com/python-filter-function/](https://realpython.com/python-filter-function/)
