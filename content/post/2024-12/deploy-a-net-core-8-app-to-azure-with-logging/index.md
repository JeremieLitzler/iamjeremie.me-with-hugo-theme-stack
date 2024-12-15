---
title: "Deploy a .NET Core 8 application to Azure with Logging"
description: "And how do you setup the logging to make it easy to debug on Azure."
image: 2024-12-16-a-pile-of-logs.jpg
imageAlt: A pile of logs
date: 2024-12-16
categories:
  - Web Development
tags:
  - Microsoft Azure
---

I’ve been working with Microsoft Azure for a little while now, and I have found that setting up the logs wasn’t trivial.

I had an experience with WordPress. In this article, I’ll demonstrate it with a .NET Core 8 web api.

## Prerequisites

You’ll need:

- An account on Microsoft Azure. Personnally, I have only a work account through my current employer at the time of this writing. So I had a few issues to have the resources work together or to gain permissions to perform some actions. I’ll detail them as we go.
- Visual Studio 2022, at least, that’s what I used to make this guide. You’ll need to connect your account so you can deploy through the _Publish_ feature within Visual Studio. This article will not show how to setup a CI pipeline through Azure and deploy a Docker image. Please read my other guide on the topic [where I deployed a Python webapi to Microsoft Azure](../../2024-07/deploy-a-rest-api-python-to-azure/index.md).
- An App Service Plan: if you don’t have any, there isn’t any challenge about this. You’ll create it along with the App Service later in the article.

## Creating the `WebApi`

First, let’s create the application locally.

In Visual Studio, create a new project of type “_APS.NET Core Web Api_” and provide the following details:

- Give it a name
- Select the target framework. Though .NET 9.0 is just out as I write this, I’ll prefer the current LTS version which .NET 8.0.
- Select no authentication type. We’ll deal with this through OpenIddict in a later article. [Subscribe to know more](https://iamjeremie.substack.com/) when I release the article.
- Check the _Configure for HTTPS_ option.
- Uncheck the _Enable container support_ option.
- Decide if you want to use Swagger to document your webapi with the _Enable OpenAPI Support_ option*.* In the article, it is off topic.
- Check _Use controllers_ option.
- Leave the rest as it is.

By default, it will create an application with a _WeatherForecast_ controller.

Check that it works through the _right-click menu_ and _Debug > Start new instance_.

## Create the _App Service_

Before we deploy, we need to create where the application will run.

Go to the Azure portal (`https://portal.azure.com/`) and using main search bar at the top, type “_App Services”_.

On the loaded page, you’ll see all the existing App Services on your subscription or Resource Group.

Select _Create_ and then _Web App_.

Under the _Basics_ tab, you will need to input:

- The resource group.
- The name of the resource.
- The _Publish_ type to _Code_.
- The _Runtime stack_ to _.NET 8 (LTS)_
- The _Operating system_ to _Linux_
- The _Region_ (Note: I selected the same as the other resources, because I had an existing _App Service Plan_ to avoid the creation (and costs) of a new one)
- The _Linux plan_. If you have an existing plan, Azure will list it for you. Otherwise, click _Create new_.

Under the _Deployment_ tab, check the _Basic authentication_ to _Enable_ for _Authentication settings._

Leave the tabs _Database_ and _Networking_ with the defaults. The database is created seperately when we’ll prepare the _OpenIddict_ integration. [Subscribe to know more](https://iamjeremie.substack.com/) when I release the article.

Under the _Application Insights,_ leave it as it is because, even if it can be interesting, it is not how you tell Azure where the application logs will go.

Under the _Tags_ tab, set the tags to organize your resource. You should have a strategy to sort and organize your resources. But that’s a topic for another article.

Finish with _Review + create_ and confirm the resource creation.

## Deploy the Application to Microsoft Azure

Now, let’s deploy the application to the newly created _App Service_.

Right-click on the project and select _Publish._

You’ll need to create a publish profile, so click _Add a publish profile_.

On the modal,

- Select _Azure_ as the _Target._
- Select _Azure App Service (Linux)_ as the _Specific target_
- Select the _App Service_ you just created. You need to be connected in Visual Studio to the same account you used to create the resource in Azure. Otherwise, you won’t see it.
- Select _Publish (generatates pubxml file)_ as the _Deployment type_.

Close the modal and hit _Publish_.

After a couple of minutes, the application should be deployed to Azure. Use the _Overview_ blade of the _App Service_ on Azure to browse the Web API: it should be something like `demowebapinetcore8-fcg3bqdgbme3dchd.westeurope-01.azurewebsites.net`. Add `/weatherforecast` to validate the API is working.

## Enable the Application Logs to the FileSystem

On the Azure portal, browse your _App Service_ resource and search for the _App Service Logs_ blade.

Enable the _Application logging_ to _File System_ and set the _Retention Period_ to _7 days_.

Save the changes.

To check it is working, search for the _Advanced Tools_ blade and click _Go_.

In the new browser tab that opened, select the _Bash_ tab to load a SSH client, also known as the _Kudu_.

Type the following command:

```bash
ls -l LogFiles
```

You should see a file named `yyyy_mm_dd_[some_hash_value]_default_docker.log`. This is where the logs you add in your application will go.

### About the LogStream

You may have come across YouTube video or articles that tells you that you can view the logs live in the _LogStream._ Maybe, it was possible or is still possible in certain conditions. I find that it is not reliable. I’ve tried many things and it often remains stuck with the message “Connected!”…

### Modify `Program.cs` to Add Your First Log

First, before your instanciate the builder, add the following lines:

```csharp
using var loggerFactory = LoggerFactory.Create(loggingBuilder => loggingBuilder
    .SetMinimumLevel(LogLevel.Trace)
    .AddConsole());

ILogger logger = loggerFactory.CreateLogger<Program>();
logger.LogInformation("Program.cs logger ready :)");

logger.LogInformation("Program.cs > init builder...");
var builder = WebApplication.CreateBuilder(args);
```

This way, you can debug errors while your application starts.

Let me tell you how important it is when it will come to debug the _OpenIddict_ integration (well, for you, it might not if you follow exactly the same steps as I describe here).

To test this, hit _Publish_ again and wait that the _App Service_ restarts. In the log file, you should see the two lines of log near the end of the file:

```bash
cat LogFiles/yyy_mm_dd_[some_hash_value]_default_docker.log
# 2024-12-10T10:37:19.5210376Z info: Program[0]
# 2024-12-10T10:37:19.5211218Z       Program.cs logger ready :)
# 2024-12-10T10:37:19.5366643Z info: Program[0]
# 2024-12-10T10:37:19.5366935Z       Program.cs > init builder...
```

### Modify `WeatherForecastController.cs` to Add a Log

In the controller file, use dependency injection to use the logger:

```csharp
        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IEnumerable<WeatherForecast> Get()
        {
            _logger.LogInformation("Getting the forecast...");
            // Business logic...
        }
```

To test this, hit _Publish_ again and wait that the _App Service_ restarts. Request the `/weatherforecast` endpoint and check the logs as described above.

## Conclusion

That’s it. I've longed so much to understand where those log files where. Somehow, the articles and vlogs outthere show outdated information and this article is what you may be looking for.

Again, [subscribe to know more](https://iamjeremie.substack.com/) when I release the article about integrating _OpenIddict_ to the application.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Craig Adderley](https://www.pexels.com/photo/rustic-woodpile-in-a-lush-forest-clearing-29162610/) on Pexels.
