---
title: "Common Use Cases of Action Filters In ASP.Net WebAPI"
description: "In ASP.Net WebAPI, Action Filters are commonly used for various cross-cutting concerns that need to be applied to multiple action methods or controllers"
image: 2025-09-08-several-coffee-cups.jpg
imageAlt: Several coffee cups
date: 2025-09-08
categories:
  - Web Development
tags:
  - ASP.Net
  - Web API
  - Csharp
---

Here are some of the common use cases for Action Filters:

## The Use Cases

### Authentication and Authorization

You can implement action filters on authentication and authorization logic. The result of such use case ensures that only authorized users can access certain actions or controllers.

```csharp
public class CustomAuthorizeAttribute : AuthorizeAttribute
{
    protected override bool IsAuthorized(HttpActionContext actionContext)
    {
        // Custom authentication logic
    }
}
```

The above is .NET Framework specific so let me give your .NET Core version as well:

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

public class CustomAuthorizeAttribute : Attribute, IAuthorizationFilter
{
    public void OnAuthorization(AuthorizationFilterContext context)
    {
        // Custom authorization logic
        var user = context.HttpContext.User;
        if (!user.Identity.IsAuthenticated)
        {
            context.Result = new UnauthorizedResult();
            return;
        }
        // Other logic...
    }
}
```

### Logging and Diagnostics

You can also employ action filters to log details of the HTTP request and response, which can be useful for debugging and monitoring.

```csharp
public class LoggingFilterAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(HttpActionContext actionContext)
    {
        // Log request details before it is processed
    }
    public override void OnActionExecuted(HttpActionExecutedContext actionExecutedContext)
    {
        // Log response details after the business logic is executed.
    }
}
```

In .NET Core style, the code changes slightly. The parameter types change from `HttpActionContext` and `HttpActionExecutedContext` (.NET Framework) to `ActionExecutingContext` and `ActionExecutedContext` (ASP.NET Core).

Registration and application work nearly the same, but may use DI and `ServiceFilter` or `TypeFilter` for injected filters.

```csharp
using Microsoft.AspNetCore.Mvc.Filters;

public class LoggingFilterAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(ActionExecutingContext context)
    {
        // Log request details before it is processed
    }

    public override void OnActionExecuted(ActionExecutedContext context)
    {
        // Log response details after the business logic is executed.
    }
}
```

A concrete use case would be to log the elapsed time to process the request by starting a watcher in `OnActionExecuting` and stopping it on `OnActionExecuted`.

### Exception Handling

If you need to handle exceptions globally, action filters allow for a consistent approach to error handling across multiple controllers or actions.

```csharp
public class CustomExceptionFilterAttribute : ExceptionFilterAttribute
{
    public override void OnException(HttpActionExecutedContext context)
    {
        // Custom exception handling logic
    }
}
```

With .NET Core, it would look like this:

```c#
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

public class CustomExceptionFilterAttribute : ExceptionFilterAttribute
{
    public override void OnException(ExceptionContext context)
    {
        // Custom exception handling logic
        // For example: set context.Result to a custom IActionResult, log exception

        context.Result = new ObjectResult(new { Error = context.Exception.Message })
        {
            StatusCode = 500
        };
        context.ExceptionHandled = true;
    }
}
```

### Caching

Action filters can manage caching strategies by adding caching headers to the response or implementing server-side caching mechanisms.

The code looks exactly like the logging example.

### Input Validation

One last common use case is validation of the incoming request data before the action method executes.

The code looks exactly like the logging example.

### More reading on the topic

For Microsoft Documentation, here are a few articles to dive deeper into the topic with .NET Framework:

- [ASP.NET Web API Filters](https://learn.microsoft.com/en-us/aspnet/web-api/overview/advanced/http-message-handlers)
- [Using Action Filters in ASP.NET Web API](https://learn.microsoft.com/fr-fr/aspnet/web-api/overview/advanced/http-message-handlers#example-x-http-method-override)
- [Exception Handling in ASP.NET Web API](https://learn.microsoft.com/en-us/aspnet/web-api/overview/error-handling/web-api-global-error-handling)

For .NET Core, go read:

- [this guide](https://learn.microsoft.com/en-us/aspnet/core/mvc/controllers/filters?view=aspnetcore-9.0) for filters.
- [this guide](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling-api?view=aspnetcore-9.0&tabs=minimal-apis) for exceptions.

## How do you use them in the controllers?

To use Action Filters in ASP.Net WebAPI controllers, you can apply them in several ways:

### At the Action Method Level

You can apply an Action Filter to a specific action method by decorating the method with the filter attribute.

```csharp
public class ProductsController : ApiController
{
    [LoggingFilter]
    [ValidateModel]
    public IHttpActionResult Post(Product product)
    {
        // Action method logic
        return Ok();
    }
}
```

### At the Controller Level

You can apply an Action Filter to all action methods within a controller by decorating the controller class with the filter attribute.

```csharp
[LoggingFilter]
[Authorize]
public class ProductsController : ApiController
{
    [ValidateModel]
    public IHttpActionResult Post(Product product)
    {
        // Action method logic
        return Ok();
    }

    public IHttpActionResult Get(int id)
    {
        // Action method logic
        return Ok();
    }
}
```

### Globally

You can apply an Action Filter globally to all controllers and actions in your WebAPI application.

This is done by registering the filter in the `WebApiConfig` class.

```csharp
public static class WebApiConfig
{
    public static void Register(HttpConfiguration config)
    {
        // Other configuration code...

        config.Filters.Add(new LoggingFilterAttribute());
        config.Filters.Add(new CustomExceptionFilterAttribute());
    }
}
```

The above works for .NET Framework applications. On .NET Core, you would do it in the `ConfigureServices` method:

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers(options =>
    {
        options.Filters.Add(typeof(LoggingFilterAttribute)); // Register globally
        options.Filters.Add(typeof(CustomExceptionFilterAttribute)); // Register globally
    });
}
```

or in .NET 6+ (`Program.cs`):

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers(options =>
{
    options.Filters.Add<LoggingFilterAttribute>();
    options.Filters.Add<CustomExceptionFilterAttribute>();
});

var app = builder.Build();
app.MapControllers();
app.Run();
```

## Conclusion

Action filters in ASP.NET Web API and .NET Core are a versatile mechanism that enables developers to manage centrally cross-cutting concerns such as **authentication**, **logging**, **exception handling**, **caching**, and **input validation** across controllers and actions.

By configuring these filters at the action, controller, or global scope, application code remains clean and maintainable, while crucial infrastructure tasks are handled consistently.

Leveraging action filters improves security, reliability, and performance—making them essential for robust API development in modern .NET environments.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Lucas Andrade](https://www.pexels.com/photo/man-hand-pouring-coffee-20643647/).
