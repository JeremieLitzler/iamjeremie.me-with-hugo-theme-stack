---
title: "Custom Retention Policy for Docker Images On Azure Container Registries"
description: "On Microsoft Azure, cost management is a day-to-day job. I’ll take an example with a Container Registry and the retention policy to keep only the last 10 images."
image: 2025-03-10-lots-of-containers.jpg
imageAlt: Lots of steel containers
date: 2025-03-10
categories:
  - Web Development
tags:
  - Microsoft Azure
  - Docker
  - Container Registries
  - Python
---

On a [Python](../../../tags/python/) project last year, I had set up an Azure DevOps pipeline with the logic to build a Docker image of a Python web application with the following logic:

- When a feature was developed, I would pull a branch from the `develop` and make the modification.
- When I finished the feature, I’d create a PR to merge that feature into the `develop`.
- Once the PR was merged, the branch policy of `develop` would trigger the pipeline to run and build a `ready-qa` tagged image to deploy to the testing environment in Azure.
- After QA testing, I’d merge `develop` to `main`, triggering another build and tag a new image with the value `latest`. It’d be the image to deploy to the production environment on Azure.

This created a lot of Docker images because, in addition to the `ready-qa` or `latest`, I’d have a `{build_id}` tag for each run.

In consequences, the Container Registry cost the most in all the resources provisioned to Azure. And the Docker image list would built up over time.

How could I improve by cleaning up the older and useless Docker images?

## Brainstroming

The first solution would be to upgrade the _Container Registry_ to a premium one to define a retention policy.

I didn’t want that.

I knew I wanted to keep all non-numeric tags because I had only one of each.

But I could delete all but the last 10 numerically tagged images.

That's when I thought about the Azure CLI.

## The Script

I ask Claude AI to help me out with this.

First, I wondered how to list the numeric tags I wanted:

```bash
# List repositories
az acr repository list --name <registry-name> --output table

# List tags for a specific repository
az acr repository show-tags --name <registry-name> --repository <repository-name> --orderby time_asc --output table

# Delete a specific image
az acr repository delete --name <registry-name> --image <repository-name>:<tag> --yes
```

This worked well, but as I had dozens of images to delete, I wanted to make efficient.

My requirements were:

- provide the _Container Registry_ as a required input.
- provide an option to _dry run_ the script.
- provide the ability to configure the number of numeric tags to keep.
- ignore the non-numeric tags from deletion.

The first suggestion was to use a Python script. But it required to be connected to Azure. It required more work.

However, I knew I could run a bash script in the Azure CLI console, here is the script that achieves that:

```bash
#!/bin/bash

# Function to check if a string is numeric
is_numeric() {
    [[ $1 =~ ^[0-9]+$ ]]
}

# Help function to display script usage
usage() {
    echo "Usage: $0 <registry_name> [--dry-run]"
    echo "  <registry_name>: The name of your Azure Container Registry"
    echo "  --dry-run: Optional. If set, no actual deletions will occur"
    exit 1
}

# Check if registry name is provided
if [ $# -eq 0 ]; then
    echo "Error: Registry name is required."
    usage
fi

# Set variables
REGISTRY_NAME=""
echo "Retaining the last $RETENTION_COUNT tags... To change that, edit the constant RETENTION_COUNT in the script"
RETENTION_COUNT=10
DRY_RUN=0

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        *)
            if [ -z "$REGISTRY_NAME" ]; then
                REGISTRY_NAME="$1"
            fi
            shift
            ;;
    esac
done

# Check if registry name is not null or empty
if [ -z "$REGISTRY_NAME" ]; then
    echo "Error: Registry name cannot be null or empty."
    usage
fi

# Verify if the registry exists
if ! az acr show --name "$REGISTRY_NAME" &>/dev/null; then
    echo "Error: Registry '$REGISTRY_NAME' not found or you don't have access to it."
    exit 1
fi

echo "Processing Azure Container Registry: $REGISTRY_NAME"
if [ $DRY_RUN -eq 1 ]; then
    echo "DRY RUN: No actual deletions will occur"
fi

# Get list of repositories from registry
repositories=$(az acr repository list --name $REGISTRY_NAME --output tsv)

for repo in $repositories; do
    echo "Processing repository: $repo"

    # Get all tags for the repository
    tags=$(az acr repository show-tags --name $REGISTRY_NAME --repository $repo --orderby time_desc --output tsv)

    # Initialize counters
    numeric_count=0

    # Remove the images...
    for tag in $tags; do
        if is_numeric "$tag"; then
            ((numeric_count++))

            if [ $numeric_count -gt $RETENTION_COUNT ]; then
                if [ $DRY_RUN -eq 1 ]; then
                    # dry run = just print out a message
                    echo "Would delete tag: $repo:$tag"
                else
                    # Real deal = delete the image
                    echo "Deleting tag: $repo:$tag"
                    az acr repository delete --name $REGISTRY_NAME --image "${repo}:${tag}" --yes
                fi
            fi
        else
            echo "Keeping non-numeric tag: $repo:$tag"
        fi
    done
done
```

The AI made a mistake on the `--dry-run` implementation when checking it. In bash, you check a boolean with:

```bash
if [ $MY_BOOLEAN -eq 1 ]; then
	# do something
fi
```

At first, it told me the following, which isn’t proper bash syntax:

```bash
if [ "$DRY_RUN" = true ]; then
	# do something
fi
```

## Beyond A Bash Script

I’d love to run this regularly without me thinking about it. Is the time to build that worth the cost?

Is the cost of a Premium Container Registry higher?

A few weeks following this initial Bash script, I’ve found how to do it. I’ll give you a hint: _Runbook_.

To be continued...

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Tom Fisk](https://www.pexels.com/photo/aerial-photography-of-container-van-lot-3063470/).
