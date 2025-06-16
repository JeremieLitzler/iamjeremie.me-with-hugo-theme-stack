---
title: "Expired Secrets on Azure DevOps Service Connections"
description: "I’ve spent half a day to resolve an expired secret in application registered automatically by Azure DevOps. Here is how and my takeaways."
image: 2025-06-16-expired-secrets-on-azure-devops.jpg
imageAlt: Expired secrets on Azure DevOps
date: 2025-06-16
categories:
  - Software Development
tags:
  - Azure DevOps
  - Microsoft Azure
---

In the article where I describe the deployment of a Python application to Microsoft Azure, I briefly explain how to set up the Docker image push to an azure container registry (ACR in the following paragraphs).

## The Problem

While creating the DevOps pipeline, it creates a service connection automatically. This represents the identity that has permission to push the image to ACR.

Under the hood, Azure DevOps creates an application registration in the Microsoft Entra ID with a secret that expires after 3 months by default.

And you don’t really notice… until it expires.

Suddenly, on day 91, you make a modification to your application, push the code and build the new Docker image.

Then the pipeline terminates with an error:

```bash
 unauthorized: Invalid clientid or client secret
```

First, you don’t understand because three months is a long period. But, more importantly, you don’t know why.

## The fix

The first question that comes to mind is “what is that secret that is invalid and where is it located?”.

You may try to get the ID of the service connection (found under _Project settings > Service Connections_) but you don’t find any reference to that in the Azure resources.

After this, a good place to start is to use the Azure CLI and read the full service connection data.

First, create yourself a PAT token under the menu next your avatar in DevOps and select “_Personal Access Tokens_”.

Select permission to read service connections.

Next, open the Azure portal and open the built-in CLI available to the left of the notifications icon on the top right menu.

Then run the following commands:

```bash
az devops login
# Paste your PAT token when asked

# Available in the DevOps UI on the selected service connection
SERVICE_ENDPOINT_ID="MY_SERVICE_CONNECTION_ID"
ORGA_NAME="MY_ORGA"
PROJECT_NAME="MY_PROJECT"
az devops service-endpoint show --id $SERVICE_ENDPOINT_ID --organization https://dev.azure.com/$ORGA_NAME --project $PROJECT_NAME
```

We get the following.

{{< blockcontainer jli-notice-note "Sensitive values have been replaced with '{}' containing what it represents">}}

{{< /blockcontainer >}}

```json
{
  "administratorsGroup": null,
  "authorization": {
    "parameters": {
      "loginServer": "crmycontainer.azurecr.io",
      "scope": "/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.ContainerRegistry/registries/{repository-name}",
      "servicePrincipalId": "{registered-application-id}",
      "servicePrincipalKey": null,
      "tenantId": "{tenant-id}"
    },
    "scheme": "serviceprincipal"
  },
  "createdBy": {
    "descriptor": "aad.{description-id}",
    "directoryAlias": null,
    "displayName": "John Doe",
    "id": "user-id",
    "imageUrl": "https://dev.azure.com/CBTW-CH/_apis/GraphProfile/MemberAvatars/aad.{description-id}",
    "inactive": null,
    "isAadIdentity": null,
    "isContainer": null,
    "isDeletedInOrigin": null,
    "profileUrl": null,
    "uniqueName": "user@email.com",
    "url": "https://spsprodneu1.vssps.visualstudio.com/{some-id}/_apis/Identities/{id}"
  },
  "creationDate": "2024-07-17T09:22:44.087Z",
  "data": {
    "appObjectId": "{app-object-id}",
    "azureSpnPermissions": "[{\"roleAssignmentId\":\"{role-assignment-id}\",\"resourceProvider\":\"Microsoft.RoleAssignment\",\"provisioned\":true}]",
    "azureSpnRoleAssignmentId": "{azure-spn-role-assignment-id}",
    "registryId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.ContainerRegistry/registries/{repository-name}",
    "registrytype": "ACR",
    "spnObjectId": "{spn-object-id}",
    "subscriptionId": "{subscription-id}",
    "subscriptionName": "My Subscription name"
  },
  "description": "Allows to push the generated Docker image to the ACR.",
  "groupScopeId": null,
  "id": "{service-connection-id}",
  "isOutdated": false,
  "isReady": true,
  "isShared": false,
  "modificationDate": "2024-11-19T09:49:04.997Z",
  "modifiedBy": {
    "displayName": null,
    "id": "00000002-0000-8888-8000-000000000000"
  },
  "name": "{service-connection-name}",
  "operationStatus": {
    "errorCode": null,
    "severity": "",
    "state": "Ready",
    "statusMessage": ""
  },
  "owner": "Library",
  "readersGroup": null,
  "serviceEndpointProjectReferences": [
    {
      "description": "Allows to push the generated Docker image to the ACR.",
      "name": "crtpgoncallprod",
      "projectReference": {
        "id": "{project-id}",
        "name": "My DevOps project"
      }
    }
  ],
  "serviceManagementReference": null,
  "type": "dockerregistry",
  "url": "https://management.azure.com/"
}
```

The most interesting part of it all is the `{registered-application-id}`. From that value, if you possess the `Application Administrator` role in Microsoft Entra ID, you can find the application under the _Application Registrations_ blade.

If you have an expired secret, then you quickly noticed a red toast notification bar at the top of the resource inviting you to “_create a new secret_”.

It isn’t the way to go.

Instead, go to Azure DevOps and load the service connection again and go into edit mode.

By clicking _Save_, DevOps will create a new secret key/value (and override any you may have created manually).

From there, you can resume the CI by triggering a manual build of the pipeline. It’ll build and push the new Docker image to the ACR.

Unfortunately, as of November 2024, I could find no other way. Don’t trust “Click the _Verify_ button” some articles and even the official Microsoft documentation talks about, as it became obsolete at some point. The _Save_ button does it all.

You’ll need to perform this manual action every three months.

Unless Microsoft makes it automatic or **more explicit**?

{{< blockcontainer jli-notice-tip "Follow me">}}

I appreciate you taking the time to read this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
