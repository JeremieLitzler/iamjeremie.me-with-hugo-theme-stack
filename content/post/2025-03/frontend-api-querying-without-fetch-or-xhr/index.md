---
title: "Frontend API Querying Without Fetch or XHR"
description: "Once upon a time, people used XHR . Everyone today (should) uses the fetch API, native to JavaScript. But do you know about the third way to query data?"
image: 2025-03-31-a-question-mark-drawn-with-chalk.jpg
imageAlt: A question mark drawn with chalk
date: 2025-03-31
categories:
  - Web Development
tags:
  - HTML
  - JavaScript
---

Less than twenty years ago, developers used the XHR request, either in vanilla JavaScript, or through jQuery `ajax()` method.

Then, EMCAScript 2015 came out and introduces `fetch` and its promise-based logic. Querying data with it improved a lot developer experience.

With modern JS came Angular, then React and Vue, to quote the main frameworks used today, we all use `fetch` under a layer of abstraction.

Fetching data is easy as long as you understand a minimum how promises work.

## The Third Way

While `fetch` is great, on a project last year, I was asked to build a frontend with vanilla HTML and JavaScript to keep dependencies to the bare minimum.

No XHR, no `fetch` with or without frameworks.

> “How is that even possible?”, I wondered.

Well, that’s the third way. It’s probably the way before XHR existed. Do you know about its origin and history? [Tell me on X](https://x.com/LitzlerJeremie)!

## The Example

Let’s take an example. You have a login page with a form composed of two inputs: an email and a password.

On submit, the form sends credentials to a backend endpoint based on Flask, a Python popular web framework.

That endpoint responds at `POST /app/login` and returns the following possible JSON response:

```json
// on success
{
  "success": true,
  "error": ""
  "next_page": "/path/to/next/page"
}

// on failure
{
  "success": false,
  "error": "Credentials are invalid"
}
```

## The Markup

Let’s start to code the example with the markup.

A form is defined with a `form` element and several `input` elements combined with `label` (always) and a button that allows you to submit the form.

```html
<!-- Do you see special part? Yes, the key is `target="responseFrame"` and its associated iframe -->
<form
  id="loginForm"
  method="POST"
  action="{{ url_for('frontend.execute_login', next=next) }}"
  target="responseFrame"
  class="p-4 border rounded shadow-sm"
>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email" name="email" required />
  </div>
  <div class="password-block mb-3">
    <label for="password" class="form-label">Mot de passe</label>
    <input type="password" class="form-control" id="password" name="password" />
  </div>
  <div class="d-grid">
    <button id="loginButton" type="submit" class="btn btn-primary">
      Se connecter
    </button>
  </div>
  <div id="feedbackMessage" class="mt-3 alert" style="display: none;"></div>
</form>
<!-- This hidden iframe to receive form submissions -->
<iframe name="responseFrame" id="responseFrame" hidden></iframe>
```

## The JavaScript

### Let’s Start With the Backbone

I’ll give you the full code in the article, step-by-step: first, we register the `DOMContentLoaded` event with all the methods we need to handle a login.

```jsx
// The form element
const loginForm = document.getElementById("loginForm");
// The email element
const emailInput = document.getElementById("email");
// The password
const passwordContainer = document.querySelector(".password-block");
// The submit button
const submitBtn = loginForm.querySelector('button[type="submit"]');
// The magical element...
const responseFrame = document.getElementById("responseFrame");

document.addEventListener("DOMContentLoaded", function () {
  // handles the scenario where the SSO login
  // I won't go into the details in the article
  emailInput.addEventListener("input", useSsoLoginButton);

  // moves focus to login button on exiting the email input
  emailInput.addEventListener("blur", function () {
    submitBtn.focus();
  });

  // show a "connecting" message while we wait for the API response
  loginForm.addEventListener("submit", showConnecting);

  // process the API response
  responseFrame.addEventListener("load", processLoginResponse);
});
```

### Show the Connecting Message

This one is simple: as long as the API response didn’t reply, let’s disable the button and show a message:

```jsx
function showConnecting(e) {
  submitBtn.disabled = true;
  showFeedback("Connecting...", false);
}
```

### Process the API Response

Then, at some point the API will send the response. But how do you “catch” the response?

Remember that `target="responseFrame"`? Well, it instructed the browser to forward to the `responseFrame` element the API response.

So we have this implementation:

```jsx
// `this` in the function corresponds to the `responseFrarme` element
function processLoginResponse() {
  try {
    // By forwarding the API response, the browser has "filled the
    // iframe document's body content with the response data.
    // Since it is a string, let's first parse it.
    const response = JSON.parse(this.contentDocument.body.textContent);
    // If the login failed, we call `showFeedback` to show the error details
    if (!response.success) {
      // the feedback message takes the response's error value or a fallback
      showFeedback(response.error || "Failed to log you in...", true);
      // and re-enable the login button to allow a new attempt.
      submitBtn.disabled = false;
      return;
    }
    // Otherwise, let's switch the feedback message to provide
    // the user feedback that we are about to redirect
    showFeedback("Redirecting...", false);
    // ... and redirect the user to the next_page when the
    // timeout ends
    // The timeout is only to show the redirecting message
    let timeoutId = setTimeout(() => {
      clearTimeout(timeoutId);
      window.location.href = response.next_page;
    }, 250);
  } catch (error) {
    // Just make sure to catch all errors
    console.error("Error parsing response:", error);
    showFeedback(
      "An error has occurred. Open DevTools, try again and report the fault to the administrator.",
      true,
    );
    submitBtn.disabled = false;
  }
}
```

That’s it!

BTW, you don’t need a `event.preventDefault()`. With this strategy, the submit action doesn’t reload the page. You handle everthing, on success or not, inside `processLoginResponse`.

## Conclusion

Have you learned something today? I sure did when I coded this.

By the way, I learned about this using Claude.ai, who guided me through this and helped discover a (forgotten) technique that, I think, we should all know.

To be honest, the AI had trouble to give this solution at first, trying the other two solutions…

<!-- more -->

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Photo by [Pixabay](https://www.pexels.com/photo/question-mark-on-chalk-board-356079/).
