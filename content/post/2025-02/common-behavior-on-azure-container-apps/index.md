---
title: "Common Behavior on Azure Container Apps"
description: "When you deploy an container app on Azure or any cloud provider, you need to know this."
image: 2025-02-17-tunnel-written-on-a-metal-structure.jpg
imageAlt: “Tunnel” written on a metal structure
date: 2025-02-17
categories:
  - Web Development
tags:
  - Python
  - Security
---

I worked on a REST API in Python and it integrated Twilio to handle incoming calls.

I had set up the webhook with an HTTPS protocol.

To secure the webhook, I need to parse Twilio’s signature from the headers to validate it came from them.

You can start in [Twilio documentation](https://www.twilio.com/docs/messaging/tutorials/how-to-receive-and-reply/python) to understand that works. You can even ask the [Twilio Docs AI](https://help.twilio.com/).

It implemented everything and I was ready to test. But then…

## The Issue

When I made the call, Twilio’s lady told me: “Sorry, an application error occurred.”

I had made sure I logged all the parts that make the signature before deploying:

- the Auth token, provided by Twilio,
- the request URL,
- the payload,
- the actual signature sent by Twilio.

What did I learn?

The URL struck me as the only problematic value: it was missing the “s” on the “http”…

Therefore, when I calculated the signature from the Twilio API, it gave me a different value, which ended the request in an error.

## Where Does The `HTTP` Come From

This behavior came from the way Azure Container Apps handles HTTPS traffic. Here’s what I understood:

1. The external request to the app arrives over HTTPS. Twilio call logs confirmed that.
2. The Azure Container App terminates the SSL/TLS connection at its load balancer or reverse proxy.
3. The request is then forwarded to the Flask application using HTTP internally.

As a result, Flask sees the internal HTTP request, not the original HTTPS request. This is a common setup in cloud environments for performance and security reasons.

## How Do You Solve This Issue

To get the original HTTPS URL, you can try the following:

### Method 1

Check if Flask is behind a proxy by looking for the `X-Forwarded-Proto` header:

```python
from flask import request

if request.headers.get('X-Forwarded-Proto') == 'https':
    # The original request was HTTPS
    original_url = 'https://' + request.host + request.path
else:
    # Use the regular request.url
    original_url = request.url

```

### Method 2

If that doesn’t work, you might need to configure Flask to trust the proxy headers:

```python
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

```

This tells Flask to trust the `X-Forwarded-Proto` header.

If you’re still having issues, you might need to check your Azure Container Apps configuration to ensure it’s properly setting the `X-Forwarded-Proto` header.

In my use case, I used the first method with a slight difference: I used `replace` method to rewrite the URL.

```python
        no_header = 'header not sent'
        request_protocol = request.headers.get("X-Forwarded-Proto", no_header)
        if request_protocol == 'https':
            return request.url.replace('http://', 'https://', 1)
        else:
            return request.url
```

## Conclusion

Running an application inside a container often means that you have a reverse proxy. And between the reverse proxy and the application, the communication doesn’t require `https`.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Jonny Gios](https://unsplash.com/@supergios?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/a-close-up-of-a-train-on-a-train-track-avLaWXizuWM?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
