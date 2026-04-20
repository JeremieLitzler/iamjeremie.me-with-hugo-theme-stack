---
title: "Sort() Equivalent With Python"
description: "Python isn’t JavaScript. I’ll show you with example of the equivalent in Python of Sort JavaScript's function."
image: /images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2026-04-15
categories:
  - Web Development
tags:
  - Python
---

Today, we’ll focus on the equivalent to JavaScript’s `sort`.

The examples I provide handle both primitive values and objects.

## Python Equivalent to JavaScript’s `sort()`

Python’s equivalents are `list.sort()` (in-place) and `sorted()` (returns new list).

## Numeric Primitive Sorting

Unlike JS (which sorts as strings by default — `[1, 2, 10].sort()` > `[1, 10, 2]`), Python sorts numerically out of the box.

```python
nums = [3, 1, 4, 1, 5, 10, 2, 6]

# in-place, mutates original
nums.sort()
# Output [1, 1, 2, 3, 4, 5, 6, 10]

# returns new list, original untouched
sorted(nums)
# descending
sorted(nums, reverse=True)
```

## String Primitive

### Default behavior

Python sorts strings by Unicode code point, which produces surprising results:

```python
words = ["banana", "Apple", "cherry", "apple"]
sorted(words)
# ['Apple', 'apple', 'banana', 'cherry']
```

All uppercase letters come before all lowercase in the Unicode table (A-Z = 65-90, a-z = 97-122). So the order is logic.

With strings containing accents with default sorting (e.g., no second argument), we obtain the following:

```python
fruits = ["éclair", "apple", "banana", "zebra"]
sorted(fruits)
# ['apple', 'banana', 'zebra', 'éclair']
```

The “é” (which is `U+00E9 = 233` in Unicode table) sorts **AFTER** “z” (which is 122 in Unicode table) leading to accented chars being dumped at the end.

### Case-insensitive

To solve the previous examples in order to obtain a result that is more consistent with what one would expect, we need to provide a second parameter to `sorted`.

With upper letters:

```python
sorted(words, key=str.lower)
# ['Apple', 'apple', 'banana', 'cherry']
```

You may wonder: why `Apple` remains first in the original list `["banana", "Apple", "cherry", "apple"]`? `key=str.lower` transforms the words to `["banana", "apple", "cherry", "apple"]`, the sorting doesn’t change the order of the apple words.

If you had `["banana", "apple", "cherry", "Apple"]`, the lowercase apple word would come first.

If you need to sort lowercase first on ties, you need to add a secondary key that breaks ties in favor of lowercase:

```python
words = ["banana", "Apple", "cherry", "apple"]

print(sorted(words, key=lambda s: (s.lower(), s.swapcase())))
# ['apple', 'Apple', 'banana', 'cherry']
```

How does the `swapcase` trick work?

- With “apple”, you get `key ("apple", "APPLE")`
- With “Apple”, you get `key ("apple", "aPPLE")`

If the primary keys tie, then Python compares the secondary value of the key: `"APPLE" < "aPPLE"` because `'A' (65) < 'a' (97)"`. So `apple` wins.

A more explicit yet less flexible approach would be the following:

```python
sorted(words, key=lambda s: (s.lower(), not s.islower()))
# ('apple', False) < ('apple', True)  > lowercase wins
```

Cleaner intent, but only distinguishes “fully lowercase” vs. “not”. The swap case version handles arbitrary mixed case (e.g., “aPpLe” vs. “ApPlE”) consistently.

What about special letters that we find in German, Greek or Turkish, to name a few?

```python
sorted(words, key=str.casefold)
```

`str.casefold` handles better full Unicode (handles ß, Greek sigma, Turkish dotted I, etc.)

`casefold()` is more aggressive than `lower()` — designed specifically for caseless comparison across scripts.

### Accent-aware (locale)

Neither trick above is locale-aware — still pure code-point comparison on the tie-break. If you’re also dealing with accents, combine with normalization:

```python
import locale
locale.setlocale(locale.LC_COLLATE, "fr_FR.UTF-8")

fruits = ["éclair", "apple", "banana", "zebra", "Être"]
sorted(fruits, key=locale.strxfrm)
# ['apple', 'banana', 'éclair', 'Être', 'zebra']
```

`é` now sorts near `e` as a French speaker expects.

### Accent-aware (no locale dependency)

Locales are process-global and depend on what the OS has installed. It’s fragile on servers/containers. `pyuco` or the stdlib `unicodedata` approach is more portable:

```python
import unicodedata

def strip_accents(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()

sorted(fruits, key=lambda s: (strip_accents(s).lower(), s))
# Output = ["éclair", "apple", "banana", "zebra", "Être"]
```

The above strips accents for primary sort, keeps original for stable tie-breaking.

For proper Unicode Collation Algorithm (UCA) support, use the `pyuca` library (`pip install pyuca`). it implements the actual Unicode standard.

### Summary for String Lists

If we summarize:

- Code-point sort isn’t alphabetical. For ex: “Z” < “a” < “é”. Almost never what users want for display.
- `locale.setlocale` is process-global and not thread-safe — setting it affects the entire program. You need to avoid it on web servers with concurrent requests; use `pyuca` instead.
- Locale availability varies: `fr_FR.UTF-8` may not exist on minimal Docker images. Generate it (`locale-gen`) or install `locales` package.
- Normalization matters: "café" can be encoded two ways — `café` (single `é`, NFC) or `cafe` + combining accent (NFD). They compare as unequal. Make sure to normalize first: `unicodedata.normalize("NFC", s)`.
- German ß, Turkish I, Greek final sigma have locale-specific rules that simple `.lower()` gets wrong. `casefold()` handles most; full correctness needs ICU (`pip install PyICU`).
- Numbers in strings don't sort "naturally". For ex, `["file2", "file10"]` > `[’file10', ’file2']`. Use the `natsort` library for natural ordering.
- Chinese/Japanese/Korean charracters sort by code point won't match pinyin/stroke/radical order users expect — needs ICU or language-specific libraries.

### Quick decision guide

For English-only with mixed case, use `key=str.casefold`.

For European languages on a controlled environment, use `locale.strxfrm`.

For portable or multi-threaded code with proper Unicode support, use `pyuca` or `PyICU`.

For filenames with numbers, use `natsort`.

## Object List

Using the `key` argument, it's more efficient and cleaner than JS's comparator function:

```python
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Carol", "age": 35},
]

sorted(users, key=lambda u: u["age"])
# sorted by age ascending

# Multiple keys (tuple)
sorted(users, key=lambda u: (u["age"], u["name"]))

# For class instances, use operator.attrgetter ( which faster than lambda)
from operator import itemgetter, attrgetter
sorted(users, key=itemgetter("age"))
```

## Performance Considerations

The complexity is `O(n log n)` for worst case scenario, `O(n)` on already-sorted or nearly-sorted data. Python uses the same algorithm JS engines like V8 use for `Array.prototype.sort` since 2018.

When comparing **`sort()` vs `sorted()`**: `sort()` is slightly faster and uses less memory because no new list is allocated. Use it when you don't need the original order.

As mentionned aboce, **`attrgetter`/`itemgetter’** are implemented in C and are noticeably faster than equivalent lambdas on large lists.

### About `key` versus Comparator

The core difference between the two is the following:

- `key` transforms each element into a sort value _once_. Python then compares those precomputed values.
- the comparator is a function that takes _two_ elements and returns negative/zero/positive. Python calls the function every time the sort algorithm needs to compare a pair.

For `n` elements, sorting with the comparator does `n log n` comparisons, but only `n` key transformations.

Let’s take an example of sorting strings by length:

```python
words = ["kiwi", "fig", "banana", "apple", "date"]
```

With `key`, you’d write:

```python
call_count = 0

def length_key(s):
    global call_count
    call_count += 1
    return len(s)

sorted(words, key=length_key)
print(call_count)  # 5  — called once per element
```

With the comparator via `cmp_to_key`, you’d have:

```python
from functools import cmp_to_key

call_count = 0

def length_cmp(a, b):
    global call_count
    call_count += 1
    return len(a) - len(b)

sorted(words, key=cmp_to_key(length_cmp))
print(call_count)  # 7  — called once per comparison (varies by input)
```

5 elements produce 5 key calls vs. ~7 comparator calls. With 1,000 elements: 1,000 vs. ~10,000. With 1,000,000: 1M vs. ~20M.

So when do you _actually_ need a comparator?

When the sort order depends on a **relationship between two elements,** that can’t be reduced to a single value per element.

Let’s look at a common example where we need to arrange a list of numbers to get the largest number from the list.

So given this list `[3, 30, 34, 5, 9]`, the sort result would be `[9, 5, 34, 3, 30]` to get this biggest number: `"9534330"`.

You can’t assign a single sort key to compare `3` vs. `30` in isolation — it depends on which you’re comparing against:

- `3` vs `30` would provide this pair comparaison `"330" > "303"`. We can say that `3` comes first.
- `3` vs `34` would provide this pair comparaison `"334" < "343"`. This time `34` comes first.

Let's code it:

```python
from functools import cmp_to_key

nums = [3, 30, 34, 5, 9]

def compare(a, b):
    # If "ab" > "ba", a should come first so it returns negative
    if str(a) + str(b) > str(b) + str(a):
        return -1
    elif str(a) + str(b) < str(b) + str(a):
        return 1
    return 0

result = sorted(nums, key=cmp_to_key(compare))
print("".join(map(str, result)))  # "9534330"
```

No single-value `key` function can express this — the ordering is inherently pairwise.

So to make the decision between `key` or a comparator, follow this rule of thumb:

- Want to sort by X of each element ? Sse `key`.
- Want to sort based on how two elements relate to each other? Use `cmp_to_key`.
- If you can express it as `key`, always prefer it: fewer calls, and the transformed values get cached internally.

## A Few Caveats to Know

`list.sort()` returns `None`, not the sorted list. Use `sorted()` for chaining or assignment.

Remember that equal elements (see the apple example above) preserve their original order (same as modern JS).

If you use **mixed types**, Python will raise `TypeError` and `sorted([1, "a"])` fails. JavaScript would silently coerce to strings.

`None` values can't be compared to numbers — supply a `key` that handles them: `key=lambda x: (x is None, x)`.

Last but not least, remember that strings sort lexicographically by Unicode code point, so `"Z" < "a"`. For case-insensitive sorts, use `key=str.lower`; for locale-aware, use `locale.strxfrm`.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Pixabay on Pexels.
