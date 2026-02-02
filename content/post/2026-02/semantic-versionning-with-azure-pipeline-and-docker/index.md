---
title: "Semantic Versionning with Azure Pipeline and Docker"
description: "This is a solution, not the solution. And it works nicely as a first step toward semantic versionning automation."
image: 2024-07-24-logos-ms-azure-and-python.jpeg
imageAlt: "Logos of Microsoft Azure and Python"
date: 2026-02-02
categories:
  - Software Development
tags:
  - Azure DevOps
  - Docker
  - Versionning
---

When it comes to versioning an application, there are many ways to go about it. [JetBrains names its software version](https://blog.jetbrains.com/blog/2016/03/09/jetbrains-toolbox-release-and-versioning-changes/) `yyyy.r.n.m` to get something like `2024.1.6.30` for example.

I have used the [semantic version style](https://semver.org/) myself more than a custom versionning style.

On a project using Azure Pipelines to build and Docker to create the deployed container, I came at a point where I needed to deal with that.

Here’s how I went about solving the task of automating the process.

## Starting Point

I had this `version` controller:

```python
from flask import Blueprint, jsonify

version = Blueprint("version", __name__)

version_value = '1.2.6'

@version.route("/", methods=["GET"])
def get_version():
    response = {
        "version": version_value
    }
    return jsonify(response)
```

It was simple but manual.

I needed the version to include the `build` value (the fourth value in the version: `{major}.{minor}.{patch}.{buildId}`) automatically from the build running on the Azure pipeline.

The major, minor or patch values would update manually as we follow the semantic versionning rules.

The version update happens on the build against the `develop` branch.

It shouldn’t happen when the build runs against the `main` or `release` branch.

The question:

- where to store the major, minor or patch values?
- how to tell the controller where to get the full version?

## Updating the Code

First I needed to update the Python code quoted above.

My idea was to use a text file in the same directory as the controller.

The file could be empty, but in my case, I use the opportunity to use it as documentation.

The controller would simply read the content and the frontend would call the controller at the root action to get the value and display it.

The code changed to:

```python
import os

from flask import Blueprint, jsonify

version = Blueprint("version", __name__)

def get_version_from_file():
    version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
    with open(version_file, 'r') as file:
        return file.read().strip()

@version.route("/", methods=["GET"])
def get_version():
    response = {
        "version": get_version_from_file()
    }
    return jsonify(response)
```

Locally, you can still see the version displayed with whatever value written in the file.

## Updating the Pipeline

Next, which pipeline to update? Why “which pipeline”?

Well, I’ve learned that it is best to seperate the Pull Request Validation pipeline (which runs tests) from the actual Application Build pipeline (which will publish the built Docker image in a Container Registry). It applies the seperation of concerns principle, even if the task is more a DevOps task than a software task.

The target pipeline in this step is the Application Build pipeline.

In my example, the pipeline contained:

- a step to set image tag, which is different whether I build on `develop` or on `main` (the details of that is out of the scope here)
- a step to build and push the Docker image

I can tell you we need two steps between the original ones:

- a step to get the next version
- a step to update the next version so it is persisted somewhere.

Why? Because you want to the version value to be the same.

## Updating the Dockerfile

### Beyond the Basics

Now, Semantic versionning says:

> - Patch version Z (x.y.Z | x > 0) MUST be incremented if only backward compatible bug fixes are introduced. A bug fix is defined as an internal change that fixes incorrect behavior.
> - Minor version Y (x.Y.z | x > 0) MUST be incremented if new, backward compatible functionality is introduced to the public API. It MUST be incremented if any public API functionality is marked as deprecated. It MAY be incremented if substantial new functionality or improvements are introduced within the private code. It MAY include patch level changes. Patch version MUST be reset to 0 when minor version is incremented.
> - Major version X (X.y.z | X > 0) MUST be incremented if any backward incompatible changes are introduced to the public API. It MAY also include minor and patch level changes. Patch and minor versions MUST be reset to 0 when major version is incremented.

So we can go further and say that:

- if my branch is named `bug/docker-image-not-building`, hence containing the prefix `bug`, then, I bump the `patch` version.
- if my branch is named `feature/add-awesome-ai-chatbot`, hence containing the prefix `feature`, then, I bump the `minor` version.
- if my branch is named `next/generation-api-v2`, hence containing the prefix `next`, then, I bump the `major` version.

I’m sure that’s possible but it would mean to perform this on the Pull Request buidl because you have access to the source branch.

Another option a colleague of mine shared is to look at the commit messages since the last release:

- if at least one commit contains `fix`, `refactor`, `chore`, `style`, then, I bump the `patch` version.
- if at least one commit contains `feat`, then, I bump the `minor` version.
- if at least one commit contains `BREAKING CHANGE`, then, I bump the `major` version.
- otherwise the build is bumped (for new documentation, CI changes)

I won’t dive into this in this article because I haven’t done it (yet). In a later article, I’ll showcase how I did it with a Vue project, some handy package and GitHub Actions.

### What Did Change In My Dockerfile

I added the following:

```dockerfile
# After setting timezone...
# Accept VERSION as a build argument
ARG VERSION

# ...

# After getting all sources into the project container...
# Update the version file
RUN echo "Version is <$VERSION>"
RUN echo $VERSION > /project-container/app/modules/version/version.txt
```

where `$VERSION` is a parameter passed to the `docker build` command.

### Updating the pipeline

In the YAML file, we need to make the build step and publish step are separate. I learned the hard way that the built-in step "_Build and Publish_" couldn’t care less for the parameters passed on and therefore, it ignores any value silently.

So the steps look like that:

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
    arguments: --build-arg VERSION=$(setVersionStep.fullVersion)

- task: Docker@2
  displayName: Push image to container registry
  inputs:
    command: push
    repository: $(imageRepository)
    containerRegistry: $(dockerRegistryServiceConnection)
    tags: |
      $(imageTags)
```

Of course, you can name the parameter whatever you want, but make sure the name in `arguments: --build-arg VERSION=$(setVersionStep.fullVersion)` matches the variable name in the `Dockerfile`.

Have you learned something? Is there anything unclear or you saw a typo? [Tell me](https://iamjeremie.me/page/contact-me/) !

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
