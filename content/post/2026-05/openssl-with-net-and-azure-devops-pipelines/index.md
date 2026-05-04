---
title: "OpenSSL With .NET And Azure DevOps Pipelines"
description: "We use OpenSSL for securing our websites or, more generally, to secure communication between services, tools and so on. While today the version to use is OpenSLL 3, you can find yourself needing a lower version."
image: 2026-05-04-the-word-secure-in-scrabble-letters.jpg
imageAlt: The word "Secure" in scrabble letters
date: 2026-05-04
categories:
  - Software Development
tags:
  - Security
---

Let’s be clear: you should always use the latest version of software, especially when it deals with security.

But in the example I’ll detail below, you can’t always bump the version with a snap of the fingers.

Let’s review what happened to me and how I solved it.

## The Context

I made a simple fix on a .NET Core 3.1 application. It had nothing to do with OpenSSL. A simple business rule needed to be removed.

So I did.

Then, on completing the pull request, the pipeline triggered a build. Within 15 seconds, its feedback returned KO with the error “**No usable version of libssl was found**” on a step called “Build Backend .NET”.

## The Reason

This error on an Azure DevOps pipeline is due to an incompatibility between the version of .NET used and the OpenSSL libraries on the build agent. Indeed, .NET Core 3.1 (used implicitly by my .NET publishing task) requires OpenSSL 1.x, but recent systems like Ubuntu 22.04 or above provide OpenSSL 3.0 or above by default.

So I checked my Linux distribution and yes, the pipeline used the latest Ubuntu 24.04.

In my research, I couldn’t find the real reason why, suddenly, the agent considered that it needed to use a recent version of Ubuntu.

## How Do I Solve the Issue

### Finding the Library

I researched how to get the OpenSSL 1.x library. After finding several dead links, I found [https://launchpad.net/ubuntu/+archive/primary/+files/libssl1.1_1.1.1f-1ubuntu2.23_amd64.deb](https://launchpad.net/ubuntu/+archive/primary/+files/libssl1.1_1.1.1f-1ubuntu2.23_amd64.deb) that worked.

I decided to download it because 2 out of 3 links were obsolete. Nothing told me the third one would stay valid forever.

But how can you use this specific file in the pipeline?

### Azure Pipeline Artifacts

Using the Azure Pipeline Artifacts, you can store files in the Git repository and load them into the context of the pipeline build.

For example, let’s say I placed the library in a folder `azure-pipelines-artifacts` at the repository’s root. Here are the steps I’d need to add to the YAML pipeline definition:

```yaml
- script: lsb_release -a
  displayName: "Check Linux version"

- publish: "azure-pipelines-artifacts" # Folder path containing the artifact in the Git repository
  artifact: "openssl-deb" # Artifact name (Warning: it is not the filename...)
  displayName: "Publish OpenSSL artifact"

- download: current
  artifact: openssl-deb # Published artifact name as named above
  displayName: "Download OpenSSL artifact"

- script: |
    sudo dpkg -i "$(Pipeline.Workspace)/openssl-deb/libssl1.1_1.1.1f-1ubuntu2.23_amd64.deb"
    sudo sed -i 's/openssl_conf = openssl_init/#openssl_conf = openssl_init/g' /etc/ssl/openssl.cnf
  displayName: "Install OpenSSL 1.1"

- script: ls -l /usr/lib/x86_64-linux-gnu/libssl.so.1.1
  displayName: "Check OpenSSL 1.1 installed"
```

The filename is the value `libssl1.1_1.1.1f-1ubuntu2.23_amd64.deb` in the ’Install OpenSSL 1.1` step above.

With that in place, the build succeeded on the step “Build Backend .NET”!

### Better Solution

I know I should upgrade the .NET target version, but it wasn’t possible due to budget constraints (a recurrent problem in software development). Still, if you’re like me, sometimes, you have to patch. I’m sure you’ll find this experience useful if you still use .NET 3.1 on your projects with the latest Azure DevOps.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by Miguel Á. Padriñán on Pexels.com.
