---
title: "A TimeCostLogger in C#"
description: "Knowing how long your code takes to execute is the first information to gather when a process seems to underperform."
image: 2026-01-26-a-stopwatch.jpg
imageAlt: A stopwatch
date: 2026-01-26
categories:
  - Software Development
tags:
  - Csharp
---

Your application runs fine in development, passes all tests, and then, suddenly, users start complaining about slowness in production.

You check the logs and scan through metrics you have available, but can’t pinpoint where the bottleneck actually lives.

Is it the database query, non-optimized for the data volume in production ? The file processing? A third-party API call you added last month for a new feature?

Here is one way to identify the code responsible for slow code execution.

## Measuring Time Spent Executing Code

This is exactly where a `TimeCostLogger` becomes invaluable. Instead of guessing or setting up elaborate profiling tools, you can wrap suspicious code blocks and let the numbers tell the story.

Drop it around your database operations, your heavy computation loops, or those external service calls. For example:

```csharp
using (new TimeCostLogger("MailService.Send"))
{
  _mailService.Send(mail, null);
}
```

When the logs roll in, you’ll see exactly which pieces are eating up those precious seconds.

## How to Implement it

Like I said, you don’t need to install profiling software, learn new tools, or change your deployment process.

It’s just a `using` statement that you can add during bug investigation and leave in place for production monitoring. When performance doesn’t look great, you’ll have historic timing data showing you exactly when and where things started slowing down.

It’s particularly useful when you’re dealing with complex workflows that have multiple steps. Maybe your entire process takes five seconds, but you don’t know if that’s because step one runs slow or step five is the culprit.

You can wrap each step individually. That series of calls to different services that you thought was the problem? It took a few hundred milliseconds. The email client sending emails? That’s your twenty seconds bottleneck.

It happended to me a few months back.

Sure, there are more sophisticated profiling tools out there, but sometimes you just need quick answers without the overhead.

## The Code

The following `TimeCostLogger` below gives you that focused visibility right where you need it, with the logging infrastructure you already have in place.

````csharp
      /// Usage: wrap the code to measure
      ///
      /// - with a suffixed-custom-block-name appended to the log
      /// ```
      /// using (new TimeCostLogger("Custom block name"))
      /// {
      ///   // Code to time…
      /// }
      /// ```
      ///
      /// or wrap a whole class and method:
      ///
      /// ```
      /// using (new TimeCostLogger())
      /// {
      ///   // Code to time…
      /// }
      /// ```
      /// </summary>
      public class TimeCostLogger : IDisposable
      {
            private readonly Stopwatch _stopwatch;
            private readonly string _className;
            private readonly string _methodName;
            private readonly string _blockName;

            public TimeCostLogger([CallerMemberName] string methodName = "", [CallerFilePath] string filePath = "")
            {
                  _className = GetClassNameFromFilePath(filePath);
                  _methodName = methodName;
                  _blockName = null;
                  _stopwatch = Stopwatch.StartNew();
            }

            public TimeCostLogger(string blockName, [CallerMemberName] string methodName = "", [CallerFilePath] string filePath = "")
            {
                  _className = GetClassNameFromFilePath(filePath);
                  _methodName = methodName;
                  _blockName = blockName;
                  _stopwatch = Stopwatch.StartNew();
            }

            private string GetClassNameFromFilePath(string filePath)
            {
                  if (string.IsNullOrEmpty(filePath))
                        return "Unknown";

                  var fileName = System.IO.Path.GetFileNameWithoutExtension(filePath);
                  return fileName;
            }

            public void Dispose()
            {
                  _stopwatch.Stop();

                  var timeElapsedInMs = _stopwatch.ElapsedMilliseconds;
                  var location = string.IsNullOrEmpty(_blockName)
                        ? $"{_className}.{_methodName}"
                        : $"{_className}.{_methodName} - {_blockName}";
                  var message = $"Time elapsed for {location} in ms : {timeElapsedInMs}";

                  LogHelper.LogInfo(LoggedInUser.Instance.AppCode, message, null);
            }
      }

```’

## Conclusion

And you, how would you do it?

For me, it helps pinpoint the issue: the SMTP server was configured with a folder drop in using a CNC path and, if you performed several calls to the top-level API, it’d take 20 seconds to run.

The feature behind it wasn’t critical and the client used it very sparingly, so we downgraded the priority, though I’ll be writing about the reason as soon as the issue becomes a priority again.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [William Warby](https://www.pexels.com/photo/close-up-of-a-heuer-mechanical-stopwatch-19730401/).
````
