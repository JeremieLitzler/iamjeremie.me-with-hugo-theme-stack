---
title: "How to format a duration in a formula on Google Sheets"
description: "Yes, you can use the formatting menu, but it is not enough. What if I told you can format a decimal value representing a time using a formula. Let's review the steps."
image: 2025-05-16-an-alarm-clock-displaying-23h53.jpg
imageAlt: An alarm clock displaying 23h53
date: 2025-05-14
categories:
  - Astuce Du Jour
tags:
  - Google Sheets
---

Let’s take the example below:

|     | A       | B                        | C                    |                       |
| --- | ------- | ------------------------ | -------------------- | --------------------- |
| 1   | Lessons | NumberOfMinutesPerLesson | TotalDurationDecimal | TotalDurationFormated |
| 2   | 50      | 5                        | 4.16                 | 4:10:00               |
| 3   | 35      | 6                        | 3.50                 | 3:30:00               |

## The caveat

In Google Sheet, the conversion from a decimal to a duration value follow some rules.

For example,

- `1` is equivalent to `24:00:00`
- `1.35` is equivalent to `32:24:00`
- `0.5` is equivalent to `12:00:00`
- `0.05125` is equivalent to `01:13:48`

So if we format the decimal values above, the result won’t be the _4:10:00_ and _3:30:00_ expected.

## The solution

Thankfully, it’s easy to solve that.

Given that we have applied the duration formatting on the column D, the formula is as follows:

|     | A       | B                        | C                    | D                     |
| --- | ------- | ------------------------ | -------------------- | --------------------- |
| 1   | Lessons | NumberOfMinutesPerLesson | TotalDurationDecimal | TotalDurationFormated |
| 2   | 50      | 5                        | =A2\*B2              | =C2/60/24             |
| 3   | 32      | 6                        | =A3\*B3              | =C3/60/24             |

Column C contains a number of hours.

Since the formatting will apply `1 = 24h` , we simply need to divide the column C value by 60 and then by 24.

When the duration formatting is applied, it’ll therefore display the proper duration.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [FOX ^.ᆽ.^= ∫](https://www.pexels.com/photo/white-digital-desk-clock-2046808/).
