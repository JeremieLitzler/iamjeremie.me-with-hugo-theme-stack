---
title: "How to migrate a WordPress site to Microsoft Azure"
description: "I did a migration from InMotion shared hosting to Microsoft Azure in 2023 for a non profit organization in the US. I learned a lot as a first experience with Azure. Here is how it went."
image: /images/-.jpg
imageAlt:
date: 2024-02-13
categories:
  - Tutorials
tags:
  - Microsoft Azure
  - WordPress
draft: true
---

## Prerequisites

You need to:

- have an account on Microsoft Azure.
- be able to access to the source hosting you want to migrate to.
- be able to add the plugin `` to migrate the website content.

## Create an app service plan

The architecture of the WordPress App Service on Microsoft Azure is the following:

![Digram from Microsoft Learn](images/wordpress-app-service-diagram.png)

Credit: image from [this article](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/infrastructure/wordpress-app-service) on Microsoft Learn

## Clean up the app service

## Configure the app service with HTTP2

## Migrate from a host to Azure

## Cost: for non-profits, take advantage of Microsoft's offering

See more details at [https://www.microsoft.com/en-us/nonprofits/azure](https://www.microsoft.com/en-us/nonprofits/azure).

## Maintenance and updates with deployment slots

### Why deployment slots

Once you are done migrating the website, it is time to think about how to perform the maintenance. That includes updating the core of WordPress, the theme and the plugins.

While you could use a plugin, such as UpdrafPlus or something else, I recommend to use the deployment slots native of Azure.

I agree with you that it is more technical, but it is all included in the App Service Plan available to you. Plus, I personnaly tried UpdrafPlus on Azure and it didn't go as well as I'd have hoped.

### About backups in Microsoft Azure

So, by default, your database instance and App Service are backup automatically.

The database is backep up once a day, around the hour it was created.
You can take manual backup at any time, within the limit of 50 per instance.

The App Service is backed up every hour. You could setup manual backups but I don't see a use for it.

The time of backup may not be in synchronization between the database and the App Service.

To avoid loss of data or issue, I recommend to take a manual backup of the database right after an automatic backup of the App Service.

Also refrain from making modifications before you are done with the maintenance tasks.

### About the deployment slots

When you have an App Service running, ...
