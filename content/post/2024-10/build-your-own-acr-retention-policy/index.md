---
title: "Build Your Own ACR Retention Policy"
description: "Costs on Azure can add up and before you know it, the bill will hurt you. Here is my take on managing container images retention in an Azure Container Registry."
image: images/2024-10-01-complex-music-box.jpg
imageAlt: Complex music box
date: 2024-10-01
categories:
  - Web Development
tags:
  - Microsoft Azure
---

## The Need

I worked on a Python project deployed to Azure and the app was containerized.

After a few months, we noticed that the most expensive resource among a set of container registry, container apps, key vaults and storage accounts was the first resource listed.

Originally, I coded a Bash script to run manual cleanup of all tagged images with the build number.

The usage was simple:

- you open [the Azure portal](https://portal.azure.com/) on the company tenant.
- you open the Azure CLI from the first icon on the left on the top right menu.
- you create a `shell` script and copy the content of the script using Nano.
- you adjust the constant `RETENTION_COUNT`, if needed. It’s set to 10 in the versioned script.
- run it with a dry run first:

  ```bash
  bash acr_custom_retention_policy.sh <registry_name> --dry-run
  ```

- run it without a dry run to delete permanently images:

  ```bash
  bash acr_custom_retention_policy.sh <registry_name>
  ```

However, I wanted to challenge this by automating it.

## Solutions possible

You have several solutions and not all of them can work for you, depending on your permissions on Microsoft Azure:

1. Azure DevOps Pipeline: you can define a new pipeline in DevOps with a few manageable variables (ACR name and dry run option in my use case) and use the schedules to run the pipeline on a recurring basis.
2. Azure Automation: this service enables you to schedule and run PowerShell scripts or Python _runbooks_.
3. Azure Logic Apps: this could work, but might be overly complex for a simple script execution. As you’d need to create a Logic App with a recurrence trigger and use the Azure CLI action to run the script.
4. Azure Container Instances: you could containerize the script and schedule it to run periodically using Azure Container Instances.

I chose the Azure Automation over Azure DevOps Pipeline since I lacked the permission to use that first option in particular the Service connection creation). The other two seemed overkill for my need.

The best option depends on factors like the type of script you’re running, its complexity, and your specific requirements.

## Create the Automation Account

On the Azure portal, search for _Automation Accounts_ and create a new one following the naming guideline from Microsoft.

Apart from the name and region, that followed the value selected for the existing resources of the project, I left the settings with their default.

Once created, you need to give the `AcrDelete` and `Reader` role-based permission to the _System assigned_ Object ID for the automation account.

## Configure Permissions Between the _Container Registry_ and the _Automation Account_

Now, go to the Container Registry and under the _Access control (IAM)_ blade, add a role:

- search for `AcrDelete` role and select it
- click the _Members_ tab, select _Managed identity_ and click _Select members_
- on the right pane, you will see a form with a managed identity input. Select from the drop-down the _All system-assigned managed identities_, which is the default when you created the _Automation account_.
- select the _Automation Account_ you created earlier and confirm selection with the button _Select_
- finally, click twice _Review + assign_.
- repeat the steps above to add `Reader` role.

## Craft Your Script Before You Set Up The _Runbook_ With It

In my case, I went to the documentation page for `**Get-AzContainerRegistryTag**` ([found here](https://learn.microsoft.com/en-us/powershell/module/az.containerregistry/get-azcontainerregistrytag?view=azps-12.3.0)) and I selected the _Open Cloud Shell_ in the example section.

You will need to set up an account or log-in to an existing one and complete the _Microsoft Learn_ form.

Then, when the cloud shell opens, you’ll want to switch to PowerShell (see top left of the cloud shell window) instead of using Bash.

There you can test a single command or upload your crafted `.ps1` from your computer. It was helpful for me.

## Create the _Runbook_ With PowerShell

Back the _Automation Account_, navigate to the blade _Process Automation >_ _Runbooks_. Then:

- create a _PowerShell runbook_:
- give it a name (e.g., “ACR-Retention-Policy”)
- choose “PowerShell” as the _runbook_ type
- choose version 7.2 or above
- confirm creation with a click on _Review + Create_

## Code the _Runbook_ Script With PowerShell

Once the _runbook_ is created, go to the _Overview_ blade and select _Edit > Edit in Portal_. A code editor opens.

Paste your script, save it and publish it.

Before putting a schedule on it, run it by clicking _Start_ from the _Overview_ blade.

Once you’re happy and that the script ran as expected,

- go to the the _Resources > Schedules_ blade while in your _Runbook_ resource.
- click _Add a schedule_
- click _Link your runbook to a schedule_
- click _Add a schedule_ again (not the same as the first instance…)
- on the right pane that opened, name your schedule, describe it and set up your schedule start date and time and the recurrence.
- click _Create_ and select the schedule and click _OK_ at the bottom left to link it to the runbook.

Now, wait for the schedule to run and check the run result.

## Caveat About the PowerShell Option

When I finally tested the _runbook_ set up above, it turned out that the `Remove-AzContainerRegistryTag` command doesn’t actually delete the image with the numeric tag…

The only programmatic way was to use the Azure CLI command. But how could I run the job so that it could work just like the Bash script?

I went and created a second _runbook_ using Python as the runtime engine.

## Code the _Runbook_ With Python

Back the _Automation Account_, navigate to the blade _Process Automation >_ _Runbooks_. Then create a _Python runbook_ like so:

- give it a name (e.g., “ACR-Retention-Policy”)
- choose “Python” as the _runbook type_
- choose version 3.8 or above (at the time of writing, 3.8 was recommended).
- confirm creation with a click on _Review + Create_

## Configure the _Runbook_ With Necessary Packages

The equivalent script in Python uses a few packages from Microsoft:

- [`azure.identity`](https://pypi.org/project/azure-identity/#files)
- [`azure.common`](https://pypi.org/project/azure-common/#files)
- [`azure.core`](https://pypi.org/project/azure-core/#files)
- [`azure.mgmt.core`](https://pypi.org/project/azure-mgmt-core/#files)
- [`azure.containerregistry`](https://pypi.org/project/azure-containerregistry/#files)

To install the package, you need to use the links above and download the `.whl` file for each and go to the _Shared Resources > Python Packages_ blade.

Click _Add a Python package_.

Then select the `.whl` file and select the same _Runtime version_ as the one selected on the _runbook_ creation.

Importing the package will take time, so go get a coffee or take a short walk and come back.

## Code the Runbook Script With Python

I converted the manual and original Bash script to a Python script.

```python
#!/usr/bin/env python3

import sys
from azure.identity import ManagedIdentityCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.containerregistry import ContainerRegistryClient
from azure.core.exceptions import ResourceNotFoundError

def is_numeric(string):
    return string.isdigit()

def cleanup_acr(registry_name, retention_count=3, dry_run=False):
    print(f"Processing Azure Container Registry: {registry_name}")
    if dry_run:
        print("DRY RUN: No actual deletions will occur")

    # Create a Managed Identity credential
    credential = ManagedIdentityCredential()

    # Create a management client
    mgmt_client = ContainerRegistryManagementClient(credential, subscription_id)

    try:
        # Get the registry
        registry = mgmt_client.registries.get(resource_group_name, registry_name)
    except ResourceNotFoundError:
        print(f"Error: Registry '{registry_name}' not found or you don't have access to it.")
        return
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

    # Create a ContainerRegistryClient
    registry_client = ContainerRegistryClient(f"https://{registry_name}.azurecr.io", credential)

    # List repositories
    for repository in registry_client.list_repository_names():
        print(f"Processing repository: {repository}")

        # Get all tags for the repository
        tags = list(registry_client.list_tag_properties(repository))

        # Sort tags by creation time in descending order
        tags.sort(key=lambda x: x.created_on, reverse=True)

        numeric_count = 0

        for tag in tags:
            print(f"Processing tag: {repository}:{tag.name}")
            if is_numeric(tag.name):
                numeric_count += 1

                if numeric_count > retention_count:
                    if dry_run:
                        print(f"Would delete tag: {repository}:{tag.name}")
                    else:
                        print(f"Deleting tag: {repository}:{tag.name}")
                        registry_client.delete_tag(repository, tag.name)
            else:
                print(f"Keeping non-numeric tag: {repository}:{tag.name}")

# Azure Automation entry point
if __name__ == "__main__":
    # You need to set these variables
    subscription_id = "[guid-of-your-subscription]"
    resource_group_name = "[resource-group-name]"

    # Parse automation variables
    registry_name = "[container-registry-name]"  # or use the paramter 1 > sys.argv[1]
    retention_count = 2  # or use the paramter 2 > int(sys.argv[2]) if len(sys.argv) > 2 else 3
    dry_run = False  # or use the paramter 3 > sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False

    cleanup_acr(registry_name, retention_count, dry_run)
```

The _runbook_ could accept parameters but it seems that you need to provide them manually on each manual run and on a schedule, I didn’t want to spend the time to research how to provide them automatically.

Setting local variables within the script was sufficient.

## Conclusion

I now have a clean and efficient Container Registry with the minimum container images persisted on each repository of images, hence optimizing the costs for my employer.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. You liked it? Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Daniel Tuttle](https://unsplash.com/@danieltuttle?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/a-close-up-of-a-machine-with-a-lot-of-black-dots-on-it-7iFNGzRRukA?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
