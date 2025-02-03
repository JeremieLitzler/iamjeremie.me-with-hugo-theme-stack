---
title: "How to Build a Pseudo-backend With Netlify Functions"
description: "And it is great to host simple MVPs"
image: 2025-02-03-a-json-sticker-held-by-someone.jpg
imageAlt: A JSON sticker held by someone
date: 2025-02-03
categories:
  - Web Development
tags:
  - Netlify
---

## My Need

Last year, I worked on an application integrating Twilio API for an on-call application.

We had a scenario where the primary person on-call couldn’t reply to the customer calling.

Therefore, after a certain time, a scheduled task would trigger a call to the backup person through the Call API at Twilio.

To do so, we need to make the call in the following manner:

```python
message = self.twilio_client.calls.create(
    from_=self.config.TWILIO_PHONE_NUMBER,
    to=on_call_individual.phone_number,
    url=quote(call_instructions, safe=':/')
```

However, the API checks if the `Url` parameter is valid.

Guess what? Locally, the `Url` was valid, but not accessible from Twilio point of view.

## Solution

I developed a quick app using Netlify Functions.

The goal was that the `Url` above would be `[http://domain.com/twiml/instructions/call/{dynamic_value}](http://domain.com/twiml/instructions/call/%7Bdynamic_value%7D)` and would reply:

```xml
<Response>
  <script/>
  <Say>
    <speak-as interpret-as="telephone"> The caller +41123456789 has called the On-call team for a problem. A SMS was sent to you to confirm you're calling the person back. The message contains the caller's number. Thanks. </speak-as>
  </Say>
</Response>
```

### Step 1: Structure Your Project For Netlify

```plaintext
twiml-response-app/
│
├── functions/
│   └── twiml.js
│
├── public/
│   └── index.html
│
├── netlify.toml
└── package.json
```

### Step 2: Initialize And Implement The Project

With `npm init -y`, you can initialize the project.

Then, install the dependencies:

```bash
@netlify/functions
```

Next, create the `index.html` file to provide instructions when loading the base URL.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>TwiML Response App</title>
  </head>
  <body>
    <h1>TwiML Response App</h1>
    <p>
      Use the /twiml/instructions/call/{dynamic_value} endpoint to get TwiML
      responses.
    </p>
    <form>
      <label for="phoneNumber">
        Enter the number:
        <input type="tel" name="phoneNumber" id="phoneNumber" />
      </label>
    </form>
    <section class="link"></section>
    <script>
      const phoneNumberEl = document.querySelector("[name='phoneNumber']");
      const link = document.querySelector(".link");
      phoneNumberEl.addEventListener("keyup", () => {
        event.preventDefault();
        const anchor = document.createElement("a");
        const phoneNumberEncoded = encodeURIComponent(phoneNumberEl.value);
        const href = `${document.location.protocol}//${document.location.host}/twiml/instructions/call/${phoneNumberEncoded}`;
        anchor.innerText = href;
        anchor.href = href;
        anchor.target = "_blank";
        link.innerHTML = "";
        link.appendChild(anchor);
      });
    </script>
  </body>
</html>
```

Then, we create the function `twiml.js` under `functions` directory.

```js
exports.handler = async function (event, context) {
  const path = event.path.split("/");
  const encodedValue = path[path.length - 1];
  const dynamicValue = decodeURIComponent(encodedValue);
  console.log(`Received request at ${event.path}`);

  const xmlResponse = `<?xml version="1.0" encoding="UTF-8"?>
    <Response>
    <Say>
        The caller <say-as interpret-as="telephone">${dynamicValue}</say-as> has called the On-call team for a problem. A SMS was sent to you to confirm you're calling the person back. The message contains the caller's number. Thanks.
    </Say>
</Response>`;

  console.log(`Replying with ${xmlResponse}`);
  return {
    statusCode: 200,
    headers: {
      "Content-Type": "text/xml",
    },
    body: xmlResponse,
  };
};
```

**Be careful with XML**: in the template string, avoid having any leading newline. Otherwise, you’ll get “_error on line 2 at column 10: XML declaration allowed only at the start of the document”._

Finally, let’s configure the `netlify.toml` file with the following content:

```toml
[build]
  functions = "functions"
  publish = "public"

[[redirects]]
  from = "/twiml/*"
  to = "/.netlify/functions/twiml/:splat"
  status = 200
```

First, we tell Netlify where the functions to run are. Note that, by default, Netlify looks up in the `netlify/functions` directory if we don’t provide `functions = "functions"`.

Then `publish = "public"` tell Netlify where is the root directory to serve the application.

Finally, we define a redirect to tell Netlify, on any request to `/twiml/*`, to call the function with the wildcard placeholder (`:splat`) that captures and forwards any additional path segments after `/twiml/` to the destination URL.

### Step 3: Deploy The Application

This step is so simple.

Just create an account at Netlify using your preferred versioning provider and deploy the application from your repository.

The default settings work great.

### Step 4: Test The Application

Browse to the URL provided by Netlify and enter a value in the input.

Click the link that appears below to preview the XML generated.

## Conclusion

There you have it! Now, you can use this hosted application locally and test Twilio API against a URL available on the Internet.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [RealToughCandy.com](https://www.pexels.com/photo/a-person-holding-a-paper-11035481/)
