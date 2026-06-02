---
title: "Injecting Configuration To A Service In a .NET Application"
description: "And three things to know to do it well."
image: 2026-06-01-wooden-peg-figures-forming-an-organizational-hierarchy-chart.jpg
imageAlt: Wooden peg figures forming an organizational hierarchy chart
date: 2026-06-01
categories:
  - Software Development
tags:
  - DotNet
  - CSharp
---

In the following example, `MyOtherService` is registered in the IOC of a .NET application.

A `Service1` must also be registered into the IOC to ensure `MyOtherService` can work with it.

```csharp
services.AddScoped(serviceProvider =>
{
  var dep1 = serviceProvider.GetRequiredService<Service1>();
  var config = serviceProvider.GetRequiredService<IConfiguration>();
  return new MyOtherService(dep1, config.GetSection("MySection").Get<MySectionOptions>());
});
```

`MyOtherService` and `MySectionOptions` are defined as follows:

```csharp
// MySectionOptions.cs
public class MySectionOptions
{
    [Required]
    public string ConnectionString { get; set; }

    [Range(1, 100)]
    public int MaxRetries { get; set; }
}
```

```csharp
// MyOtherService.cs
public class MyOtherService
{
    private readonly Service1 _service1;
    private readonly MySectionOptions _options;

    public MyOtherService(Service1 service1, MySectionOptions options)
    {
        _service1 = service1;
        _options = options;
    }

    public void DoWork()
    {
        var opts = _options.CurrentValue; // always fresh
        var conn = opts.ConnectionString;
    }
}
```

There are caveats about this syntax. What are they?

## Caveats

### Scope Delta

If you were to register `MyOtherService` as a singleton and `Service1` as scoped or transient, the latter gets captured and lives for the app's lifetime, which defeats its intended shorter lifecycle. Ensure dependent services use the same lifetime to avoid issues.

### `ValidateOnBuild` Bypass

Factory-based registrations aren’t checked at startup. So, if `Service1` or `IConfiguration` is missing, you won't know until the first resolution at runtime. You lose the safety net of `ValidateScopes` / `ValidateOnBuild`.

When you enable validation in `Program.cs`:

```csharp
builder.Host.UseDefaultServiceProviderFactory(new ServiceProviderOptions
{
    ValidateOnBuild = true,
    ValidateScopes = true
});
```

With the following constructor-based registration,

```csharp
services.AddSingleton<MyOtherService>(); // depends on Service1 via constructor
// Service1 is never registered
```

The app crashes immediately on startup with:

```plaintext
System.AggregateException: Some services are not able to be constructed
(Error while validating the service descriptor 'ServiceType: MyOtherService'):
Unable to resolve service for type 'Service1'
```

You find the bug before any request hits the server.

If you use factory-based registration,

```csharp
services.AddSingleton(sp =>
{
    var dep = sp.GetRequiredService<Service1>(); // Service1 never registered
    return new MyOtherService(dep);
});
```

Then, the app starts without errors. `ValidateOnBuild` sees the factory delegate as a black box — it can't inspect what `GetRequiredService` calls are inside. The `InvalidOperationException` only fires when something first requests `MyOtherService`, potentially minutes, hours, or days later in production under a specific code path.

That's the core tradeoff: factory delegates give you flexibility but move dependency errors from build-time to runtime, which is exactly the class of bugs `ValidateOnBuild` was designed to eliminate.

### Manual Options Binding

Calling `config.GetSection(...).Get<T>()` inside the factory bypasses the Options pattern. You lose `IOptionsMonitor<T>` reload support and validation via data annotations.

Say we have:

```csharp
public class MySectionOptions
{
    [Required]
    public string ConnectionString { get; set; }

    [Range(1, 100)]
    public int MaxRetries { get; set; }
}
```

With manual binding in the factory, three things can go wrong:

1. Validation attributes are ignored: `Get<T>()` just maps values — it doesn't run `[Required]’ or `[Range]`. If `appsettings.json`has`"MaxRetries": 999’ or omits `ConnectionString` entirely, no error. You get a silent null or invalid value at runtime.

   With the Options pattern:

   ```csharp
   services.AddOptions<MySectionOptions>()
       .BindConfiguration("MySection")
       .ValidateDataAnnotations()
       .ValidateOnStart(); // fails at startup, not at first use
   ```

   The app won’t start if the config is invalid.

2. No hot reload: if `appsettings.json` changes at runtime (common with Azure App Configuration, Kubernetes ConfigMaps, etc.), your singleton captured a snapshot at construction time. It’s frozen as long as the application runs.

   If `MyOtherService` takes `IOptionsMonitor<MySectionOptions>` instead:

   ```csharp
   public class MyOtherService
   {
       private readonly IOptionsMonitor<MySectionOptions> _options;

       public MyOtherService(IOptionsMonitor<MySectionOptions> options)
       {
           _options = options;
       }

       public void DoWork()
       {
           var current = _options.CurrentValue; // always fresh
       }
   }
   ```

   Every access reflects the latest config without restarting the app.

3. No named options: `Get<T>()` gives you one flat binding. The Options pattern supports named instances out of the box:

   ```csharp
   services.Configure<MySectionOptions>("Primary", config.GetSection("Primary"));
   services.Configure<MySectionOptions>("Secondary", config.GetSection("Secondary"));
   ```

   Then resolved via `IOptionsSnapshot<T>.Get("Primary")`. No equivalent exists with manual binding without reinventing the plumbing yourself.

## Conclusion

So, if we were to rewrite the registration and update the class accordingly, we would obtain the following:

First, the `MyOtherService` constructor changes to use `IOptionsMonitor`:

```csharp
public class MyOtherService
{
    private readonly Service1 _service1;
    private readonly IOptionsMonitor<MySectionOptions> _options;

    public MyOtherService(Service1 service1, IOptionsMonitor<MySectionOptions> options)
    {
        _service1 = service1;
        _options = options;
    }

    public void DoWork()
    {
        var opts = _options.CurrentValue; // always fresh
        var conn = opts.ConnectionString;
    }
}
```

Then, in the `Programe.cs`,

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// 1. Validate DI graph at startup
builder.Host.UseDefaultServiceProviderFactory(new ServiceProviderOptions
{
    ValidateOnBuild = true,
    ValidateScopes = true
});

// 2. Options with validation — fails at startup if config is invalid
builder.Services
    .AddOptions<MySectionOptions>()
    .BindConfiguration("MySection")
    .ValidateDataAnnotations()
    .ValidateOnStart();

// 3. Plain constructor injection — no factory needed
builder.Services.AddSingleton<Service1>();
builder.Services.AddSingleton<MyOtherService>();

var app = builder.Build();
```

What this gives you compared to the original:

- **Missing dependency** is caught at startup (`ValidateOnBuild`)
- **Invalid config** is caught at startup (`ValidateOnStart` + `ValidateDataAnnotations`)
- **Captive dependency** is caught at startup (`ValidateScopes`)
- **Config hot reload** is handled (`IOptionsMonitor`)
- **No factory** means the entire DI graph is transparent and inspectable

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by Ann H on Pexels—`https://www.pexels.com/photo/pawns-connected-with-wooden-sticks-7422341/`.
