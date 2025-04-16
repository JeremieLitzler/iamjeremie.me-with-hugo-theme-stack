---
title: "Using Regular Expression With Visual Studio Code Replace Functionnality"
description: "Once I had the new to replace many [n] into [^n]."
image: 2025-04-16-vsc-with-regex-on-string-replacement.svg
imageAlt: Visual Studio Code and Regular Expressions For String Replacement
date: 2025-04-16
categories:
  - Web Development
tags:
  - Regular Expressions
  - IDE
  - Visual Studio Code
---

That’s a great example to use Regex in the Find and Replace function of Visual Studio Code.

To replace all occurrences of `[n]` with `[^n]` in Visual Studio Code, where `n` is any number, follow these steps:

## Step 1. Open the Find and Replace Panel

- Press `Ctrl + H` (Windows/Linux) or `Cmd + Option + F` (Mac).

## Step 2. Enable Regular Expression Search

- Click the `.*` icon (or press `Alt + R`) to enable regex mode.

## Step 3. Enter the Find Pattern

- Use the following regular expression to match `[n]` where `n` is a number:

  ```plaintext
  \[(\d+)\]
  ```

  - `$$` and `$$` match the literal square brackets.
  - `(\d+)` captures one or more digits.

## Step 4. Enter the Replace Pattern

- Use this replacement string:

  ```plaintext
  [^$1]
  ```

  - `$1` refers to the captured number inside the brackets[3].

## 5. Replace All

- Click "Replace All" (or press `Alt + Enter` to select all matches, then `Ctrl + Shift + L` to replace).

## Example

| Original Text | Find Pattern | Replace Pattern | Result              |
| ------------- | ------------ | --------------- | ------------------- |
| [1],,[456]    | $$(\d+)$$    | [^$1]           | [^1], [^23], [^456] |

This will convert every `[number]` into `[^number]` throughout your document using Visual Studio Code's regex-powered find and replace.

**Note:** Make sure regex mode is enabled, or the patterns won't work as intended.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
