---
title: "Deploy a REST API Python to Microsoft Azure"
description: "It is good to build an application. It is great to deploy it and witness it running. Let’s see how to do that using Microsoft Azure."
image: images/2024-07-24-logos-ms-azure-and-python.jpeg
imageAlt: "Logos of Microsoft Azure and Python"
date: 2024-07-24
categories:
  - Web Development
tags:
  - Python
---

## Introduction

In the past months, I started my programming journey with Python, building a REST API using Flask and SQLAlchemy.

I had the opportunity at work to build another API and at one point, it was time to deploy the MVP to Microsoft Azure.

Below, you’ll find the detailed steps with no image because Microsoft moves things around often and a screenshot become obsolete quickly…

Naming of blades and tabs could change too, so be patient and look around ;)

For naming resources, you can use the [official guide](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations) on the matter.

## Key vault setup

### Create The _Key Vault_

Via the search on Azure portal, create a _Key Vault_ resource with:

- Basic tab : its name that should be `kv-[project name]-[env]`
- Access config tab : leave as default
- Networking tab: leave as default

### Access control Of The _Key Vault_

Under the _Access Control (IAM)_, you will need to give the following _Role permission_:

- add a role assignment _Key Vault Administrator_ to be able to define the secrets.

{{< blockcontainer jli-notice-tip "Tip: add a member by typing the full email.">}}

{{< /blockcontainer >}}

### Configure The _Key Vault_

Once create, in the _Objects_ blade, create each secret manually.

The key name should be **kebab-case.**

## Container Registry setup

### Create The _Container Registry_

Via the search bar, type “_Container Registry_” and select the resource type.

When setting it up, use _Basic_ plan for lower pricing.

{{< blockcontainer jli-notice-note "Note">}}

The Azure _DevOps_ pipeline will create the repository when the CI is in place.

{{< /blockcontainer >}}

### Configure The _Container Registry_

Under the _Access Control (IAM)_, you will need to give the follow _Role permissions_:

- _ACR Registry Catalog Lister_
- _AcrPull_
- _AcrPush_

These permissions allow:

- you to list the images in the registry when browsing them on the Azure Portal.
- you to configure the Azure pipeline so you can tell the _DevOps_ to push images the Container Registry
- the Container App we’ll create later to pull the images

## Azure Pipeline

### Prerequisites

In Azure, you’ll need to add to your user account the **Application Administrator Role** in Azure AD or Microsoft Entra ID to allow the pipeline creation in _DevOps_.

If you aren’t an administrator, you may need to ask one to grant you this permission. It isn’t something you can do like Role-based permissions.

You’ll also need a _DevOps_ where your project resides. The article doesn’t detail creating the _DevOps_ and it supposes that you have one and that you have created a Git repository to store your application code.

### Configure The Pipeline

Go to the _DevOps_ and the _Pipeline_ blade.

Then:

- on the Connect tab, select _Azure Repositories_.
- on the Select tab, select the target repository.
- on the Configure tab, select registry container created above.

Once you confirmed the pipeline creation, add the tag `latest` in the configuration file generated so that you can select this tag on the _Container App_ later.

Otherwise you’ll need to update the image to deploy to the _Container App_ after each build.

Also, in the generated `azure-pipelines.yml` file, you make a few modifications to prepare the deployment of the Docker image to the _Container App_:

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

- and specifically define the `buildContext` to use `projectPath`:

```yaml
inputs:
  command: buildAndPush
  repository: $(imageRepository)
  dockerfile: $(dockerfilePath)
  buildContext: $(projectPath)
  containerRegistry: $(dockerRegistryServiceConnection)
```

Why? If you have structured your project with a `Dockerfile` in a subfolder `docker`, you must perform the steps above to avoid an error on `docker build` that it can’t find the file `requirements.txt` (list of Python dependencies of your project).

This applies in the following folder structure:

```yaml
project
│   config.py
│   requirements.txt
│   run.py
├── app
│   └── some files ...
└── docker
│   └── Dockerfile
│   └── docker-compose.yml
└──
```

## Storage Account and File Share setup

### Create The Storage Account

Create the storage account in the same zone as all other resources.

There is no specific instructions to create the resource except for the naming that starts with `st` and doesn’t allow hyphens.

Go back to the guide quoted in the introduction.

### Configure The Storage Account

Under _Data Storage > File shares_ blade,

- create a file share. In the app we’re building, we need to store the SQLLite database file. Enable a backup if you need.
- create another file share to store logs. No need for backups.
- create another file share for configuration files and other data files you need to be able to edit without updating the code.

I name my file shares the following way: `fileshare-[designation]- [project]-[env]` where `[designation]` is either `db` for database, `logs` or `json` for files I need to edit on the fly.

You’ll link the _Container app environment_ and _Container App_ to all file shares.

## Container App setup

### Prerequisite

You need:

- A pipeline exists in Azure _DevOps_ with an image ready.
- You need a Contributor role on the Azure Subscription for your user account. Therefore, you might need to provide the create instructions to someone with that permission, if you can’t have them based on your organization policy.

### Create The _Container App_

Via the search bar, type _Container App_ and select the resource type.

On the Basics tab,

- configure the Resource group, the name and the region
- customize the _Container Apps Environment_ (it’s what holds many _Container App_) by creating a new one.
  - click _New_
  - then, on the _Basics_ tab, give a name, the convention in the introduction and leave the rest of the options as it is.
  - next, on the _Monitoring_ tab, disable the logs. The Container App provides a console log stream that can help and your application should store file logs in the dedicated file share.
  - leave the _Workload profiles_ and _Networking_ tabs as they are.

On the Container tab,

- select the image source to be Azure Container Registry (ACR).
- select the ACR you created previously.
- select the image.
- select the image tag to `latest`.
- adjust the CPU and Memory to your needs.
- you could set up the environment variables now, but we’ll look at that in the Configure step. In fact, you may need to adjust then in the lifetime of your application.

On the Bindings tab, leave it blank.

On the Ingress tab, you will need to configure the TCP part so the REST API is accessible over HTTP:

- check the _Ingress_ checkbox
- select _Ingress Traffic_ to be _Accepting traffic from anywhere_
- select HTTP for the _Ingress type_
- leave the Client certificate mode as default (no option selected)
- set the _Target port_ to 5000, the default port of the Flask app we’re deploying.
- confirm the creation on the _Review + create_ tab.

Note: if the review fails with the following error, it probably means you don’t have the permission to create the resource:

> The client ’youraccount@example.com” with object id “xxx” doesn’t have authorization to perform action “**Microsoft.App/register/action**” over scope “/subscriptions/yyy” or the scope is invalid. If access was recently granted, please refresh your credentials. (Code: AuthorizationFailed) (Code: AuthorizationFailed)

### Configure the Container Apps Environment

Once Azure has created the _Container App_, go straight to the _Container Apps Environment_ to link the file shares to it.

To do so, retrieve the name and access key under the _Storage Account:_

- go to _Security + networking_ and select the _Access keys_ blade.
- copy
  - one of the keys.
  - the Storage account name.
  - the file share names created earlier (found under the _File shares_ blade).

Back on the Container Apps Environment:

- go to _Settings_ and the _Azure Files_ blade.
- decide of the name using this naming: `azure-files-[designation]` (`designation` would be `db`, `logs`, etc.)
- add a new one and fill the field by pasting the values copied previously.
- set the _Access mode_ to _Read/Write_ or _Read only_ (I do that for the files I need the application not to write).
- repeat for all the file shares you need the _Container App_ to use.

What will we use that for? In the REST API, you may use a SQLLite database where the database is a file and you need to persist it.

The same goes for file logging.

You could write the files in the container image. But, as it restarts on a new deploy, you’ll lose the data…

### Configure the _Container App_ Deploy Settings

Next, to go the _Container App_ to configure the deploy settings.

To do so, go to the _Revisions and replicas_ blade under _Application_ and click _Creation new revision_.

We’ll set up the _Container_ tab last. You’ll understand why soon.

Go to the _Scale_ tab and adjust the _Min replicas_ and _Max replicas_ to use based on a scale rule you define. I’ve not used any rule in my scenario so I’ll skip that. I simply set the min. and max. values to 1.

On the _Volumes_ tab,

- select _Azure file volume_ as _Volume type_.
- give the volume a name. For example, I’d name the databases volume `databases`. You’ll need one volume for each file share you created.

**Important note: the volume name** must match the name of the volume you need to create in the Dockerfile. The volume name corresponds to what follows the `WORKDIR` value under the `VOLUME` commands below:

```yaml
# Set work directory of the docker image
WORKDIR /project-container

# Create mount points with absolute paths
VOLUME /project-container/databases
VOLUME /project-container/logs
```

- select the target file share (which is really the Azure file value you created under the _Container App Environment_).
- set the mount options to `nobrl` if the volume contains a SQLLite database file. Why? The problem is that Docker mounts the volume as CIFS file system which can’t deal with SQLite3 lock. See [this answer](https://stackoverflow.com/a/54051016) and [that answer](https://stackoverflow.com/a/61077705) in Stackoverflow. The [Microsoft documentation](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/storage/mountoptions-settings-azure-files#other-useful-settings) also confirm this.
- make sure to click the _add_ button before continuing.

Go back to the _Container_ tab to add the volumes based on the File shares you create. On our example so far, we need:

- leave the _Revision details_ section as it is.
- Under the _Container image_ section, click of the existing image.

It’ll open a right pane:

- under the _Basics_ tab, you find the details you specified at the creation of the _Container App_ resource. This is where you can add your environment variables (scroll to the very bottom). We’ll come back to it when we will link the _Key Vault_ to pull the secret values from it.
- under the _Health probes_, leave as it is.
- under the _Volumes mounts_ tab, add all the volume mounts you need:
  - the Volume name will equal to the name you defined above.
  - the Mount path should be the same value as you defined in the _Dockerfile_ as explained above.
  - leave the _Sub path_ empty.
- click _Save_
- make sure to click _Create_

Under the _Revisions and replicas_ blade, you should see within a couple of minutes if the deploy was successful when it displays the _Running status_ as _Running_ and a green check mark.

If not, click the revision link on the first column and click _Console log stream_. Somehow, the logs may not always appear so try a few times… Consistency in what the console log stream displays is random... On that end, I saw logs, and sometimes, I didn’t.

### Linking the Key Vault and the Container App

This is a prerequisite to configuring the environment variables.

First, under the _Identity_ blade in the _Container App_ resource, enable the System assigned identity by toggling the status to _On_.

You need this so you can provide the identify of the _Container App_ a role-based permission in the _Key Vault_ IAM.

Then, go to _Key Vault_ resource and browse to the _Access control (IAM)_ blade.

Click _Add_ and then _Add role assignment_.

- under the _Role_ tab, search for _Key Vault Secrets User_ and select it.
- under the _Members_ tab,
  - select _Managed identity_.
  - click _Select members_.
  - on the right pane that opens,
    - select your subscription,
    - select the _Managed identity_: you should have a value called _Container App (1)_ (`1` is the number of _Container App_ you have configured with a system identity).
    - select the target member list under _Select_. It should display a member with the name of your _Container App_.
    - make sure to click _Select_.
    - finish with _Review + assign_.

### Configure the _Container App_ Secrets Environment Variables

To start this section, you’ll need to copy the _Vault URI_ found under the _Overview_ blade of the _Key Vault_ resource.

Also make note of the secret names you created.

Prepare a URL for each with the following format: `{vault_uri}/secrets/{secret_name}`

Back to the _Container App_, browse to the _Settings_ and _Secrets_ blade.

From there, add your secret from the _Key Vault_ by clicking _Add_ button. Then:

- set the _Key_ value to the secret name you’re adding with a prefix `kv_`.
- set the _Type_ to _Key Vault reference_.
- set the _Value_ to the corresponding URL you prepared.
- click _Add_ and wait that the secret does appear.

{{< blockcontainer jli-notice-warning "Attention">}}

If the secret doesn’t appear, even if the Azure Portal gives a positive feedback in the notifications, the problem is that you didn’t complete properly “_Linking the Key Vault and the Container App_” step properly.

{{< /blockcontainer >}}

### Configure the Environment Variables

Once you’re done, create a new revision from the _Applications > Revisions and replicas_ blade.

Select your container image and scroll down to the _Environment Variables_ section and:

- first, add the variables that aren’t a secret using the _Source_ as _Manual entry_.
- second, add the variable whose values come from the Key vault using the _Source_ as _Reference a secret_. Then select as the _Value_ the corresponding secret reference.

Make sure to click _Save_ and create the revision.

You’re done configuring! 🏆

## Testing the API

Using Visual Studio Code and the REST Client extension, you can create a little file to test your endpoints:

```rest
### Create an event
POST https://capp-myproject-prod.cravesea-7fd7d8d0b6.myregion.azurecontainerapps.io/event
Content-Type: application/json

{
  "id": 1234
}

### GET all events
GET https://capp-myproject-prod.cravesea-7fd7d8d0b6.myregion.azurecontainerapps.io/event/all
Content-Type: application/json
```

## Troubleshooting

### Can’t Call The REST API App Even If Deploy Is Successful

If you get the following message when calling your app while the deploy is successful and Azure tells you it’s running:

```logs
azure upstream connect error or disconnect/reset before headers. retried and the latest reset reason: remote connection failure, transport failure reason: delayed connect error: 111
```

Make sure you use a production-grade server, not the default Flask server.

To fix that, you need to:

- install `gunicorn` package: it’s a production-grade webserver.
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

## Conclusion

If you read thus far, well done and thank you!

I’ll continue sharing more about Python and Azure as I work with it.

Save my website in your bookmarks!

Credit: Logos of the header images are from WorldVectorLogo and SVGRepo. You can find the original images [here](https://worldvectorlogo.com/logo/azure-2) and [there](https://worldvectorlogo.com/logo/python-4): I built the image with [Sketchpad](https://sketch.io/sketchpad/) of Sketch.io.
