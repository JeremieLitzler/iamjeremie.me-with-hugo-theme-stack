---
title: "Getting information from JWT in C#"
description: "JWT authentication is a token-based stateless authentication mechanism. It is popularly used as a client-side-based stateless session and it is typically encoded & signed. But how do you decode it? Let’s look at this."
image: images/2024-05-24-html-code-handling-the-failed-on-authentication.jpg
imageAlt: "HTML code handling the failed on authentication"
date: 2024-05-24
categories:
  - Web Development
tags:
  - Tip Of The Day
  - Authentication
---

Below, I’ll describe a simple way to read the header and extract an information.

## Logic

### Which `usings`

```csharp
using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Text;
using Microsoft.AspNetCore.Http;
using Microsoft.IdentityModel.Tokens;
```

### Extract the JWT value from the request

This is the first step. The header used to pass the JWT value is `Authorization`:

```csharp
public static string GetJwtTokenFromRequest(HttpContext context)
{
    var authHeader = context.Request.Headers["Authorization"].FirstOrDefault();

    if (string.IsNullOrEmpty(authHeader))
    {
      //no authorization header
      return null;
    }

    if (!authHeader.StartsWith("Bearer "))
    {
      //no bearer but authorization header returned
      return authHeader;
    }

    //bearer present, returning trimmed value
    return authHeader.Substring("Bearer ".Length).Trim();
}
```

The code above actually takes care of the presence of `Bearer` in the header value.

It is best practice to use it (at least, I’ve never seen passing or receiving the `Authorization` without `Bearer`)

### Decode the JWT value

Let’s dive into the decoding.

The code below actually validates the siging key (see [ValidateIssuerSigningKey](https://learn.microsoft.com/en-us/dotnet/api/microsoft.identitymodel.tokens.tokenvalidationparameters.validateissuersigningkey?view=msal-web-dotnet-latest#microsoft-identitymodel-tokens-tokenvalidationparameters-validateissuersigningkey)).

To validate other parts, [visit the Microsoft website](https://learn.microsoft.com/en-us/dotnet/api/microsoft.identitymodel.tokens.tokenvalidationparameters?view=msal-web-dotnet-latest).

```csharp
public static string GetInformationFromToken(HttpContext context, string dataProp)
{
  var token = GetJwtTokenFromRequest(context);
  if (string.IsNullOrEmpty(token))
  {
    //token is empty, returning null
    return null;
  }

  try
  {
    var tokenHandler = new JwtSecurityTokenHandler();
    tokenHandler.ValidateToken(token, new TokenValidationParameters
    {
      ValidateIssuerSigningKey = true,
      ValidateIssuer = false,
      ValidateAudience = false
    }, out SecurityToken validatedToken);

    var jwtToken = (JwtSecurityToken)validatedToken;
    //the JwtSecurityToken contains a property "Claims" from which you extract a data property that you want to read
    var targetInfo = jwtToken.Claims.FirstOrDefault(c => c.Type == dataProp);

    if (targetInfo != null)
    {
      return targetInfo.Value;
    }

    return null;
  }
  catch (Exception e)
  {
    // Token validation failed
    return null;
  }
}
```

## Usage

Then, you simply call like so:

```csharp
var dataExtractedFromJwt =
    JwtTokenHelper.GetInformationFromToken(
        HttpContextAccessor.HttpContext,
        "some_data_in_jwt");
```

Credit: Photo by [Markus Spiske](https://unsplash.com/@markusspiske?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/text-6pflEeSzGUo?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
