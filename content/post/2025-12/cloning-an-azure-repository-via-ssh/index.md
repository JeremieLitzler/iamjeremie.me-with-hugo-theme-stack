---
title: "Cloning a Repository from Azure With A SSH Key"
description: "Cloning a repository may seem easy if you have credentials with a password, but you don’t always can."
image: 2025-12-01-someone-handing-over-a-key.jpg
imageAlt: Someone handing over a key
date: 2025-12-01
categories:
  - Tools
tags:
  - Azure DevOps
---

Using an SSH Key to clone a repository can be the only way you have sometimes.

Let's see how it works and what is the little caveat about it.

## Recommended Key Types

The two most popular SSH key generation algorithms are:

- **RSA**: Widely supported though less secure.
- **Ed25519**: More cryptographically strong, recommended for modern systems

{{< blockcontainer jli-notice-warning "Some systems don’t support the `Ed25519` type.">}}

{{< /blockcontainer >}}

## Generating an SSH Key

Open a terminal and run:

```bash
# Browse to the user root
cd

# Create .ssh directory and browse to it
mkdir .ssh
cd .ssh

# Choose the version depending on the system where you want to use it
# For the latest security
bashssh-keygen -t ed25519 -C "your_email@example.com"

# Or for broader compatibility
bashssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy the public key. You'll need to add to the repository settings or your versioning system.
cat id_rsa.pub # or whatever you named your key.
```

## Key Generation Process

1. When prompted to “Enter file in which to save the key”, press Enter to accept the default location or type your key name (for ex. `id_rsa_my_great_app`).
2. You’ll be asked to enter a passphrase:
   - **Recommended**: Add a passphrase for extra security
   - **Optional**: Press Enter to skip passphrase

## Key Location

The default location will be the current directory where you run the command of key creation. It’s recommended to generate the keys into `.ssh` folder.

## After Generation

A **private key** and **a public key** will be created.

The public key file will have a **`.pub`** extension.

**Keep your private key secret and secure**.

## Next Steps

Use the public key (for example **`id_rsa_my_great_app.pub`**) when setting up SSH access on services like Azure DevOps, GitHub, GitLab, or remote servers.

For example in Azure DevOps:

![Screenshot of a Azure DevOps project](with-azure-devops.png)

1. Click “SSH Public Keys” menu from the top right menu.
2. You should land in “SSH Public Keys” page.
3. Add a new key through “New Key” and name the key and paste the public key.

You can view the public key content using: `cat ~/.ssh/id_rsa_my_great_app.pub`.

## Caveat: Registration of SSH Key

The issue that could happen is that, in the case of Azure DevOps, the SSH key isn’t used to accept any Git command.

In on many repositories, you can clone using HTTPS and SSH:

![Screenshot of a GitHub project](with-github.png)

Using HTTPS usually requires login and password credentials. With Azure DevOps, you can’t always do that.

Using SSH requires the SSH keys: the public key is known to the server and you hold the private key.

I ran into an issue where, even though the server knew the public key, the Git command to clone wouldn’t pick up the SSH key.

To solve that, you have to explicitly tell the SSH client to register the new key created:

```bash
# Start the SSH Agent
eval "$(ssh-agent -s)"
# Register a SSH key
ssh-add ~/.ssh/your_private_key
```

In case you need to run this often, add a Git alias:

```bash
# In your .gitconfig file located in /c/Users/YourUser directory
[alias]
    ssh = ! eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa_devops_my_project
```

That’s it for today.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Thirdman](https://www.pexels.com/photo/shadow-of-a-hand-holding-a-key-on-wall-8470839/).
