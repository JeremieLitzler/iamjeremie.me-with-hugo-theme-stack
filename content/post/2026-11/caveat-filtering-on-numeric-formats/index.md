---
title: "Caveat Filtering On Numeric Formats"
description: "There are many numeric formats, variable from a country to another. When it comes to searching on those values, you need careful attention to detail."
image: 2026-11-02-calculator-display-showing-large-number.jpg
imageAlt: Close-up of a calculator display showing a large number
date: 2026-11-02
categories:
  - Software Development
tags:
  - Csharp
---

Earlier this year, I worked on a bug with where a query (as in _CQS pattern_) didn't return the expected results when performing a specific search to find a record from a money amount.

Let me explain with an example what was going on and how I solved it.

## The Starting Point

The search term was `5'`. Why? Because the client application displayed money amount with a pseudo-german-swiss numeric format. The value `10000` would be displayed `10'000` instead of `10’000` as it should.

Therefore, users in Switzerland, or any country to that matter, don't really type the typographic apostrophe (`’`, you have to type `ALT+0146` to get it...) but they will use the regular apostrophe (aka. dactolygraphic apostrophe or `'`).

The query pulled a list of items and we used EF6, Gridify (for pagination), LINQ to write the query.

Before that, nothing is available in memory.

The search above supposed the existance of a column `Amount` of type `money`, in the SQL Server database, where the value of record was `65000`.

The code looked like this (it isn't the original code but something close to it):

```csharp
//Excerpt of TransactionsQueryHandler
private IQueryable<TransactionResult> PerformSearch(IQueryable<TransactionResult> transactions, string search) =>
  search // Cannot be null
    .ToLower()
    .Trim()
    .Split(' ')
    // Add "and" clauses to the query for each term
    .Aggregate(transactions, (transaction, term) => transaction.Where(SearchExpression(term)));

private readonly string _dateSeparator = "-";

private Expression<Func<TransactionResult, bool>> SearchExpression(string term)
{
    return transaction =>
    (transaction.CreatedOn.Year.ToString() + _dateSeparator +
        (transaction.CreatedOn.Month > 10
        ? transaction.CreatedOn.Month.ToString()
        : "0" + transaction.CreatedOn.Month.ToString()) + _dateSeparator +
        (transaction.CreatedOn.Day > 10
        ? transaction.CreatedOn.Day.ToString()
        : "0" + transaction.CreatedOn.Day.ToString()) + _dateSeparator
    +
    transaction.Id +
    transaction.ReferenceId +
    transaction.Amount +
    transaction.CurrencyIsoCode
    )
    .ToLower()
    .Contains(term);
}

```

Where is the issue?

## The Cause

In short, the regular expression wasn’t specific enough and only took care of the apostrophes with numbers around.

Let’s fix that!

## The Solution

```csharp
//Excerpt of TransactionsQueryHandler
  search // Cannot be null
    .ToLower()
    .Trim()
    .Split(' ')
    // The new line
    .Select(term => term.StripNumericApostrophes())
    // Add "and" clauses to the query for each term
    .Aggregate(transactions, (transaction, term) => transaction.Where(SearchExpression(term)));

// The class to normalize the search terms
public static class StringExtensions
  {
    /// <summary>
    /// Remove the regular apostrophe and right single quotation mark in string.
    /// </summary>
    /// <param name="source">The string containing the characters to remove</param>
    /// <returns>The normalized string</returns>
    /// <see cref="DecimalExtensions.Search(decimal, string)"/>
    public static string StripNumericApostrophes(this string source)
    {
      // Remove apostrophes that are commonly used as thousands separators in numbers
      // This handles both regular apostrophe (') and right single quotation mark (’)
      // We only remove them if they appear between digits
      var normalized = System.Text.RegularExpressions.Regex.Replace(
        source,
        @"(?<=\\d)''’'",
        ""
      );

      return normalized;
    }
  }

```

I wrote the following tests:

```json
// lang, test description, searchText, except record count
{ "en", "Search '5000' should find item on amount", "5000", 1 },
{ "en", "Search '5'000' should find item on amount", "5'000", 1 },
{ "en", "Search '65’0' should find item on amount", "65’0", 1 },
{ "en", "Search '65'0' should find item on amount", "65'0", 1 },

```

These were fine. But, I missed a few use cases:

```json
{ "en", "Search '’000' should find item on amount", "’000", 2 },
{ "en", "Search ''000' should find item on amount", "'000", 2 },
{ "en", "Search '65’' should find item on amount", "65’", 2 },
{ "en", "Search '65'' should find item on amount", "65'", 2 },

```

These failed. Why?

The regular expression was incorrect. To match the extra 4 tests, it had to become the following:

```csharp
@"(?<!\\w)''’|(?<=\\d)[''’]",

```

This only removes leading apostrophes in word boundaries and only if it comes before or after a digit.
In details,

- First part: `(?<!\\w)''''`
  - This matches apostrophes before digits:
    - `(?<!\\w)` - It is a negative lookbehind that asserts that what comes immediately before the current position is NOT a word character.
    - `?<!` represents the negative lookbehind.
    - `\\w` matches letters, digits, and underscore `[a-zA-Z0-9_]`.
    - This prevents matching apostrophes in the middle of words like `don't50`.
  - `[''’]`
    - Matches any ONE of these apostrophe characters:
      - `'` - Regular apostrophe (U+0027) (doubled to escape it)
      - `’` - Typographic/right single quotation mark (U+2019)
  - `(?=\\d)` - Positive lookahead
    - `?=` asserts that what comes immediately after the apostrophe is a digit
    - `\\d` matches any digit [0-9]
- `|`: the pipe character means `OR`. The regex will match if EITHER the first part OR the second part matches to something
- Second part: `(?<=\\d)[''’]`
  - This matches apostrophes after digits:
    - `(?<=\\d)` is a positive lookbehind that asserts that what comes immediately before the current position IS a digit. This ensures we only match apostrophes that follow numbers
    - `[''’]` works like the first part of the expression.

## Testing `StripNumericApostrophes`

That prompted me to test the method `StripNumericApostrophes`. The use cases were:

```csharp
using AwesomeAssertions;
using MyProject.Application.Queries.Extensions;
using Xunit;

namespace MyProject.Application.Queries.IntegrationTests.Extensions
{
  public class StringExtensionsShould
  {
    [Theory]
    [InlineData("5'", "5")]
    [InlineData("5'0", "50")]
    [InlineData("'50", "50")]
    [InlineData("5’", "5")]
    [InlineData("5’0", "50")]
    [InlineData("’50", "50")]
    [InlineData("’test", "’test")]
    [InlineData("test’", "test’")]
    [InlineData("test’test", "test’test")]
    [InlineData("'test", "'test")]
    [InlineData("test'", "test'")]
    [InlineData("test'test", "test'test")]
    public void StripNumericApostrophesCorrectly(string source, string expected)
        => source.StripNumericApostrophes().Should().Be(expected);
  }
}

```

In my business need, I didn't need to handle the `@'10` or `10'!` because it wasn't going to happen. It would have been useless tests.

## Security Risks Evaluation

From my research, I came across a **ReDoS (Regular Expression Denial of Service)** risk, though it's relatively low with this specific pattern tested so far. However, I'd like to share the possible concerns that you need to be aware of.

### _ReDoS_ Risk Assessment

The regex `(?<!\\w)''’|(?<=\\d)[''’]` is relatively safe because:

- it uses no nested quantifiers (`+`, , `{n,m}`)
- it has no overlapping alternations that cause excessive backtracking
  - For example, `(.|\\s)*` pattern with a source string that is many spaces could ended up with 2^N permutations.
- it has lookbehinds and lookaheads are fixed-width
  - `?<` checks exactly 1 character behind so it is fixed-width
  - `?=` checks exactly 1 character ahead so it is fixed-width

**However**, malicious input could still cause issues with very long strings (MB+ of text) that would take time to process. Indeed, `Regex.Replace` must scan the entire string character by character.

### Recommended Mitigations

In the frontend application, the `<input>` element could use `maxlength` attribute to limit this issue.
In the backend application, we could also mitigate the issue with string length check:

```csharp
public static string StripNumericApostrophes(this string source)
{
    if (string.IsNullOrEmpty(source))
        return source;

    // Mitigation 1: Limit input length
    const int MaxLength = 10000; // Adjust based on your needs
    if (source.Length > MaxLength)
        throw new ArgumentException($"Input exceeds maximum length of {MaxLength} characters");

    // Mitigation 2: Set regex timeout (requires .NET 4.5+)
    try
    {
        var normalized = System.Text.RegularExpressions.Regex.Replace(
            source,
            @"(?<!\\w)''’|(?<=\\d)[''’]",
            "",
            // Only specified to use the timeout
            System.Text.RegularExpressions.RegexOptions.None,
            // Timeout after 100ms in case of catastrophic backtracking. See above example.
            // Plus, the timeout would not apply on the whole expression, but each part.
            TimeSpan.FromMilliseconds(100)
        );
        return normalized;
    }
    catch (RegexMatchTimeoutException)
    {
        // Log the attempt
    }
}

```

### Additional Best Practices

You could consider caching the compiled regex for better performance:

```csharp
private static readonly Regex NumericApostropheRegex = new Regex(
    @"(?<!\\w)''’|(?<=\\d)[''’]",
    RegexOptions.Compiled,
    TimeSpan.FromMilliseconds(100)
);

public static string StripNumericApostrophes(this string source)
{
    if (string.IsNullOrEmpty(source))
        return source;

    if (source.Length > 10000)
        throw new ArgumentException("Input too long");

    return NumericApostropheRegex.Replace(source, "");
}

```

Using this practice will depend on the amount of searches performed on the frontend.

The regex is complex and the application could benefit from it. But that's an optimization to consider when the breaking point happens. It wasn't used heavily in the application (only one endpoint).

### Non-Regex Approach

If you're very concerned about security, consider a character-by-character approach:

```csharp
public static string NoRegexStripNumericApostrophes(this string source)
{
    // Again, limit the source size
    if (string.IsNullOrEmpty(source) || source.Length > 10000)
        return source;

    var sb = new StringBuilder(source.Length);
    var apostrophes = new HashSet<char> { '\\'', '’' };

    for (int i = 0; i < source.Length; i++)
    {
        char c = source[i];

        if (apostrophes.Contains(c))
        {
            bool afterDigit = i > 0 && char.IsDigit(source[i - 1]);
            bool beforeDigit = i < source.Length - 1 && char.IsDigit(source[i + 1]);
            bool afterNonWord = i == 0 || !char.IsLetterOrDigit(source[i - 1]) && source[i - 1] != '_';

            // Skip apostrophe if it matches our removal criteria
            if ((afterNonWord && beforeDigit) || afterDigit)
                continue;
        }

        sb.Append(c);
    }

    return sb.ToString();
}

```

This works exactly the same as the regex method.

### Sources

- Timeout - Timeouts are built in to the .NET standard library through the System.Text.RegularExpressions.Regex MatchTimeout property ([Wikipedia](https://en.wikipedia.org/wiki/ReDoS)).
- Length limits - This is a standard security practice for input validation.
- RegexOptions.Compiled - Improves performance for frequently used patterns ([Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-options)).
- Try-catch - When a RegexMatchTimeoutException is thrown, the recommended pattern is to wait for a brief, random time interval after the exception is thrown before calling the matching method again ([Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regexmatchtimeoutexception?view=net-8.0)).

## Conclusion

The search is a complex matter and we could go on well beyond this article. Using specialized services may help, but in this case, the implementation of a new dependency was a big overhead. So we kept the regular expression

Thank you for having read to the end!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Marina Agrelo on Pexels (`https://www.pexels.com/photo/person-using-a-calculator-5652294/`).
