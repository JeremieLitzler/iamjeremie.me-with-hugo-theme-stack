---
title: "How to Bind Shortcuts on Multi-Desktop Windows 11"
description: "Windows 11 has no shortcut to jump to a virtual desktop by number. Here is how I picked an open source tool to add one, and the AutoHotkey script that gives me what I needed."
image: 2026-10-28-keys-A-L-T-aligned-on-salmon-color-background.jpg
imageAlt: Keys A-L-T aligned on salmon-color background
date: 2026-10-28
categories:
  - Tutorial
tags:
  - Windows 11
  - AutoHotkey
  - Virtual Desktops
  - Open Source
---

I wanted something simple: pressing a shortcut that lands me on the virtual desktop I needed activated. Windows 11 makes available virtual desktops, but no way to jump to one by its number or name.

Before writing a single line of code, I wanted to know whether someone had already solved this. Someone had, and this article explains how I chose the tool and how I set it up.

## What Windows 11 Gives You Out of the Box

According to the [Microsoft keyboard shortcuts page](https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec), the native shortcuts for virtual desktops are:

- `Win+Tab` to open Task view
- `Win+Ctrl+D` to create another desktop
- `Win+Ctrl+Right` arrow and `Win+Ctrl+Left` arrow to move between desktops
- `Win+Ctrl+F4` to close the current desktop

None of them jumps to a desktop by number. And let me tell you that, within 2 days of usage, I felt friction to perform `Win+Tab`, then `Tab` then the arrows to select the desktop and `Enter` to select it... The `Win+number` family looks promising, but it acts on apps pinned to the taskbar, not on desktops. So Task view stays a mouse or arrow-key affair, with no typed-number prompt.

## Why Every Tool Is a Bit Fragile

Microsoft documents only one COM interface for virtual desktops, [`IVirtualDesktopManager`](https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ivirtualdesktopmanager). It has three methods: `GetWindowDesktopId`, `IsWindowOnCurrentVirtualDesktop` and `MoveWindowToDesktop`. It cannot switch the active desktop, create one, remove one or list them. The same page even says applications should avoid switching the user from one desktop to another.

So every tool that switches by number relies on undocumented shell interfaces, and the repositories say so themselves. [`MScholtes/VirtualDesktop`](https://github.com/MScholtes/VirtualDesktop) states that Windows 11 23H2 build 3085 changed the COM GUIDs again and ships separate source variants per Windows version. [`Grabacr07/VirtualDesktop`](https://github.com/Grabacr07/VirtualDesktop) says the class IDs change between Windows versions. [`dankrusi/WindowsVirtualDesktopHelper`](https://github.com/dankrusi/WindowsVirtualDesktopHelper) warns that some builds may not fully work. That fragility shaped how I judged the candidates.

## How I Picked One Solution

I only trusted primary sources: official repositories, `README` files, example files, GitHub metadata and Microsoft documentation. Anything I could not confirm there was dropped or listed as a gap.

My need was specific. I wanted to switch native Windows 11 virtual desktops by number, on build 26200 (25H2), in a work and personal context. So I applied two filters. The `README` had to declare Windows 11 support, and the repository needed a release or a push within the last six months of my research date, 2026-10-21, so the cutoff was 2026-04-21.

Most candidates fell out quickly:

- MScholtes/VirtualDesktop declares Windows 11 and has a 24H2 variant, but its last release and push date from 2025-08-12.
- lu0/windows-desktop-switcher only documents Windows 10 and was last pushed in March 2025.
- GlazeWM and Komorebi are active, but they use their own workspaces instead of native desktops, and neither declares Windows 11 support. Komorebi's license also restricts work use.
- Grabacr07/VirtualDesktop and mzomparelli/VirtualDesktop are libraries without recent activity.
- SylphyHorn targets Windows 10 and has been dormant since 2022.

PowerToys has no virtual desktop switcher in its utility list. Keyboard Manager could, in theory, but no project documents that combination, so I did not count on it. The Windhawk mods I found are click-based or edge-based, and I could not read the mod pages directly, so I kept them out as well.

Two candidates survived. Windows Virtual Desktop Helper by dankrusi supports custom hotkeys such as `Ctrl + Alt + Shift + D1 = Desktop1`, but its `README` names Windows 10 and 11 without mentioning 24H2, 25H2 or build 26200.

[VirtualDesktopAccessor](https://github.com/Ciantic/VirtualDesktopAccessor) by Ciantic was the one. It is MIT licensed, its last push was on 2026-10-11, and its `README` says it requires at least 24H2 build 26100.2605 and was tested with 25H2 build 26200.8117. That is the only candidate that explicitly covers my build. It is a library, not an app, so I write the hotkeys myself in AutoHotkey, which suits me fine.

One disappointment: none of the tools I reviewed ships a typed-number prompt. My original idea of pressing a shortcut and then typing a desktop number would have to be built on top of `GoToDesktopNumber`. For now, direct hotkeys are enough.

## Why Alt and Not Fn

I first wanted to use the Fn key. On most keyboards, though, Fn is handled in the keyboard firmware, so it is invisible to Windows and AutoHotkey. Alt stands in for it. My three desktops are named Bureautique, Dev and SQL, and they answer to Alt+Q, Alt+W and Alt+E.

## Setting It Up

You need three things:

- Windows 11 24H2 build 26100.2605 or later.
- AutoHotkey v2, from the [official download page](https://www.autohotkey.com/download/). The page lists 2.0.30 as the latest stable version at the time of writing and notes that browsers sometimes flag the download falsely.
- `VirtualDesktopAccessor.dll` from the [project releases](https://github.com/Ciantic/VirtualDesktopAccessor/releases). The latest release, tagged `2024-12-16-windows11`, has a single asset with that name.

Once you've gathered all those, install AutoHotkey v2 with the defaults. Then create a folder such as `C:\Tools\vda` and drop the DLL in it. The script expects the DLL next to itself.

The release DLL dates from December 2024, while the `README`'s 25H2 test comes from the current source. I confirmed the setup works on build 26200. If `LoadLibrary` fails or every call returns -1 on your machine, you should build the DLL from the repository source instead (which I haven't tried). The `README` gives no build instructions, but the repository contains a Rust crate. With AI, cloning the repo and asking an agent to look at it may be enough to rebuild the DLL if the need appears someday.

Then, save the following as `C:\Tools\vda\desktops.ahk`. Desktop numbers are zero-based in the project's example, so Bureautique is 0, Dev is 1 and SQL is 2.

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force
SetWorkingDir(A_ScriptDir)

; Same folder as the script
hVDA := DllCall("LoadLibrary", "Str", A_ScriptDir . "\VirtualDesktopAccessor.dll", "Ptr")
if (!hVDA) {
    MsgBox("Cannot load VirtualDesktopAccessor.dll from " A_ScriptDir)
    ExitApp
}

GetDesktopCountProc := DllCall("GetProcAddress", "Ptr", hVDA, "AStr", "GetDesktopCount", "Ptr")
GoToDesktopNumberProc := DllCall("GetProcAddress", "Ptr", hVDA, "AStr", "GoToDesktopNumber", "Ptr")
CreateDesktopProc := DllCall("GetProcAddress", "Ptr", hVDA, "AStr", "CreateDesktop", "Ptr")
SetDesktopNameProc := DllCall("GetProcAddress", "Ptr", hVDA, "AStr", "SetDesktopName", "Ptr")

GetDesktopCount() {
    global GetDesktopCountProc
    return DllCall(GetDesktopCountProc, "Int")
}

GoToDesktopNumber(num) {
    global GoToDesktopNumberProc
    DllCall(GoToDesktopNumberProc, "Int", num, "Int")
}

SetDesktopName(num, name) {
    global SetDesktopNameProc
    nameUtf8 := Buffer(1024, 0)
    StrPut(name, nameUtf8, "UTF-8")
    return DllCall(SetDesktopNameProc, "Int", num, "Ptr", nameUtf8, "Int")
}

; Make sure three desktops exist, then name them
while (GetDesktopCount() < 3) {
    DllCall(CreateDesktopProc, "Int")
}
SetDesktopName(0, "Bureautique")
SetDesktopName(1, "Dev")
SetDesktopName(2, "SQL")

; Alt+Q, Alt+W, Alt+E
!q:: GoToDesktopNumber(0)
!w:: GoToDesktopNumber(1)
!e:: GoToDesktopNumber(2)
```

The script creates missing desktops on startup, so you do not even need to press `Win+Ctrl+D` beforehand. Double-click the file and a green H icon appears in the notification area. Press `Alt+W` and you should land on Dev. Open Task view with `Win+Tab` to see the desktop names.

To start it at sign-in, press Win+R, type `shell:startup` and press Enter, then create a shortcut to `desktops.ahk` in that folder. It seems that it doesn't work all the time, though. So in my case, I run the `Windows+R`and type `C:\Tools\vda\C:\Tools\vda\desktops.ahk` which shows up in my history as I type the disk letter.

## Things to Watch

`Alt+letter` combinations are also used as menu mnemonics in some applications. While the script runs, the AutoHotkey hotkey takes priority, so those in-app shortcuts stop working for Q, W and E. If that matters to you, pick another modifier combination.

Hotkeys also match the character on your layout. On an AZERTY keyboard, Q, W and E sit in different physical positions than on QWERTY. To bind physical positions instead, use scan codes in the hotkey definitions.

According to the `README`, the names set by `SetDesktopName` work on Windows 11 only, and every function returns -1 on error. My script does not check return values. I have confirmed that names survive a restart of Explorer or Windows. However, I have yet to see if the DLL survives after the next Windows update: I have not tested it yet.

Finally, remember that the COM interfaces behind all this are undocumented. A Windows update can break the DLL until the project ships a fix.

## Conclusion

Windows 11 will not let you jump to a desktop by number, and every tool that adds the feature leans on interfaces Microsoft has never documented. That is why I judged candidates on one question: does the `README` explicitly cover my build, and is the project alive? Only `VirtualDesktopAccessor` passed both tests. Fifty lines of AutoHotkey later, `Alt+Q`, `Alt+W` and `Alt+E` take me where I want to go in a snap. After the next Windows update, I will run the script again and see whether it still holds.

If you liked this article…

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo de Miguel Á. Padriñán (`https://www.pexels.com/fr-fr/photo/clavier-mot-boutons-saisir-2882505/`)
