---
title: "What is Statelessness in software engineering?"
description: "A stateless service is a type of service that does not retain any internal state between calls from clients. Let’s review the concept."
image: 2025-06-02-a-sticker-saying-get-me-some-api-now.jpg
imageAlt: A sticker saying, “Get me you some API, now.”
date: 2025-06-02
categories:
  - Software Development
---

A stateless service processes each request from a client independently, with no knowledge of previous interactions. 

This makes stateless services highly scalable and easier to manage because they don’t require maintaining session information between requests.

## An example using C#

Let’s create a simple stateless web API using ASP.NET Core.

1. First, create a new ASP.NET Core Web API project using the built-in terminal in Visual Studio or Rider:

    ```bash
    dotnet new webapi -n StatelessServiceExample
    cd StatelessServiceExample
    ```

2. Then, update the example `WeatherForecastController` to be a simple stateless service:

    ```csharp
    using Microsoft.AspNetCore.Mvc;
    
    namespace StatelessServiceExample.Controllers
    {
        [ApiController]
        [Route("[controller]")]
        public class GreetingController : ControllerBase
        {
            [HttpGet]
            public IActionResult GetGreeting(string name)
            {
                if (string.IsNullOrEmpty(name))
                {
                    return BadRequest("Name parameter is required");
                }
    
                var greeting = $"Hello, {name}!";
                return Ok(greeting);
            }
        }
    }
    ```

3. Finally, run the service:

    ```bash
    dotnet run
    ```

    You can now access the stateless service by navigating to `http://localhost:5000/greeting?name=John` in your browser or using tools like `curl` or Postman.

    This sample application doesn’t retain any information about previous requests from the same client.

## Use Cases for Stateless Services

### 1. Microservices

Microservices often communicate over the network and need to be easily scalable.

Statelessness ensures each instance of a microservice can handle any request without relying on a shared state.

For example, you can consider an authentication service that verifies user credentials without storing session data, as stateless. It simply takes a token and verifies that it’s valid according to its predefined rules and returns, for each request, the result it calculated.

### 2. Serverless Functions (e.g., AWS Lambda, Azure or Netlify Functions)

Serverless architectures benefit from stateless services because each function invocation is independent. 

This allows the cloud provider to scale, in compute power or in quantity, the functions seamlessly.

For example, you can consider an image processing function that processes uploaded images and returns the result, as stateless.

### 3. RESTful APIs

Software engineers create RESTful APIs to be stateless to improve scalability and simplicity. 

Each API call contains **all the information needed** to process the request.

## Benefits of Stateless Services

In other words, we can describe stateless services or applications as:

- **Scalable**, meaning it’s easier to add new instances without complex session synchronization.
- **Reliable** because there is a reduced risk of failure due to a lack of a shared state, making the service more robust.
- **Maintainable**, as it simplifies the codebase. Each request remains self-contained and doesn’t depend on previous requests.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [RealToughCandy.com](https://www.pexels.com/photo/programmer-holding-a-paper-cutout-with-an-api-quote-11035364/)