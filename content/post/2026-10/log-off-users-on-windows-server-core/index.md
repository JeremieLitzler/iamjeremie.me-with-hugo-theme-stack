---
title: "Log Off Users on Windows Server Core"
description: "Stale sessions on forgotten VMs kept locking my Windows account. Here is how to list and log off users on Windows Server Core from the command line."
image: 2026-10-21-a-series-of-red-padlocks-attached-to-a-stone-wall.jpg
imageAlt: A series of red padlocks attached to a stone wall
date: 2026-10-21
categories:
  - Software Development
tags:
  - Windows Server
  - PowerShell
  - Windows Server Core
  - Remote Desktop
---

I have the habit of changing my password once a month instead of waiting for the 90-day limit. But somehow, it has caused me some headaches at work: my Windows account kept getting locked, very often.

It turned out that I was still connected to several remote VMs, and they kept trying to log me in with an old password. Each failed attempt counted toward the lockout.

On a Windows VM with a desktop, logging off a user is easy. You open the Task Manager, go to the **Users** tab, right-click the session and choose **Sign off**. But what about Windows Server Core, which has no Task Manager UI to click through? This short tutorial answers that.

## List the Active Sessions

Open a PowerShell prompt on the target server (Choice "15") and run:

```powershell
query user
```

The short form `quser` works too. Microsoft's documentation describes it as the command that "displays information about user sessions on a Remote Desktop Session Host server", and it returns the user name, the session name, the session ID, the state, the idle time and the logon time.

The output looks like this:

```plaintext
 USERNAME     SESSIONNAME   ID  STATE   IDLE TIME  LOGON TIME
 jermiel      rdp-tcp#0      2  Active          .  10/19/2026 9:12 AM
 alext                       3  Disc         1:05  10/19/2026 8:40 AM
```

A `>` symbol is displayed before the current session, which helps you avoid cutting off the branch you are sitting on.

If you are not on the server itself, you can query it remotely:

```powershell
quser /server:SERVERNAME
```

Notice the `Disc` state on the second line. A disconnected session is exactly what bit me: the session is gone from your screen, but it is still alive on the VM and still holds your old credentials.

## Log Off One of Them

The `logoff` command takes the session ID, the number in the `ID` column, not the user name:

```powershell
logoff 3
```

Against a remote server, add the same `/server` parameter:

```powershell
logoff 3 /server:SERVERNAME
```

Two remarks from the documentation are worth keeping in mind. After a log off, all processes of that session end and the session is deleted from the server, so unsaved data is lost. And you need the Full Control permission to log off users other than yourself. Microsoft even suggests warning the user with the `msg` command before doing so.

## When the Session Does Not Go Away

Sometimes `logoff` hangs on a session that is stuck. In that case, reset it:

```powershell
rwinsta 3
```

The long form `reset session 3` does the same. Be aware that it is brutal, and anything unsaved in that session is lost.

You may also read about the `Get-RDUserSession` and `Invoke-RDUserLogoff` cmdlets. They only exist if the Remote Desktop Services role and its module are installed, which is not the case by default on Server Core. The two classic commands above work everywhere.

## Conclusion

A monthly password change is a good habit, but every forgotten session on a remote VM is a small time bomb that keeps retrying the old one. Now that I know `quser` and `logoff` work as well on Server Core as the Task Manager does elsewhere, cleaning up after a password change takes seconds, and my account stays unlocked.

## References

- [query user, Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/query-user)
- [logoff, Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/logoff)

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Diana on Pexels (`https://www.pexels.com/photo/close-up-of-red-padlocks-in-stone-wall-35908540/`).
