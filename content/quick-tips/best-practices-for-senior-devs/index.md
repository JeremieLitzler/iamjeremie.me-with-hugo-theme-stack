---
title: "Best Practices: Checklist to Become a Good Senior Dev"
description: "The engineer shipping the most code isn't always the one who gets promoted."
image: /quick-tips/images/an-organized-desk.jpg
imageAlt: An organized desk
date: 2026-02-20
categories:
  - Software Development
tags:
  - Best Practices
---

## Before finishing any task (5–15 min max)

- Add a comment explaining a non-obvious decision or “why”
- Clarify or improve an error message
- Extract a magic number into a named constant
- Add type hints to function signatures
- Add a log statement that would speed up future debugging
- Fix a flaky test if you spot one
- Update the `README` with something that confused you
- Extract repeated logic into a shared/reusable module
- Add examples or error cases to API/function docs
- Document a deployment or config gotcha

## The 5 questions to ask yourself

1. What confused me while working on this?
2. What will confuse the next person?
3. What was non-obvious or surprising?
4. What would make debugging this easier?
5. What pattern am I repeating that could be extracted?

{{< blockcontainer jli-notice-warning "The Rule">}}

- 5 min minimum, 15 min maximum.
- If it needs more, create a ticket—don’t skip it entirely.

{{< /blockcontainer >}}

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/black-study-lamp-on-black-table-159839/).
