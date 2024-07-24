---
title: "Deploy a REST API Python to Microsoft Azure"
description: "It is good to build an application. It is great to deploy it and witness it running. Let's see how to do that using Microsoft Azure."
image: images/2024-07-24-logos-ms-azure-and-python.jpg
imageAlt: "Logos of Microsoft Azure and Python"
date: 2024-07-24
categories:
  - Web Development
tags:
  - Python
draft: true
---

## Introduction

In the past months, I started my programming journey with Python, building a REST API uisng Flask and SQLAlchemy.

I had the opportunity at work to build another API and at one point, it was time to deploy the MVP to Microsoft Azure.

Below, you'll find the detailed steps with no image because Microsoft moves things around often and a screenshot become obsolete quickly...

Naming of blades and tabs could change too, so be patient and look around ;)

For naming resources, you can use the [official guide](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations) on the matter.

## Key vault setup

### Create

Via the search on Azure portal, create a Key Vault resource with:

- Basic tab : its name that should be `kv-[]`
- Access config tab : leave as default
- Networking tab: leave as default

### Access control

You’ll need to:

- add a role assignment "Key Vault Administrator" to be able to define the secrets.

Tip: add a member by typing the full email.

### Configure

Once create, in the Objects blade, create each secret manually. The key name should be **kebab-case.**

Under the _Access Control (IAM)_, you will need to give the follow _Role permissions_:

- _Key Vault Administrator_ so that you can view, add adn edit secrets

## Container registry setup

### Create

Via the search bar, type "Container Registry" and select the resource type.

When setting it up, use "Basic" plan for lower pricing.

Note: the Azure DevOps pipeline will create the repository when the CI is in place.

### **Configure**

Under the _Access Control (IAM)_, you will need to give the follow _Role permissions_:

- _ACR Registry Catalog Lister_
- _AcrPull_
- _AcrPush_

They are used to allow:

- you to list the images in the registry when browsing them on the Azure Portal.
- you to configre the Azure pipeline so you can tell the DevOps to push images the Container Registry
- the Container App we’ll create later to pull the images

## Azure Pipeline

### Prerequisite

In Azure, you’ll need to add to your user account the **Application Administrator Role** in Azure AD or Microsoft Entra ID to allow the pipeline creation in DevOps.

### Configure

Go to the DevOps and the Pipeline blade.

Then:

- on the Connect tab, select _Azure Repositories_
- on the Select tab, select the target repository
- on the Configure tab, select registry container

Once you confirmed the pipeline creation, add the tag “latest” in config file generated so that you can configure the _Container App_ later on with that tag. Otherwise you’ll need to update the image deploy to the _Container App_ after each build

Also, in the generated `azure-pipelines.yml` file, you need to:

- add a variable `projectPath` to define the project path:

```yaml
variables:
  # Container registry service connection established during pipeline creation
  dockerRegistryServiceConnection: "e5979aa7-383a-4ddb-9aff-6e531f3d023a"
  imageRepository: "my-app"
  containerRegistry: "mycontainerregistry.azurecr.io"
  dockerfilePath: "$(Build.SourcesDirectory)/docker/Dockerfile"
  projectPath: "$(Build.SourcesDirectory)"
  tag: "$(Build.BuildId)"
```

- and specifically define the `buildContext` :

```yaml
inputs:
  command: buildAndPush
  repository: $(imageRepository)
  dockerfile: $(dockerfilePath)
  buildContext: $(projectPath)
  containerRegistry: $(dockerRegistryServiceConnection)
```

Why? If you have structured your project with a `Dockerfile` in a subfolder `docker`, not doing the above two steps willl throw an error on `docker build` that the `requirements.txt` is not found.

This applies in the following folder structure:

```yaml
project
│   config.py
│   requirements.txt
│   run.py
├── app
│   └── some files ...
└── docker
├── Dockerfile
└── docker-compose.yml
```

## Storage Account and File share setup

### Prerequisite

None.

### Create

Create the storage account in the same zone as all other resources.

### Configure

Under _Data storage > File shares_ blade,

- create a file share. In the app we are building, we need to store the SQLLite dabtase file. Enable a backup, if you need.
- create another file share to store logs. No need for backups.

You’ll link the _Container app environment_ to that file share in the _Contain App_ setup.

## Container App setup

### Prerequisite

You need:

- A pipeline is existing in Azure DevOps with an image ready.
- You need a Contributor role on the subscription for your user acount. Therefore, you might need to provide the create instructions to someone with those permissions, if you can’t have them per your organization policy.

### Create

Via the search bar, type "Container App" and the resource type.

On the Basics tab,

- configure the Resource group, the name and the region
- customize the _Container Apps Environment_ (it is what holds many _Container App_) by creating a new one.
  - click _New_
  - on the _Basics_ tab, give a name and leave the rest of the options as it is
  - on the _Monitoring_ tab, disable the logs. The Container App provide a console log stream that cna help. Plus, in the Flask app, we have a file log system configured.
  - leave the _Workload profiles_ and _Networking_ tabs as they are.

On the Container tab,

- select the image source to be Azure Container Registry (ACR)
- select the ACR you created previously
- select the image
- select the image tag
- adjust the CPU and Memory to your needs
- you could setup the environment variables now, but we’ll look at that in the Configure step.

On the Bindings tab, leave it blank.

On the Ingress tab, you will need to configure the TCP part so the REST API is accessible over HTTP:

- check the _Ingress_ checkbox
- select _Ingress Traffic_ to be _Accepting traffic from anywhere_
- select HTTP for the _Ingress type_
- leave the Client certificate mode as default (no option selected)
- set the _Target port_ to 5000, the default port of the Flask app we’re deploying.
- confirm the creation on the _Review + create_ tab.

Note: if the review fails with the following error, it probably means you don’t have the permissions to create the resource:

> The client 'youraccount@example.tech' with object id 'xxx' does not have authorization to perform action 'Microsoft.App/register/action' over scope '/subscriptions/yyy' or the scope is invalid. If access was recently granted, please refresh your credentials. (Code: AuthorizationFailed) (Code: AuthorizationFailed)

### Configure the Container Apps Environment

Once the _Container App_ is created, go straight to the _Container Apps Environment_ to link the File share to it.

To do so, retrieve the Access key under the _Storage Account:_

- go to _Security + networking_ and select the _Access keys_ blade.
- copy
  - one of the keys.
  - the Storage account name.
  - the File share name created earlier (found under the _File shares_ balde).

Back on the Container Apps Environment:

- go to _Settings_ and the _Azure Files_ blade.
- add a new one with pasting the values copied previously.
- set the _Access mode_ to _Read/Write._
- repeat for all the file shares you need the _Container App_ to use.

What will we use that for? In the REST API, you might use a SQLLite database where the database is a file and you need to persist it.

If you leave it on the _Container App_, as it restarts on a new deploy, you’ll loose the data…

### Configure the Container App Deploy settings

Next, to go the _Container App_ to configure the deploy settings.

To do so, go to the _Revisions and replicas_ blade under _Application_ and click _Creation new revision._

We’ll setup the _Container_ tab last. You’ll see why soon.

Go to the _Scale_ tab and adjust the _Min replicas_ and _Max replicas_ to use based on scale rule you define. I’ve not used them so I won’t dive into that.

On the _Volumes_ tab,

- select _Azure file volume_ as _Volume type_.
- give the volume a name.

**Important note: the volume name** must match the name of the volume you need to create in the Dockerfile. The volume name correspond to what follows the `WORKDIR` value under the `VOLUME` commands below:

```yaml
# Set work directory of the docker image
WORKDIR /project-container

# Create mount points with absolute paths
VOLUME /project-container/databases
VOLUME /project-container/logs
```

- select the target file share
- set the mount options to `nobrl` if the volume contains a SQLLite databases file. Why? The problem is that the volume is mounted as CIFS filesystem which can not deal with SQLite3 lock. See [this answer](https://stackoverflow.com/a/54051016) and [that answer](https://stackoverflow.com/a/61077705) in Stackoverflow and that [Microsoft documentation](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/storage/mountoptions-settings-azure-files#other-useful-settings).
- make sure to click the _add_ button before continuing.

On the _Container_ tab, add the volumes based on the File shares you create. On our example so far, we need:

- leave the _Revision details_ section as it is.
- Under the _Container image_ section, click of the existing image. I’ll open a pane of the right:
  - under the _Basics_ tab, you find the details you specified at the creation of the _Container App_ resource*.* This is where you can add your environment variables (scroll to the very bottom). We’ll come back to it when we will link the Key Vault to pull the secret values.
  - under the _Health probes_, leave as it is.
  - under the _Volumes mounts_ tab, add all the volume mounts you need:
    - the Volume name will equal to the name you defined above.
    - the Mount path should be the same value as you defined in the _Dockerfile_ as explained above.
    - leave the _Sub path_ empty.
  - click _Save_
- click _Create_

Under the _Revisions and replicas_ blade, you should see within a couple of minutes if the deploy was successful is the _Running status_ is _Running_ and displays a green check mark.

### Linking the Key Vault and the Container App

This is a prerequisite to configuring the environment variables.

First, under the _Identity_ blade in the _Container App_ resource, enable the System assigned identity by toogling the status to _On_.

Then, go to _Key Vault_ resource and browse to the _Access control (IAM)_ blade.

Click _Add_ and then _Add role assigment_.

- under the _Role_ tab, search for _Key Vault Secrets User_ and select it
- under the _Members_ tab,
  - select _Managed identity_
  - click _Select members_
  - on the right pane that opened,
    - select your subscription,
    - select the _Managed identity_: you should have a value called _Container App_
    - select the members list under _Select_. It should display a member with the name of your _Container App_
    - make sure to click _Select_
    - finish with _Review + assign_

### Configure the Environment Variables

To start this section, you’ll need to copy the _Vault URI_ found under the _Overview_ blade of the _Key Vault_ resource.

Also make note of the secret names you create.

Prepare a URL for each with the following format: `{vault_uri}/secrets/{secret_name}`

Back to the _Container App_, browse to the _Settings_ and _Secrets_ blade.

From there, add your secret from the _Key Vault_ by cliking _Add_ button. Then:

- set the _Key_ value to the secret name you’re adding
- set the _Type_ to _Key Vault reference_
- set the _Value_ to the corresponding URL you prepared.
- click _Add_ and wait that the secret does appear.

Note: if the secret doesn’t appear, even Azure Portal gives a positive feedback in the notifications, the problem is that you didn’t complete properly “Linking the Key Vault and the Container App” part.

Once you’re done, create a new revision from the _Applications > Revisions and replicas_ blade.

Select your container image and scroll down to the _Environment Variables_ section and:

- first, add the variables that aren’t a secret using the _Source_ as _Manual entry_.
- second, add the variable whose values come from the Key vault using the _Source_ as _Reference a secret_. Then select as the _Value_ the proper secret reference.

Make sure to save and create the revision.

You’re done configuring! 🏆

## Testing the API

…

## Troubleshooting

### Cannot Call The REST API App Even If Deploy Is Successful

If you get the following message when calling your app while the deploy is successful and Azure tells you it is running:

```
azure upstream connect error or disconnect/reset before headers. retried and the latest reset reason: remote connection failure, transport failure reason: delayed connect error: 111
```

Make sure you use a production-grade server, not the default Flask server.

To fix that, you need to:

- install `gunicorn` package: it is a production-grade webserver.
- configure the `Dockerfile` with the following command
  ```docker
  # Runtime commmand to start server
  CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
  ```

To run the above command, you need a `run.py` file at the root that contains something like this:

```python
import os

from app import MyApp

config_name = os.getenv("FLASK_CONFIG") or "default"
app = MyApp.create_app(config_name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

```

Credit: Logos of the header images are from WorldVectorLogo and SVGRepo. You can find the original images [here](https://worldvectorlogo.com/logo/azure-2) and [there](https://worldvectorlogo.com/logo/python-4): I built the image with [Sketchpad](https://sketch.io/sketchpad/) of Sketch.io.
