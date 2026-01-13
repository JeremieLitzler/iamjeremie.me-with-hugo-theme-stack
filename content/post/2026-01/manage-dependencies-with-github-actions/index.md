---
title: "How To Manage JavaScript Dependencies With GitHub Actions"
description: "It can be difficult and time consuming to update dependencies. GitHub Actions can help automate it."
image: 2026-01-05-steel-cogs.jpg
imageAlt: Steel cogs
date: 2026-01-05
categories:
  - Software Development
tags:
  - GitHub
  - DevOps
  - Continuous Integration
---

Using _Dependabot_ for npm package updates, you can automate your dependencies more efficiently.

For that, you’ll need to create a `dependabot.yml` file in your repository, in a `.github` directory at the project’s root. Here’s how to set it up.

## Create the File

To get started with Dependabot version updates, you’ll need to specify which package ecosystem to update and where the package manifest is located.

Create a file at `.github/dependabot.yml` and set the minimal configuration:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
```

This configuration:

- Uses version 2 of the Dependabot syntax
- Monitors npm packages specified in the `package.json` found at the root directory
- Checks for updates daily and create a PR on your repository if a package needs an update

But that’s not what you’d use. I use a custom configuration so let’s look at my example for advanced configurations, which works well if you followed the [steps of this previous article](../../2025-12/configure-ci-steps-with-github/index.md).

## Advanced Configuration

On my Vue and Supabase project template, I have set up my `dependabot.yml` as follows:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    # Location of package manifests, e.g. `package.json`
    directory: "/"
    # Provide a weekly update by email and create the PR based
    # what dependatbot finds. I think weekly interval is a sweet
    # spot to avoid overwelming daily notifications.
    schedule:
      interval: "weekly"
    # Add labels to pull requests to make dependabot PR stand-out
    labels:
      - "npm dependencies"
    # Allow up to 5 open pull requests to limit the PR opened.
    # I think it helps to avoid having as many PR as you have
    # dependencies in your porject, which can be a lot when you
    # work on a JavaScript project...
    open-pull-requests-limit: 5
```

When a package update exists, `dependabot` creates a branch and submits a new PR to merge the update to `develop`, if you followed the [steps of this previous article](../../2025-12/configure-ci-steps-with-github/index.md).

Consequently, it will also run the CI to check the project still builds.

## Wanna Learn More

Please head to [the documentation for all configuration options](https://docs.github.com/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file). You might find what you’re looking for your specific need.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/gray-scale-photo-of-gears-159298/).
