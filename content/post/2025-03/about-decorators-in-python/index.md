---
title: "About Decorators In Python"
description: "Decorators in Python are equivalent to Custom Attributes in C#. Let’s check them out."
image: 2025-03-03-4-colored-brushes.jpg
imageAlt: 4-colored brushes
date: 2025-03-03
categories:
  - Web Development
tags:
  - Python
---

Decorators in Python are a way to modify or enhance functions or classes without directly changing their source code.

They use the concept of closures and higher-order functions to wrap the original function or class, adding functionality before or after the wrapped code executes.

It is similar to Router guards with Vue Router or custom attributes or middleware in C#.

Let’s break down step by step what you can code on and how it works .

## Basic Example

Let’s start with the basics. You define a Python decorator as follows:

```python
def my_decorator(original_function):
    def wrapper_function(*args, **kwargs):
        # Code to execute before the `original_function`
        result = original_function(*args, **kwargs)
        # Code to execute after the `original_function`
        return result
    return wrapper_function
```

Now, let’s look at specific use cases.

## Decorator without input from the caller

This is the simplest form of a decorator. It doesn’t have any arguments other than the function it’s decorating. In between, it prints out `In decorator before calling {function name}` and `Function {function name} called. Completing decorator logic...`.

```python
def log_function_call(func):
    def wrapper(*args, **kwargs):
        print(f"In decorator before calling <{func.__name__}>")
        result = func(*args, **kwargs)
        print(f"Function <{func.__name__}> called. Completing decorator logic...")
        return result
    return wrapper

@log_function_call
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Ouputs:
# "In decorator before calling <greet>
# "Function <greet> called. Completing decorator logic...
```

In this example, the `log_function_call` decorator adds logging before and after the function call without needing any input from the caller.

## Decorator with input from the caller

When you need to pass arguments to the decorator itself, you need to add another layer of functions.

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Bob")

```

In this case, the `repeat` decorator has an argument `times` that determines how many times the decorated function `greet` should be called.

Here’s how it works:

1. `repeat(times)` is called with the argument, returning the `decorator` function.
2. The `decorator` function then wraps the original function (`greet` in this case).
3. When `greet` is called, it actually calls the `wrapper` function, which executes the original `greet` function `times` number of times.

## The Order Matters

You can combine multiple decorators:

```python
@decorator1
@decorator2(arg)
def my_function():
    pass

```

This is equivalent to:

```python
my_function = decorator1(decorator2(arg)(my_function))

```

Ordering your decorators is crucial and will depend on your business logic. Take time to identify the proper order.

### Practical Example

Let’s say we have this endpoint intercepting an incoming call webhook:

```python
from twilio.twiml.voice_response import VoiceResponse

from app.modules.call import call
from app.commons.decorators import need_xml_output, log_headers, validate_twilio_request

@call.route('/incoming', methods=['POST'])
@validate_twilio_request
@log_headers
@need_xml_output()
def redirecting_call() -> VoiceResponse:
  # find whom to redirect the call to...
```

The decorators we want to look at are `log_headers` and `validate_twilio_request`.

They look like this:

```python
def log_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_app.logger.info(f"Request Headers: {dict(request.headers)}")
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Exception in decorator <log_headers>: {e}")

    return decorated_function

def validate_twilio_request(f):
    print("Decorator validate_twilio_request called")

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # List all the data that make a signature
            current_app.logger.debug("Inside decorated function")
            auth_token = current_app.config['TWILIO_AUTH_TOKEN']
            url = _get_url()
            post_data = request.form
            # The X-Twilio-Signature header
            twilio_signature = request.headers.get('X-Twilio-Signature', '')

            current_app.logger.debug(f"AUTH_TOKEN={auth_token}")
            current_app.logger.debug(f"url={url}")
            current_app.logger.debug(f"post_data={post_data}")
            current_app.logger.debug(f"twilio_signature={twilio_signature}")

            # Create a RequestValidator object
            validator = RequestValidator(auth_token)

            # Validate the request
            if not validator.validate(url, post_data, twilio_signature):
                # If the request is not valid, return a 403 Forbidden error
                abort(403)

            # If the request is valid, call the decorated function
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Exception in decorator <validate_twilio_request>: {e}")
            abort(500)

    return decorated_function
```

Now, a problem may arise with the `log_headers` decorator that fails to execute and trace headers. Why?

In Python, decorators are applied from bottom to top. In our use case, we’d have an equivalent to this:

```python
# ORDER OF EXECUTION
result = need_xml_output(log_headers(validate_twilio_request(call.route(args)))(redirecting_call))
```

The decorator `validate_twilio_request` fails if the signature in the `X-Twilio-Signature` header is incorrect and therefore the `log_headers` won’t execute at all because of the raised error:

```python
if not validator.validate(url, post_data, twilio_signature):
    abort(403)
```

To debug the decorator `validate_twilio_request` failure, it’s impractical not to know what the headers were.

The fix is simple: place `log_headers` first and the log file will contain all the headers received on the request.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Nataliya Vaitkevich](https://www.pexels.com/photo/blue-and-white-paint-brush-5642113/).
