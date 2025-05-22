---
title: "7 Steps To Understand OAuth2"
description: "OAuth 2.0 (Open Authorization) is a protocol that allows an application (the client) to access resources on behalf of a user without exposing the user’s credentials to the client."
image: 2025-06-25-a-person-signing-a-document.jpg
imageAlt: A person signing a document.
date: 2025-06-25
categories:
  - Web Development
tags:
  - Security
  - OAuth 2.0
---

It’s widely used to grant third-party applications limited access to user resources without sharing passwords.

## The protagonists

You have the following protagonists involved:

1. **User**: The person who wants to access a resource.
2. **Client**: The application the user wants to use to access the resource.
3. **Authorization Server**: The server that issues the access token after verifying the user’s identity and permissions.
4. **Resource Server**: The server hosting the user’s resources that the client wants to access.

### Key Steps

1. **Authorization Request**: The client requests authorization from the user to access resources.
2. **User Authorization**: The user grants or denies the authorization request.
3. **Authorization Code**: If the user grants access, the authorization server provides an authorization code to the client.
4. **Access Token Request**: The client exchanges the authorization code for an access token by making a request to the authorization server.
5. **Access Token**: The authorization server issues an access token to the client.
6. **Access Resource**: The client uses the access token to request the resource from the resource server.
7. **Resource Delivery**: The resource server validates the token and provides the requested resource to the client.

### Sequence Diagram

Below is a sequence diagram illustrating these steps:

```plaintext
User            Client                Authorization Server         Resource Server
 |                         |                            |                        |
 |-- Access request ------>|--- Authorization Request ->|                        |
 |                         |                            |                        |
 |<-- User Authorization (consent screen)---------------|                        |
 |                         |                            |                        |
 |-- Consent granted ---------------------------------->|                        |
 |                         |                            |                        |
 |                         |<-- Authorization Code -----|                        |
 |                         |                            |                        |
 |                         |-- Access Token Request --->|                        |
 |                         |                            |                        |
 |                         |<----- Access Token --------|                        |
 |                         |                            |                        |
 |                         |--- Access Resource Request ------------------------>|
 |                         |                            |                        |
 |                         |<------ Resource Delivery ---------------------------|
 |                         |                            |                        |

```

### Detailed Steps

1. **Authorization Request**: The client application redirects the user to the authorization server with a request to access resources.
2. **User Authorization**: The user is presented with a consent form where they can approve or deny the client’s request.
3. **Authorization Code**: Upon user approval, the authorization server redirects the user back to the client application with an authorization code.
4. **Access Token Request**: The client application sends the authorization code to the authorization server in exchange for an access token.
5. **Access Token**: The authorization server validates the authorization code and issues an access token to the client.
6. **Access Resource**: The client uses the access token to request resources from the resource server.
7. **Resource Delivery**: The resource server validates the access token and returns the requested resources to the client.

This way, the user’s credentials are never shared with the client application, and the client can only access the resources it has been authorized to use.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/person-signing-in-documentation-paper-48148/).
