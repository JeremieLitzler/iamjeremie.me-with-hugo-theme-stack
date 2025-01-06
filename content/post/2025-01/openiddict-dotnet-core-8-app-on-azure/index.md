---
title: "Integrate OpenIddict  to a .NET Core 8 application on Azure"
description: "OpenIddict aims at providing a versatile solution to implement OpenID Connect client, server and token validation support in any .NET application. I’ll describe in this article the steps to achieve a simple use case."
image: 2025-01-06-openiddict-homepage-doc-webiste-screenshot.jpg
imageAlt: Screenshot of Openiddict homepage
date: 2025-01-06
categories:
  - Web Development
tags:
  - Authentication
  - Microsoft Azure
  - Dot Net Core
---

I needed to create a simple RESTFul application that would allow me to mock a webservice provided by a client but inaccessible from my environment.

Also, some endpoints would be queried through Basic Authentication and others through the OpenID OAuth2 standard.

It wasn’t easy because at the same time, I was struggling with:

- Finding the application logs in my _App Service_ to debug the deployment to Azure.
- Adding the right links between resources with very limited permission in my organization.

Let’s dive in!

## Prerequisites

You’ll need:

- To complete [the following guide](../../2024-12/deploy-a-net-core-8-app-to-azure-with-logging/index.md) to kickstart the project.
- An SQL Server Instance to create a new database, but I suppose you could use a MySQL or any other driver. You need it for the _OpenIddict_ database where you store the application registrations and tokens. Alternatively, you can use an SQLite database, but I couldn’t create a storage account to store the file in my case and I already had an SQL Server provisioned.

## Create the `openiddict` Database

I’ll use an SQL Server to host the data for _OpenIddict._ As stated above, you can choose another driver.

You’ll need to provision it before you continue.

Here are the steps:

- Go to the Azure Portal.
- Browse to _SQL Databases_
- Click _Create_

Note: in case you don’t have an SQL Instance yet, the Azure Portal will request you to create it. Use the _SQL authentication_ to create the credentials to connect the instance in SQL Server Management Studio (in short _SSMS_) and through the application.

### Under _Basics_ tab

- Make sure to select the _Subscription_ and _Ressource Group_:
  - Your target _Subscription_.
  - Your target _Ressource Group_.
- Set the database name to `openiddict`.
- Set the server instance (or create one).
- Leave _Want to use SQL elastic pool_ to _No_.
- Leave the Workload environment to Development.
- Configure the _Compute + storage_ to the _Basic tier_ with 500 MB Storage.
- Choose _Locally-redundant backup storage_.

### Under _Networking_ tab

Leave the defaults as they are.

### Under _Security_ tab

Leave the defaults as they are.

### Under _Additional settings_ tab

- Set the _Collation_ to `French_CI_AS` or any value you prefer.
- Leave the rest with the defaults.

### Under _Tags_ tab

Add the necessary tags.

### Review + create

Check the summary and click _Create_.

## Modify the `Program.cs` to Use SQL Server

First, add the packages below:

```powershell
dotnet add package Microsoft.EntityFrameworkCore --version 8.0.11
dotnet add package Microsoft.EntityFrameworkCore.SqlServer --version 8.0.11
dotnet add package OpenIddict.AspNetCore --version 5.8.0
dotnet add package OpenIddict.EntityFrameworkCore --version 5.8.0
```

Then, you need to create the `ApplicationDbContext` class in a folder `Models`:

```csharp
using Microsoft.EntityFrameworkCore;

namespace DemoWebApiWithOpenIddict.Models;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions options)
        : base(options) { }

    protected override void OnModelCreating(ModelBuilder builder) { }
}

```

Then, declare it right after the registration of the controllers in the `Program.cs`:

```csharp
using DemoWebApiWithOpenIddict.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Protocols.Configuration;

using var loggerFactory = LoggerFactory.Create(loggingBuilder => loggingBuilder
    .SetMinimumLevel(LogLevel.Trace)
    .AddConsole());

ILogger logger = loggerFactory.CreateLogger<Program>();
logger.LogInformation("Program.cs logger ready :)");

logger.LogInformation("Program.cs > init builder...");

builder.Services.AddControllers();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    // Configure the context to use sql server.
    var dbServer = RetrieveValueFromConfig(builder, "DbServer", logger);
    var dbUser = RetrieveValueFromConfig(builder, "DbUser", logger);
    var dbPassword = RetrieveValueFromConfig(builder, "DbPassword", logger);
    var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")!;
    options.UseSqlServer(string.Format(connectionString, dbServer, dbUser, dbPassword));

    // Register the entity sets needed by OpenIddict.
    // Note: use the generic overload if you need
    // to replace the default OpenIddict entities.
    options.UseOpenIddict();
});

static string RetrieveValueFromConfig(WebApplicationBuilder builder, string key, ILogger logger)
{
    var keyValue = builder.Configuration[key];
    return keyValue ?? throw new ConfigurationErrorsException($"Missing <{key}> environment value in App Service");
}

```

You need to declare the `ConnectionString` in your `appsettings.json`.

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server={0};Initial Catalog=openiddict;Persist Security Info=False;User ID={1};Password={2};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  }
}
```

Locally, we’ll define the placeholders found in the connection string in the `appsettings.Development.json`:

```json
{
  "DbServer": "tcp:your-db-server.database.windows.net,1433",
  "DbUser": "your_user",
  "DbPassword": "Y0urPa55w0rd!"
}
```

On the _App Service_, we need to add the 3 variables above under the _Environment variables_ blade of the _App Service_.

Click “+ _Add”_ for each variable and provide its name and value as defined in the JSON file. By default, I check the “_Deployment slot setting_” to make sure Microsoft Azure uses the setting when creating a slot (another topic on its own…).

To test, we’ll need to complete a few more steps.

Note: you could store the `ConnectionString` in a KeyVault. I chose the environment variables to store the server, the user and the password for simplicity.

## The Key Vault

### Why a Key Vault

To protect the tokens generated, the OpenIddict client and server stacks use 2 types of credentials:

- **Signing credentials are used to protect against tampering**. They can be either asymmetric (e.g., a RSA or ECDSA key) or symmetric.
- **Encryption credentials are used to ensure the content of tokens can’t be read by malicious parties**. They can be either asymmetric (e.g., a RSA key) or symmetric.

Source: [https://documentation.openiddict.com/configuration/encryption-and-signing-credentials](https://documentation.openiddict.com/configuration/encryption-and-signing-credentials)

And you need to store those certificates in a safe place: a Key Vault.

The Key Vault creation is simple. I won’t dive into the details now because I’ve detailed it in my guide untitled, “[**Deploy a REST API Python to Microsoft Azure**](../../2024-07/deploy-a-rest-api-python-to-azure/index.md)”.

### Configure the Key Vault

You need to:

- To generate the certificates.
- To read the certificates from the application in Azure.

To generate the certificates, you need an access policy and depending on your seniority in your organization, you may not have the permission to list the users or applications to whom you need to assign the policy.

So first, under the newly created _Key Vault_, go to the _Access Policies_ blade and click “_+ Create_”.

We’ll add the policy to the certificate creator (you), so if you end up not being able to validate the creation, ask your manager.

In the form,

- Select _Select all_ as _Permissions._
- Then, select the _Principal_ or the user using your full email address.
- Leave the _Application_ blank.
- Finish by clicking _Create._

Next, add another policy to the _App Service_ resource.

Before that, make sure to enable the _System assigned_ identity under the _App Service_ and the blade _Identity_. It’ll generate a _Principal (Object) ID_ you’ll use to search the _Principal_ to assign the policy to.

For this policy, assign the permissions “_Get_” and “_List_”.

### Just in Case…

While I was doing this myself for the first time, I thought I need to add role-based permissions for myself and the _App Service._ I added:

- “_Key Vault Administrator_” to myself.
- _“Key Vault Cerfitificates User”_ and “_Key Vault Cerfitificates Officer“_ to the App Service.

I don’t think you need. But just in case…

### Generate the Certificates

Now navigate to the _Certificates_ blade in your Key Vault and:

- Click “+ Generate/Import”.
- Leave the method to _Generate._
- Provide a name like “_certificate-openiddict-encryption_”.
- Leave the type of certificate to _Self-signed certificate_ unless you can provide an authority.
- Set the _Subject_ to your App Service full domain name. So you could have for example `CN=your-appservice[-fcg3bqdgbme3dchd.westeurope-01.azurewebsites.net](http://demowebapinetcore8-fcg3bqdgbme3dchd.westeurope-01.azurewebsites.net/)`. Please adjust the URI to your App Service URI.
- Choose the _Validity Period_.
- Leave the _Lifetime Action Type_ as it is, e.g., _Automatically renew at a given percentage lifetime_.
- Confirm with a click on _Create_.

Repeat the steps but name the second certificate “_certificate-openiddict-signing_”.

## Integrate the _OpenIddict_ Solution to Enable OpenID on the Project

Back to the `Program.cs`, we first add the required packages:

```csharp
dotnet add package Azure.Identity --version 1.13.1
dotnet add package Azure.Security.KeyVault.Certificates --version 4.7.0
dotnet add package System.Security.Cryptography.X509Certificates --version 4.3.2
```

Next, we’ll encapsulate the configuration of _OpenIddict_ into a method `SetupOpenIddict`:

```csharp
logger.LogInformation("Program.cs > Register the OpenIddict core components.");
SetupOpenIddict(builder, logger);
```

Within the method, we’ll have the following. I have used comments to explain the logic. Please read them.

```csharp
using System.Security.Cryptography.X509Certificates;

static void SetupOpenIddict(WebApplicationBuilder builder, ILogger logger)
{
    builder.Services.AddOpenIddict()
        .AddCore(options =>
        {
            // Configure OpenIddict to use the Entity Framework Core stores and models.
            // Note: call ReplaceDefaultEntities() to replace the default OpenIddict entities.
            options.UseEntityFrameworkCore()
                   .UseDbContext<ApplicationDbContext>();
        })
        // Register the OpenIddict server components.
        .AddServer(options =>
        {
            // And enable the token endpoint.
            options.SetTokenEndpointUris("connect/token");

            // Then, enable the client credentials flow.
            options.AllowClientCredentialsFlow();

            // Then, register the signing and encryption credentials.
            if (builder.Environment.IsDevelopment())
            {
                // Locally, use the certificates provided through OpenIddict.
                // They won't work in Production.
                options.AddDevelopmentEncryptionCertificate()
                       .AddDevelopmentSigningCertificate();
            }
            else
            {
		        // In Production, use the certificates read from the Key Vault.
                logger.LogInformation("SetupOpenIddict > AddServer > Not Development...");
                string? keyVaultUri = RetrieveValueFromConfig(
                    builder,
                    "OpenIddict:KeyVaultUri",
                    logger);
                logger.LogInformation($"SetupOpenIddict > AddServer > OpenIddict:KeyVaultUri is <{keyVaultUri}>");
                // Initialize the Certificate Client to query the Key Vault
                var certClient = new CertificateClient(
                    new Uri(keyVaultUri),
                    new DefaultAzureCredential());
                logger.LogInformation("SetupOpenIddict > AddServer > KeyValult client to read certificates = OK!");

                // Load encryption certificate
                var openIddict_EncryptionCertificateName = RetrieveValueFromConfig(
                    builder,
                    "OpenIddict:EncryptionCertificateName",
                    logger);
                logger.LogInformation($"SetupOpenIddict > AddServer > OpenIddict:EncryptionCertificateName is <{openIddict_EncryptionCertificateName}>");
                try
                {
                    // Download the full certificate that includes the private key,
                    // required for OpenIddict. GetCertificate isn't enough and doesn't
                    // contain the private key.
                    var encryptionCert = certClient.DownloadCertificate(openIddict_EncryptionCertificateName).Value;
                    logger.LogInformation($"SetupOpenIddict > AddServer > read encryption cert: <{encryptionCert}>");
                    options.AddEncryptionCertificate(new X509Certificate2(encryptionCert));
                    logger.LogInformation("SetupOpenIddict > AddServer > AddEncryptionCertificate = OK!");
                }
                catch (Exception ex)
                {
                    logger.LogError(ex.Message, ex.StackTrace);
                    throw;
                }

                // Load signing certificate
                var openIddict_SigningCertificateName = RetrieveValueFromConfig(builder, "OpenIddict:SigningCertificateName", logger);
                logger.LogInformation($"SetupOpenIddict > AddServer > OpenIddict:SigningCertificateName is <{openIddict_SigningCertificateName}>");
                try
                {
                    var signingCert = certClient.DownloadCertificate(openIddict_SigningCertificateName).Value;
                    logger.LogInformation($"SetupOpenIddict > AddServer > read encryption cert: <{signingCert}>");
                    options.AddSigningCertificate(
                        new X509Certificate2(signingCert));
                    logger.LogInformation("SetupOpenIddict > AddServer > AddSigningCertificate = OK!");

                }
                catch (Exception)
                {
                    throw;
                }
            }
            // Register the ASP.NET Core host and
            // configure the ASP.NET Core-specific options.
            options.UseAspNetCore()
                   .EnableTokenEndpointPassthrough();
        })

        // Register the OpenIddict validation components.
        .AddValidation(options =>
        {
            // Import the configuration from the local OpenIddict
            // server instance.
            // Basically, the IIS Express or the App Service is the
            // OpenID server in parallel to your Web API.
            options.UseLocalServer();

            // Register the ASP.NET Core host.
            options.UseAspNetCore();
        });
}
```

You may have noticed you need to define some configuration key in `appsettings.json`. Here they are:

```json
{
  // ... the rest of your file
  "OpenIddict": {
    "KeyVaultUri": "https://kcdemo.vault.azure.net/",
    "EncryptionCertificateName": "certificat-openiddict-encryption",
    "SigningCertificateName": "certificat-openiddict-signing"
  }
  // ... the rest of your file
}
```

The names of the certificates are important. They must match the name provided on certificate creation earlier.

Next, you could set the values in the environment variables. To do so, adjust the configuration keys and the way you read them in the code (`OpenIddict:KeyVaultUri` vs `OpenIddict_KeyVaultUri`):

```json
{
  // ... the rest of your file
  "OpenIddict_KeyVaultUri": "https://kcdemo.vault.azure.net/",
  "OpenIddict_EncryptionCertificateName": "certificat-openiddict-encryption",
  "OpenIddict_SigningCertificateName": "certificat-openiddict-signing"
  // ... the rest of your file
}
```

## Seed the Database With a Demo Application Registration

To be able to test later, we need to tell _OpenIddict_ who may authenticate and get a token.

To do so, let’s craft a `Seeder.cs` file at the root of the WebApi project:

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using DemoWebApiWithOpenIddict.Models;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OpenIddict.Abstractions;
using static OpenIddict.Abstractions.OpenIddictConstants;

namespace DemoWebApiWithOpenIddict.Core;

public class OpenIddictSeeder: IHostedService
{
    private readonly IServiceProvider _serviceProvider;

    public OpenIddictSeeder(IServiceProvider serviceProvider)
        => _serviceProvider = serviceProvider;

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        await using var scope = _serviceProvider.CreateAsyncScope();

        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        await context.Database.EnsureCreatedAsync();

        var manager = scope.ServiceProvider.GetRequiredService<IOpenIddictApplicationManager>();

        var application = await manager.FindByClientIdAsync("console");
        if (application == null)
        {
            await CreateApplication(manager);
        }
        else
        {
            await manager.DeleteAsync(application);
            await CreateApplication(manager);
        }
    }

    private static async Task CreateApplication(IOpenIddictApplicationManager manager)
    {
        await manager.CreateAsync(new OpenIddictApplicationDescriptor
        {
            // The ClientId and ClientSecret will be used in the client later in the article.
            ClientId = "console",
            ClientSecret = "388D45FA-B36B-4988-BA59-B187D329C207",
            DisplayName = "Demo OAuth2 App For RefList",
            Permissions =
                {
                    Permissions.Endpoints.Token,
                    Permissions.GrantTypes.ClientCredentials
                }
        });
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}

```

Note: The ClientSecret is a random GUID.

By the way, the client secret should be:

1. Sufficiently random and not guessable.
2. Generated using a cryptographically secure method.
3. At least 256 bits long, typically represented as a 64-character hexadecimal string.

Read more on the topic [here](https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/).

Then, tell the application in `Program.cs` to run it just before `builder.Build()`:

```csharp
logger.LogInformation("Program.cs > Seed the OpenIddict database.");
builder.Services.AddHostedService<OpenIddictSeeder>();

var app = builder.Build();
```

## Create the Migration File

This step allows creating the database tables for _OpenIddict_ in the database created earlier. You need to install the following package first:

```json
dotnet add package Microsoft.EntityFrameworkCore.Design --version 8.0.11
```

Then run:

```powershell
# Browse to your project first, if you're in a large solution
cd DemoWebApiWithOpenIddict
# Then create the migration
dotnet ef migrations add InitOpenIddict --context DemoWebApiWithOpenIddict.Models.ApplicationDbContext --output-dir ./Migrations
# And create the SQL file to run manually or through DbUp, if you use it.
# The "0" means we ask to generate the first migration
# The "-i" option tell EF to generate a script that you can run multiple times (e.g. reset)
dotnet ef migrations script 0 InitOpenIddict --context DemoWebApiWithOpenIddict.Models.ApplicationDbContext -o ./SQL/Patch/001-init-openiddict-tables.sql -i
```

Just in case, edit the `.csproj` so you have the following if the migration commands fail:

```xml
<PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.11">
    <PrivateAssets>all</PrivateAssets>
    <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
</PackageReference>
```

## Run the Tables Creation

Open SSMS and connect to your SQL instance and select the `openiddict` database.

Open the script `001-init-openiddict-tables.sql` from the folder `SQL/Patch` and run it.

Note: You’ll get some warnings. It doesn’t cause a problem finishing the guide and run the application.

## Update the Controllers

### Add an `AuthorizationController`

First, you need to enable authentication to your app : in `Program.cs`, add `app.UseAuthentication();` just before `app.UseAuthorization();` .

Then, under the _Controllers_ folder, add this `AuthorizationController` that will generate the token when requested:

```csharp
/*
 * Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
 * See https://github.com/openiddict/openiddict-core for more information concerning
 * the license and the contributors participating to this project.
 */

using System.Security.Claims;
using DemoWebApiWithOpenIddict.Helpers;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using OpenIddict.Abstractions;
using OpenIddict.Server.AspNetCore;
using static OpenIddict.Abstractions.OpenIddictConstants;

namespace DemoWebApiWithOpenIddict.Controllers;

public class AuthorizationController : Controller
{
    private readonly IOpenIddictApplicationManager _applicationManager;
    private readonly IOpenIddictScopeManager _scopeManager;

    public AuthorizationController(IOpenIddictApplicationManager applicationManager, IOpenIddictScopeManager scopeManager)
    {
        _applicationManager = applicationManager;
        _scopeManager = scopeManager;
    }

    [HttpPost("~/connect/token"), IgnoreAntiforgeryToken, Produces("application/json")]
    public async Task<IActionResult> Exchange()
    {
        var request = HttpContext.GetOpenIddictServerRequest();
        if (request.IsClientCredentialsGrantType())
        {
            // Note: the client credentials are automatically validated by OpenIddict:
            // if client_id or client_secret are invalid, this action won't be invoked.

            var application = await _applicationManager.FindByClientIdAsync(request.ClientId);
            if (application == null)
            {
                throw new InvalidOperationException("The application details cannot be found in the database.");
            }

            // Create the claims-based identity that will be used by OpenIddict to generate tokens.
            var identity = new ClaimsIdentity(
                authenticationType: TokenValidationParameters.DefaultAuthenticationType,
                nameType: Claims.Name,
                roleType: Claims.Role);

            // Add the claims that will be persisted in the tokens (use the client_id as the subject identifier).
            identity.SetClaim(Claims.Subject, await _applicationManager.GetClientIdAsync(application));
            identity.SetClaim(Claims.Name, await _applicationManager.GetDisplayNameAsync(application));

            // Note: In the original OAuth 2.0 specification, the client credentials grant
            // doesn't return an identity token, which is an OpenID Connect concept.
            //
            // As a non-standardized extension, OpenIddict allows returning an id_token
            // to convey information about the client application when the "openid" scope
            // is granted (i.e specified when calling principal.SetScopes()). When the "openid"
            // scope is not explicitly set, no identity token is returned to the client application.

            // Set the list of scopes granted to the client application in access_token.
            identity.SetScopes(request.GetScopes());
            identity.SetResources(await _scopeManager.ListResourcesAsync(identity.GetScopes()).ToListAsync());
            identity.SetDestinations(GetDestinations);

            return SignIn(new ClaimsPrincipal(identity), OpenIddictServerAspNetCoreDefaults.AuthenticationScheme);
        }

        throw new NotImplementedException("The specified grant type is not implemented.");
    }

    private static IEnumerable<string> GetDestinations(Claim claim)
    {
        // Note: by default, claims are NOT automatically included in the access and identity tokens.
        // To allow OpenIddict to serialize them, you must attach them a destination, that specifies
        // whether they should be included in access tokens, in identity tokens or in both.

        return claim.Type switch
        {
            Claims.Name or Claims.Subject => [Destinations.AccessToken, Destinations.IdentityToken],

            _ => [Destinations.AccessToken],
        };
    }
}

```

**Important:** the endpoint you specified in the `Program.cs` (`options.SetTokenEndpointUris`) must match the endpoint in this controller.

### Modify the `WeatherForecast` Controller

To authorize requests from authenticated clients using a valid token, let’s add the `Authorize` attribute:

```csharp
namespace DemoWebApiWithOpenIddict.Controllers
{
    [Authorize(AuthenticationSchemes = OpenIddictValidationAspNetCoreDefaults.AuthenticationScheme)]
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
	    // Your controller's code
    }
}
```

You can place the attribute on some methods if not all of them require authorization. Similarly, you could have controllers not requiring any OAuth2 authorization.

Now, launch your application locally: when you load the `/weatherforecast` endpoint, you should get an error HTTP 401. We expected that!

## Test the Implementation

### Test Locally

To test your Web API locally, use this simple console application code and select the first URL (adjust them to your environment 😉).

The console application needs one package:

```csharp
dotnet add package OpenIddict.Client.SystemNetHttp --version 5.8.0
```

The code below performs two tests:

- The first request should succeed.
- The second one should fail, since we don’t provide the token in the `Authorization` header.

```csharp
using System.Net.Http.Headers;
using Microsoft.Extensions.DependencyInjection;
using OpenIddict.Client;

static string? PickUrl()
{
    Console.WriteLine("Please select a URL:");
    Console.WriteLine("1. https://localhost:7129 (Make sure you are running it locally)");
    Console.WriteLine("2. https://your-app-service-efgmfncjguejeaes.westeurope-01.azurewebsites.net");

    while (true)
    {
        Console.Write("\nEnter 1 or 2: ");
        string choice = Console.ReadLine();

        return choice switch
        {
            "1" => "https://localhost:7129",
            "2" => "https://your-app-service-efgmfncjguejeaes.westeurope-01.azurewebsites.net",
            _ => null
        };
    }
}

var host = PickUrl();
var noPick = host == null;
var pickAttempts = 0;
var maxPickAttempts = 5;

while (noPick)
{
    host = PickUrl();
    noPick = host == null;
    pickAttempts++;
    if (pickAttempts >= maxPickAttempts)
    {
        Console.Write("\nFollow instructions... Restart the app :)");
        Console.ReadLine();
    }
}

if (host == null) return;

Console.WriteLine($"\nWebApi picked: {host}");

ServiceCollection services = ConfigureValidServices(host);
await using var provider = services.BuildServiceProvider();
var token = await GetTokenAsync(provider);

Console.WriteLine("Access token: {0}", token);
Console.WriteLine();

var response = await GetResourceAsync(provider, token, host!, "/weatherforecast");
Console.WriteLine("API response: {0}", response);
Console.WriteLine();
Console.WriteLine("Press key to test oauth-protected endpoint");
Console.ReadLine();

response = await GetResourceAsync(provider, token, host, "/weatherforecast", false);
Console.WriteLine("API response: {0}", response);
Console.WriteLine();
Console.WriteLine("Press key to test oauth-protected endpoint without token bearer");
Console.ReadLine();

static async Task<string> GetTokenAsync(IServiceProvider provider)
{
    var service = provider.GetRequiredService<OpenIddictClientService>();

    var result = await service.AuthenticateWithClientCredentialsAsync(new());
    return result.AccessToken;
}

static async Task<string> GetResourceAsync(IServiceProvider provider, string token, string host, string resource, bool includeAuthBearer = true)
{
    using var client = provider.GetRequiredService<HttpClient>();
    using var request = new HttpRequestMessage(HttpMethod.Get, $"{host}{resource}");
    if (includeAuthBearer)
    {
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
    }

    Console.WriteLine($"Result of calling {host}{resource}");
    using var response = await client.SendAsync(request);
    try
    {
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadAsStringAsync();
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex.Message);
    }
    finally { client.Dispose(); }

    return "Error thrown";
}

static ServiceCollection ConfigureValidServices(string? host, string scope = "demo_api_scope")
{
    var services = new ServiceCollection();

    services.AddOpenIddict()
        // Register the OpenIddict client components.
        .AddClient(options =>
        {
            // Allow grant_type=client_credentials to be negotiated.
            options.AllowClientCredentialsFlow();

            // Disable token storage, which is not necessary for non-interactive flows like
            // grant_type=password, grant_type=client_credentials or grant_type=refresh_token.
            options.DisableTokenStorage();

            // Register the System.Net.Http integration and use the identity of the current
            // assembly as a more specific user agent, which can be useful when dealing with
            // providers that use the user agent as a way to throttle requests (e.g Reddit).
            options.UseSystemNetHttp()
                   .SetProductInformation(typeof(Program).Assembly);

            // Add a client registration matching the client application definition in the server project.
            options.AddRegistration(new OpenIddictClientRegistration
            {
                Issuer = new Uri($"{host}/", UriKind.Absolute),
                // Should match the values in OpenIddictSeeder
                ClientId = "console",
                ClientSecret = "388D45FA-B36B-4988-BA59-B187D329C207"
            });
        });
    return services;
}
```

### Test Remotely

Finally, hit that _Publish_ button in Visual Studio.

Make sure to check that the application loads fine and no errors occurred using the log file.

Then run the console app and choose the remote URL.

You should get the same results!

## Conclusion

There you have it! It was a long one but I spent a couple of days figuring it out completely (AI doesn’t do it all, BTW, but it helps).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}
