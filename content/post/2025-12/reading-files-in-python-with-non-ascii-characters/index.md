---
title: "Reading Files In Python With non-ASCII Characters"
description: "Encoding is important to the end user. As a native French speaker, I like to see the accents rendered properly on a page."
image: 2025-12-15-a-man-with-a-magnifying-glass-decyphering-symbols.jpg
imageAlt: A man with a magnifying glass deciphering symbols
date: 2025-12-15
categories:
  - Software Development
tags:
  - Python
  - ASCII
---

Rendering non-ASCII characters is crucial when a file text content contains some non-ASCII characters. In French, we often find accentuated characters like “é”, “è” or “à”. But that’s not all of them.

Let’s see how you should go about reading content from the UTF-8 file and render the accent properly in a Jinja template.

## Reading the File

Let’s take a JSON file that is encoded with UTF-8.

In Python, you read the file in the following manner:

```python
    def fetch_data(self) -> Optional[List[Dict]]:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from file: {self.file_path}")

```

While this reads the content, if you have any non-ASCII characters like “é”, “è” or “à”, you should see misencoded characters.

## How to Fix the Issue

It’s as simple as adding a parameter the `open` method:

```python
with open(self.file_path, 'r', encoding='utf-8') as file:
```

With the `encoding` parameter, Python reads the content with the proper encoding.

**Note**: If the JSON file has a Byte Order Mark (BOM), you might need to use **`encoding='utf-8-sig’’** to handle it correctly. However, if you really need to edit the file, then you should use an editor that can produce valid ’utf-8’ content.

## About Jinja Template

Jinja2 templates expect Unicode strings. If the data passed to the template contains byte strings or incorrectly encoded strings, it might not render special characters correctly.

With the fix above, the content rendered is displayed correctly to the user.

## About Writing to the File

The `json` module in Python, by default, sets `ensure_ascii=True` when serializing data, which means all non-ASCII characters are escaped. This can lead to issues when rendering these characters in HTML or Jinja templates.

The solution: when serializing JSON data, you can set **`ensure_ascii=False`** to preserve the original Unicode characters:

```python
json.dumps(data, ensure_ascii=False)
```

**Note**: This setting doesn’t affect **`json.load`** but is only relevant when you’re writing JSON data back to a file or passing it to a template.

## Did You Learn Something

If so…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article and make sure to share, [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [cottonbro studio](https://www.pexels.com/photo/photo-of-person-taking-down-notes-7319070/).
