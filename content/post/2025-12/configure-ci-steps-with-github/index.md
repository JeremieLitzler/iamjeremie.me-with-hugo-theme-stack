---
title: "Configure CI Steps With GitHub"
description: "We call these steps GitHub Actions and they can improve and automate your workflows."
image: 2025-12-29-steel-cogs.jpg
imageAlt: Steel cogs
date: 2025-12-29
categories:
  - DevOps
tags:
  - GitHub
  - Continuous Integration
---

Early this year, I worked on a Vue and Supabase project template and I thought it’d be a good idea to automate a few steps, as the community accepts as best practices.

I’ll describe two of them to showcase how to use GitHub actions to perform those steps automatically when a triggering event occurs on my repository.

## Check that Code Builds

Often, we implement a best practice to have some automation to check that code pushed to a repository works for everyone.

Hence, when a programmer submits a pull request to merge his code modifications to the `develop` branch and to guarantee his branch builds with success, we trigger a build automatically and it’ll run the appropriate build command for the project.

On my project, I need to run `npm run build`.

### The Trigger

In GitHub actions, you define the trigger as follows.

```yaml
on:
  pull_request:
    branches:
      - develop
    types: [opened, synchronize, reopened]
```

It targets the `develop` branch in the context of a pull request. It triggers only on opened or reopened pull requests. It also triggers when some new code is pushed to the feature branch we want to merge to `develop` only while a pull request exists between the two. This latter use case often occurs when developers review each other's code and suggest code updates.

### The Steps

Next, we define the steps to run:

1. The **Checkout code** step pulls the repository’s code into the workflow runner.
2. The **Setup Node.js** step installs the latest LTS version of Node.js and enables npm caching for faster installs.
3. The **Install dependencies** step installs all required npm packages using `npm ci` for a clean, reproducible setup.
4. The **Run build** steps executes the project’s build process using `npm run build`.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "lts/*"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Run build
        run: npm run build
```

### Test It

Create a YAML file `pr-build.yml` containing the snippets described above into a folder `.github/workflows` at the root of your project.

Then push the feature branch and create a pull request. It should trigger the GitHub Action.

## Create a Semantic Release

This workflow requires a more complex setup, but I'll guide you through it, step by step as usual.

{{< blockcontainer jli-notice-tip "Stay tuned!">}}

I’ve planned an article about Semantic Realase topic in February 2026. It’ll complement well to this GitHub Action.

{{< /blockcontainer >}}

For now, let me comment in the YAML code below the important parts:

```yaml
# release.yml
name: Automatic Release
run-name: ${{ github.actor }} is automatically releasing 🚀

on:
  # The GitHub Action will run automatically on pushes to
  # the main branch for example, when you merge a pull request
  # from develop branch to the main branch.
  # It supposes that the develop and main branch are protected,
  # meaning that you cannot directly push to those branches without
  # going through a pull request.
  push:
    branches:
      - main

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    environment:
      # This is the name of your environment created under https://github.com/{user}/{repo_name}/settings/environments/
      # The name must match in the YAML code and the settings
      name: CI
    steps:
      # Using the enviroment secret variables defined in the
      # under https://github.com/{user}/{repo_name}/settings/environments/
      # we'll generate a token used to allow the semantic release
      # step to edit the CHANGELOG.md file on the release
      # creation (see step "Semantic Release" below)
      - name: "Generate token"
        id: generate_token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.GH_APP_ID }}
          private_key: ${{ secrets.GH_APP_KEY }}
      # Check out the code to be able to run the release
      # creation as it requires some npm packages
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: false
          fetch-depth: 0
          ref: ${{ github.event.pull_request.base.ref }}
      # Setting up Node LTS
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "lts/*"
          cache: "npm"
      # Make sure all the dependencies are ok and installed,
      # in particular the semantic release packages
      - name: "Installing dependencies"
        run: npm ci
      - name: "Verifying the signatures"
        run: npm audit signatures
      # Execute the semantic release creation
      - name: Semantic Release
        uses: cycjimmy/semantic-release-action@v4
        # We use the token generated on the first step here.
        env:
          GITHUB_TOKEN: ${{ steps.generate_token.outputs.token }}
```

Stay tuned for the full details to set up the project with a semantic release and configure it to your needs. The article is **scheduled for February 9, 2026**.

## Conclusion

You can do a lot more with GitHub Actions, but this is a good start!

What do you use GitHub Actions for your day-to-day tasks?

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/gray-scale-photo-of-gears-159298/).
