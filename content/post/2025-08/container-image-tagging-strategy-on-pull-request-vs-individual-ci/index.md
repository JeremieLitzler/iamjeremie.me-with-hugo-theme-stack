---
title: "Container Image Tagging Strategy On Pull Request vs. Individual CI"
description: "Usually, we have a QA environment before pushing an application update to production. Let’s see to handle the creation of a Docker image for each environment in Azure DevOps."
image: 2025-08-18-a-container-ship-going-towards-the-sunrise.jpg
imageAlt: A container ship going towards the sunrise.
date: 2025-08-18
categories:
  - Software Development
tags:
  - DevOps
  - Microsoft Azure
  - Docker
  - Containers
---

Let’s say you have:

- a Python REST API and you uses Docker to containerize it.
- two environments (Production and QA) on Azure Cloud Services.
- a DevOps pipeline that builds and push the Docker image to a Container Registry on Azure and tag the latest image with _latest_ tag.

Next, you have a DevOps branch policy to trigger a build pipeline on:

- an Individual CI trigger when something is pushed to `main`.
- a Pull Request (PR) trigger where you want to merge into `main`.

With the above, the result is that DevOps creates an image tagged `latest` on both triggers.

Wouldn’t it be better to distinguish the two builds and be able to test the PR build on the QA environment?

Yes, it would.

Here is how to modify the pipeline.

## Modifiy the Pipeline

To begin, let’s define the need:

- on a PR trigger, we want to push an image tagged `ready-for-qa`.
- on a Merge Request or Individual CI on `main`, we want to push an image tagged `latest`.

Next, you need to define a variable in the `azure-pipelines.yml` file:

```yaml
variables:
  # Custom variable for build trigger tagging
  isPullRequest: $[eq(variables['Build.Reason'], 'PullRequest')]
```

You’ll use it in the bash script that allows defining in which scenario the build falls into.

Under the _stages > jobs > steps_ section, you should have one step:

```yaml
- task: Docker@2
  displayName: Build and push an image to container registry
  inputs:
    command: buildAndPush
    repository: $(imageRepository)
    dockerfile: $(dockerfilePath)
    buildContext: $(projectPath)
    containerRegistry: $(dockerRegistryServiceConnection)
    tags: |
      $(tag)
      latest
```

Let’s modify this in three steps:

1. Define the image tag.
2. Build and push an image to container registry with the `ready-for-qa` tag.
3. Push latest tag for non-PR builds

### Define The Image Tag Variable

Under the steps, add a new step of type `bash`:

```yaml
- task: Bash@3
  displayName: Set image tag
  inputs:
    targetType: "inline"
    script: |
      if [ "$(isPullRequest)" = "True" ]; then
        echo "##vso[task.setvariable variable=imageTag]ready-qa"
      else
        echo "##vso[task.setvariable variable=imageTag]$(Build.BuildId)"
      fi
```

The script checks the variable `isPullRequest`.

Then, if it’s true, it creates and sets a variable `imageTag` to `ready-for-qa`.

Otherwise, it sets the variable to the build identifier.

### Build And Push An Image To Container Registry With The `ready-for-qa` Tag

This step is actually the same as the original step except for the tags.

So instead of:

```yaml
tags: |
  $(tag)
  latest
```

We have:

```yaml
tags: |
  $(imageTag)
```

### Build and Push Latest Tag for non-PR Builds

Finally, here is the last step.

You see that it’s almost the same as the original single step but we added a condition to decide whether or not to run it:

```yaml
condition: and(succeeded(), ne(variables['Build.Reason'], 'PullRequest'))
```

Basically, if the build succeeds and that the `Build.Reason` isn’t `PullRequest`, then it will run.

Otherwise the pipeline skips it.

## Modifiy the Container App resource

Once you see the `ready-for-qa` tag appear in the Container Registry, you simply to create a revision of your Container App configuration on the QA environment.

Under the section _Image_, select the image and select the tag `ready-to-qa`.

Make sure to click _Save_ and _Create_.

After a couple of minutes, check the _Revisions and replicas_ blade under the _Application_ menu blade. If all is green, go ahead and test your application.

## Another Alternative

Though this works, I have implemented another workflow that relies on a `main` branch for production builds and `develop` for QA builds. Then, we don’t rely on the type of CI (e.g., `Individual CI` vs. `Pull Request`) but on the branch name.

You can read [this article describing the steps to configure the pipeline in such a way](../configure-docker-image-in-azure-devops/index.md).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/boat-in-body-of-water-262353/).
