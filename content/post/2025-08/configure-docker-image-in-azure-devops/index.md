---
title: "Configure Docker Image Tagging in Azure DevOps"
description: "Usually, we have a QA environment before pushing to production. Let’s see to handle Docker image tagging with Azure DevOps."
image: 2025-08-11-a-man-jumping-on-a-container.jpg
imageAlt: A man jumping on a container
date: 2025-08-11
categories:
  - Software Development
tags:
  - DevOps
  - Microsoft Azure
  - Docker
  - Containers
---

Let’s say you have:

- a Python REST API and you use Docker to containerize it.
- two environments (Production and QA) on Azure Cloud Services.
- a DevOps pipeline that builds and push the Docker image to a Container Registry on Azure and tag the latest image with _latest_ tag.

Next, you have a DevOps branch policy to trigger a build on an Individual CI trigger when something is pushed to `main` or `develop`.

With the above, the result is that DevOps creates an image tagged `latest` on both triggers.

Wouldn’t it be better to distinguish the two Docker image created and be able to test the build from the `develop` branch on the QA environment?

Yes, it would.

Here is how to modify the pipeline.

## Modifiy the Pipeline

To begin, let’s define the need:

- on a Merge Request or Individual CI on `develop`, we want to push an image tagged `ready-for-qa`.
- on a Merge Request or Individual CI on `main`, we want to push an image tagged `latest`.

First, you need to define the trigger in the `azure-pipelines.yml` file:

```yaml
trigger:
  branches:
    include:
      - main
      - develop
```

Next, let’s evaluate the image tag. You’ll use it in the bash script.

Under a `Build and  push` stage, add a `Build` job and a `bash` step where you evaluate the container tag:

```yaml
- task: Bash@3
  displayName: Set image tags
  inputs:
    targetType: "inline"
    script: |
      if [ "$(Build.SourceBranch)" = "refs/heads/develop" ]; then
        echo "##vso[task.setvariable variable=imageTags]ready-qa"
      elif [ "$(Build.SourceBranch)" = "refs/heads/main" ]; then
        echo "##vso[task.setvariable variable=imageTags]$(Build.BuildId),latest"
      else
        echo "##vso[task.setvariable variable=imageTags]$(Build.BuildId)"
      fi

  name: setImageTagsStep
```

Let’s then modify the next steps to build and push an image to the container registry with the computed image tags:

```yaml
- task: Docker@2
  displayName: Build image
  inputs:
    command: build
    repository: $(imageRepository)
    dockerfile: $(dockerfilePath)
    buildContext: $(projectPath)
    containerRegistry: $(dockerRegistryServiceConnection)
    tags: |
      $(imageTags)

- task: Docker@2
  displayName: Push image to container registry
  inputs:
    command: push
    repository: $(imageRepository)
    containerRegistry: $(dockerRegistryServiceConnection)
    tags: |
      $(imageTags)
```

The `build` and `push` are split because, in the case that you build a container and pass it an application version number, the build phase will take an argument with the computed version. The step `buildAndPush` that Azure provides doesn’t allow argument.

I’ll demonstrate this in a future article.

## Conclusion

This approach is an opinionated approach, but it worked well for me. You could possibly perform a similar outcome in a different way.

If you like my approach…

{{< blockcontainer jli-notice-tip "Follow me">}}

Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Kaique Rocha](https://www.pexels.com/photo/man-jumping-on-intermodal-container-379964/).
