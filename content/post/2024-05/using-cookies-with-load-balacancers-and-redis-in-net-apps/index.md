---
title: "Using cookies with load-balacancers and Redis in .NET apps"
description: "A colleague of mine recently worked on a problem of cookie for a .NET application backend using cookie to validate some business logic. Here how it is done."
image: images/2024-05-17-some-started-to-eat-a-cookie.jpg
imageAlt: "Someone started to eat a cookie."
date: 2024-05-17
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Redis
  - DoNet Core
---

## The background of the issue

The project used infrastructure based on multiple pods using Openshift and this allows load-balancing the frontend and backend.

On the project, we used Redis to store the cookies.

## The problem

Without load-balancing, no issue occurred. The application set the cookies and the applications worked as attended.

When the project added load-balancing, the applications stopped working.

Why?

## The solution

The cookies needed for the business logic to work were absent.

How did my colleague resolve the issue?

First by creating the session store class to handle CRUD operation in the Redis cache:

```csharp
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Caching.Distributed;

namespace My.Project.Business.Core.Services.Cache
{
    public class RedisCacheSessionStore : ITicketStore
    {
        private readonly IDistributedCache _cache;
        private const string KeyPrefix = "auth-myapp-";

        public RedisCacheSessionStore(IDistributedCache cache)
        {
            _cache = cache;
        }

        public async Task<string> StoreAsync(AuthenticationTicket ticket)
        {
            var key = $"{KeyPrefix}-{Guid.NewGuid()}";
            var value = Serialize(ticket);

            await _cache.SetAsync(key, value);

            return key;
        }

        public async Task RenewAsync(string key, AuthenticationTicket ticket)
        {
            var value = Serialize(ticket);

            await _cache.SetAsync(key, value);
        }

        public async Task<AuthenticationTicket> RetrieveAsync(string key)
        {
            var value = await _cache.GetAsync(key);

            return value == null ? null : Deserialize(value);
        }

        public async Task RemoveAsync(string key)
        {
            await _cache.RemoveAsync(key);
        }

        private static byte[] Serialize(AuthenticationTicket source)
        {
            return TicketSerializer.Default.Serialize(source);
        }

        private static AuthenticationTicket Deserialize(byte[] source)
        {
            return source == null ? null : TicketSerializer.Default.Deserialize(source);
        }
    }

}
```

From there, my colleague modified the cookie manager class to append or get cookies.

```csharp
using DocumentFormat.OpenXml.InkML;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Caching.Distributed;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;

namespace My.Project.Business.Core.Services.Cache
{
    public class RedisCookieManager : ICookieManager
    {
        private readonly IDistributedCache _cache;

        public RedisCookieManager(IDistributedCache cache)
        {
            _cache = cache;
        }

        string? ICookieManager.GetRequestCookie(HttpContext context, string key)
        {

            var result = _cache.GetString(key);
            return result;
        }

        void ICookieManager.AppendResponseCookie(HttpContext context, string key, string? value, CookieOptions options)
        {
            //var redisKey = $"{sessionId}:cookies:{key}";

            var optionsWithExpiry = new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(12)
            };

            _cache.SetString(key, value, optionsWithExpiry);
        }

        void ICookieManager.DeleteCookie(HttpContext context, string key, CookieOptions options)
        {
            var redisKey = key;
            _cache.Remove(redisKey);
        }
    }

}
```

Then, my colleague added the cookie manager class as a `Singleton` in the extension method registering the services (`public static void RegisterServices(this IServiceCollection services, IConfigurationRoot configuration, bool isTestEnvironment)`)

```csharp
services.AddSingleton<ICookieManager, RedisCookieManager>(provider =>
{
    var cache = provider.GetRequiredService<IDistributedCache>();
    return new RedisCookieManager(cache);
});
```

Finally, my colleague updated `Program.cs` startup code to use the new dependency to read the cookie from `OpenIdConnect`:

```csharp
public partial class Program {
  private const string API_CORS_POLICY = "ApiCorsPolicy";

    public static void Main(string[] args) {
        var builder = WebApplication.CreateBuilder(args);
        // Dependency Injection for Services
        builder.Services.RegisterServices(Configuration);
        // Dependency Injection for Controllers
        builder.Services.RegisterControllers(Configuration);
        // Register Loggers
        builder.Logging.RegisterLoggingProviders(Configuration, builder.Services);
        builder
            .AddCookie()
            .AddOpenIdConnect(options => {
                // ... some code is omitted for brevity
                OnTokenValidated = context => {
                    var idToken = context.SecurityToken.RawData; // Token ID
                    var accessToken = context.SecurityToken.RawData; // Access Token
                    var refreshToken = context.SecurityToken.RawData; // Refresh Token
                    var sessionId = context.Principal.FindFirst(ClaimTypes.NameIdentifier)?.Value;
                    var key = $ "{sessionId}:cookies:app-auth";

                    context.HttpContext.RequestServices.GetRequiredService<ICookieManager>()
                            .AppendResponseCookie(context.HttpContext, key, accessToken, new CookieOptions());
                        return Task.CompletedTask;
                        }
                    };
                });

        var app = builder.Build();
        app.Run();
    }
}
```

Credit: Photo by [Vyshnavi Bisani](https://unsplash.com/@vyshnavibisani?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/brown-round-cookie-on-white-surface-z8kriatLFdA?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
