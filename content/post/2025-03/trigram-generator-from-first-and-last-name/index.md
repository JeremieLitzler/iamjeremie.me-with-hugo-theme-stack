---
title: "Trigram Generator from First and Last Names"
description: "This was fun coding challenge for a project last year. How do you evaluate the trigram of a person from his or her full name?"
image: 2025-03-24-demonstration-of-a-trigram.jpg
imageAlt: Demonstration of a trigram
date: 2025-03-24
categories:
  - Software Development
tags:
  - Python
---

Let’s say you want to build a trigram from the first and last name of a person.

The trigram can equal to the first letter of the first name and the first 2 letters of the last name of the person.

The characters of the trigram are usually capitalized.

For example:

- “Jéremie Litzler” outputs “JLI”
- “John Doe” outputs “JDO”
- “Maxime Fèvre” outputs “MFE”
- “Carlos Di Montis” outputs “CDI”.

Let’s review the code in Python for this.

## AI First Attempt

Today, I’ll share how AI can speed (and where it shows its limitation) the coding process a draft of the code for the above specifications.

It provided me with this (I edited the comments):

```python
def generate_trigram(full_name):
    # Split the full name into parts
    # `[0]` means take the first element in the `name_parts` array
    # `[0]` means take the first characters of the string
    name_parts = full_name.split()

    # Get the first letter of the first name
    firstname_letter = name_parts[0][0]

    # Get the first two letters of the last name
    # `[-1]` means take the last part of the `name_parts` array
    # `[:2]` means take the first two characters of the string
    lastname_letters = name_parts[-1][:2]

    # Combine and capitalize
    trigram = (firstname_letter + lastname_letters).upper()

    return trigram
```

## Let’s Test This

```python
import unittest
from typing import Tuple, List

from app.services.trigram_service import GetTrigramService
from tests.services.common_tests import OnCallAppTestsBase

class TestGetTrigramService(OnCallAppTestsBase):

    def setUp(self):
        super().setUp()

    def test_evaluate_returns_correct_value(self):
        # The tuple defines:
        # 1- the full name to convert to a trigram
        # 2- the expected trigram
        full_names: List[Tuple[str, str]] = [
            ("Jéremie Litzler", "JLI"),
            ("John Doe", "JDO"),
            ("Carlos Di Montis", "CDI"),
            ("Maxime Fèvre", "MFE")
        ]

        for full_name, expected_trigram in full_names:
            trigram = GetTrigramService.evaluate(full_name)
            self.assertTrue(
                trigram == expected_trigram,
                f'actual=<{trigram}> ; expected=<{expected_trigram}>'
            )


if __name__ == "__main__":
    unittest.main()
```

Did you get a passing test? I didn’t! The code succeeds on 2 out of 4, failing on “Carlos Di Montis”.

Let's not blame the AI completely, the specification didn’t mention that the first name comes first and what follows the **first space** represents the last name, no matter the number of parts in it.

## What Won’t Wrong

First, with `full_name.split()`, you get an array of 3 strings: “Carlos”, “Di”, “Montis”.

Next, why take the last element of the array as the actual last name?

Of course, I could have written clearer specifications, but that’s what you call iterative programming!

## Let’s Fix The Specification and The Code

Firstly, our new requirement is to take the first 2 characters of the lastname, which may contain spaces. So we need to split the full name at the first space, instead of “at each space”.

But how do you fix the split issue?

Split in Python can take two arguments: the first one is the delimiter and the second tells after how many occurrences to stop.

The delimiter is a space and we need to stop after one occurrence (assuming that the full name excludes multiple first names, of course).

So, we update the line:

```python
name_parts = full_name.split()
```

into :

```python
name_parts = full_name.split(' ', 1)
# Below we destructure the array into individual string variables
first_name, last_name = name_parts
```

Let’s run the test. And again, it fails…

## What Is The Next Issue

The code doesn’t evaluate “Maxime Fèvre” to “MFE” but “MFV”. Why?

The accent, of course! Why? The accent was skipped, because it’s a special character and Python acted as if it wasn’t present.

Luckily, there is a solution for that: we call it “Unicode normalization” and we have 4 forms out there. For details, you can [read this detailed article](https://towardsdatascience.com/difference-between-nfd-nfc-nfkd-and-nfkc-explained-with-python-code-e2631f96ae6c).

In our _Maxime Fèvre_, we find an accent in the last name.

To remove it and keep the unaccented “e”, we’ll use _NFKD_ normalization form in the following code:

```python
import unicodedata

@staticmethod
def remove_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str)
  return ''.join([character for character in nfkd_form if not unicodedata.combining(character)])
```

This function uses the `unicodedata` module to handle Unicode characters. Here’s how it works:

1. `unicodedata.normalize('NFKD', input_str)`:
   - We use the `normalize` function to convert the string to a normalized form.
   - “NFKD” stands for “Normalization Form Compatibility Decomposition”.
   - This decomposition separates the base characters from their diacritical marks (accents).
   - For example, it decomposes “è” into “e” and the accent mark.
2. `[character for character in nfkd_form if not unicodedata.combining(c)]`:
   - This is a list comprehension that iterates through each character in the normalized form.
   - `unicodedata.combining(character)` returns `True` for characters that are combining marks (like accents).
   - The `not` inverts this, so we keep only characters that aren’t combining marks.
3. `''.join([...])`:
   - This joins all the kept characters back into a string.

So, essentially, the function works by:

1. Splitting each character into its base form and any accent marks.
2. Keeping only the base characters and discarding the accent marks.
3. Rejoining the remaining characters into a string.

For example, with the last name “Fèvre”:

1. It’s normalized to something like `['F', 'e', '`“, “v”, ’r’, “e”]`
2. The accent '`” is discarded because it’s a combining character
3. It joins the the remaining characters into a string again, resulting in “Fevre”

This method is particularly effective because it works for many accented characters and other diacritical marks across many languages, not just French accents.

Now, you can now use it in the evaluated method:

```python
#Get the first letter of the first name
first_letter = GetTrigramService.remove_accents(first_name[0])

#Get the first two letters of the last name
last_name_letters = GetTrigramService.remove_accents(last_name[:2])
```

Hooray! The test is passing. 🎇

## Final Solution (Don’t Cheat By Clicking The Table Of Contents To Soon!)

So let’s put it together.

```css
class GetTrigramService:
    @staticmethod
    def evaluate(full_name) -> str:
        # Split the full name into parts
        name_parts = full_name.split(" ", 1)

        # If there's only one part (i.e., no space in the name), return None or handle as needed
        if len(name_parts) < 2:
            return None  # or handle this case as appropriate for your use case

        first_name, last_name = name_parts

        # Get the first letter of the first name
        first_letter = GetTrigramService.remove_accents(first_name[0])

        # Get the first two letters of the last name
        last_name_letters = GetTrigramService.remove_accents(last_name[:2])

        # Combine and capitalize
        trigram = (first_letter + last_name_letters).upper()

        return trigram

    @staticmethod
    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([character for character in nfkd_form if not unicodedata.combining(character)])
```

## Conclusion

OK, I have lessons to share:

- First: don’t trust the AI on the first shot. Always review the code.
- Second: Always test the code and find the edge cases 😊.

Yes, you’ll need to think thoroughly to code a complete solution. The AI didn’t guess the last name or the accents issue.

You can because you pick good test sets and, in the end, good tests will provide a complete solution. Who said AI would replace software engineers? 😋

And beware of accents in general!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
