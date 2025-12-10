---
title: "Windows - Move AppData from C Drive to a Data Drive"
description: "The AppData can grow big."
image: /quick-tips/images/Microsoft_Windows-Logo.png
imageAlt: Logo of Microsoft Windows
date: 2025-12-06
categories:
  - Command Line
tags:
  - Windows
---

## Scenario

I was running out of space in my C Drive on my laptop and I noticed that the `AppData` was taking a lot of disk space, especially the application Signal.

The cause: the pictures and other documents shared with my contacts.

## Solution

Important: Close Signal completely before starting (right-click system tray icon → Quit)

1. Open Command Prompt as Administrator
   Press Win + X and select “Command Prompt (Admin)” or “Windows PowerShell (Admin)”
2. Move the existing Signal folder

   ```cmd
   move "C:\Users\jerem\AppData\Roaming\Signal" "E:\Applications\ProgramFiles\Signal"
   ```

3. Create the symbolic link

   ```cmd
   mklink /D "C:\Users\jerem\AppData\Roaming\Signal" "E:\Applications\ProgramFiles\Signal"
   ```

4. Verify the link was created

   ```cmd
   dir "C:\Users\jerem\AppData\Roaming" | find "Signal"
   ```

   You should see `<SYMLINKD>` icon next to Signal, indicating it's a symbolic link.

5. Start Signal—it should work exactly as before, but now store data on your E: drive.

The `/D` flag creates a directory symbolic link (junction).

Make sure `E:\Applications\ProgramFiles` exists before running the `move` command.

This preserves all Signal messages, settings, and media.
If you ever need to reverse this, delete the symbolic link and move the folder back.

## Troubleshooting

### If Signal doesn’t start

Verify the symbolic link exists and points to the correct location using `dir` command.

### `mklink` Isn’t a Known Command

Though it is a built-in Windows command, not a separate program you need to install, I came across the issue.

I was running the command line as Administrator

The alternative I used was PowerShell instead.

```powershell
New-Item -ItemType SymbolicLink -Path "C:\Users\jerem\AppData\Roaming\Signal" -Target "E:\Applications\ProgramFiles\Signal"
```

## Documentation

References:

- [Microsoft Learn—`mklink`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mklink).
- [Microsoft Learn—PowerShell](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item?view=powershell-7.5#example-7-create-a-symbolic-link-to-a-file-or-folder)

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credits: Photo by [www.logo.wine](https://www.logo.wine/logo/Microsoft_Windows)
