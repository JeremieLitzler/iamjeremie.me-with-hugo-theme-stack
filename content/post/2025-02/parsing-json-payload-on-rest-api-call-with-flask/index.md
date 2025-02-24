---
title: "Parsing JSON Payload on REST API call with Flask"
description: "This is a basic need and it is relatively simple. But is it maintainable?"
image: 2024-07-15-someone-holding-a-post-it-with-python-written-on-it.jpg
imageAlt: "Someone holding a post-it with Python written on it"
date: 2025-02-24
categories:
  - Web Development
tags:
  - Python
  - Flask
---

Back in July 2024, I started to learn Python programming through a concrete project.

The goal was to build a REST API and the very common use case is to build CRUD functionality with JSON exchange.

How does a Python application using Flask handle requests with JSON payloads and how do you parse it?

That’s the goal of this article.

## Parsing Payload Request in Flask Applications

To read the payload of a POST request in Flask (version 3 applies in the example below), you can use the `request.get_json()` method. Here’s a basic example:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def handle_post():
    data = request.get_json()
    # Process the data here
    return {"message": "Data received", "data": data}

if __name__ == '__main__':
    app.run(debug=True)

```

The code does the following:

1. Import the necessary modules
2. Create a Flask application
3. Define a route that accepts POST requests
4. Use `request.get_json()` to parse the JSON payload
5. Return a response with the received data

A few important points:

- Ensure that the client sends the data with the correct `Content-Type` header (usually `application/json`).
- If the data isn’t in JSON format, you might need to use `request.data` or `request.form` depending on the content type.
- For form data, use `request.form` to access form fields.
- For raw data, use `request.data` to get the byte string.

## What Datatype `get_json()` Returns

The `request.get_json()` method in Flask returns a Python dictionary (e.g., key/value pairs) containing the parsed JSON data from the request body. Here are some key points about its behavior:

1. If the request contains valid JSON data, it returns the parsed Python object.
2. If you provide an empty request body, it returns `None` by default.
3. If you provide invalid JSON, it raises a `werkzeug.exceptions.BadRequest` exception.
4. It can handle nested structures, converting JSON objects to Python dictionaries and JSON arrays to Python lists.
5. The method has optional parameters:
   - `force`: If set to `True`, it will try to parse the data as JSON even if the mime-type isn’t `application/json`.
   - `silent`: If `True`, it will return `None` instead of raising an exception for invalid JSON.

Here’s a simple example to illustrate:

```python
@app.route('/example', methods=['POST'])
def example():
    data = request.get_json()
    if data is None:
        return "No JSON received", 400
    return f"Received: {data}", 200

```

In this example, if you send a POST request with the JSON body `{"name": "Alice", "age": 30}`, the `data` variable would contain the Python dictionary `{'name': 'Alice', 'age': 30}`.

## How do you parse it to a DTO class

There are several methods:

### With a library

To parse the JSON payload into a Data Transfer Object (DTO) class in Flask, you can use a library like Pydantic or Marshmallow. I’ll show you how to do this using Pydantic, which suits particularly this task due to its simplicity and integration with type hints.

Here’s a step-by-step example:

1. First, install Pydantic:

   ```bash
   pip install pydantic
   ```

2. Define your DTO class using Pydantic:

   ```python
   from pydantic import BaseModel

   class UserDTO(BaseModel):
       name: str
       age: int
       email: str | None = None  # Optional field

   ```

3. Use this DTO in your Flask route:

```python
from flask import Flask, request
from pydantic import ValidationError

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        user = UserDTO(**user_data)
        # Now you can use user.name, user.age, user.email
        return {"message": "User created", "user": user.model_dump()}, 201
    except ValidationError as e:
        return {"errors": e.errors()}, 400

if __name__ == '__main__':
    app.run(debug=True)

```

This code does the following:

1. Defines a `UserDTO` class that inherits from Pydantic’s `BaseModel`.
2. In the route handler, it gets the JSON data using `request.get_json()`.
3. It then creates a `UserDTO` instance by unpacking the JSON data into the constructor.
4. If the data is valid, it returns a success message along with the user data.
5. If the data is invalid (e.g., missing required fields or wrong types), it catches the `ValidationError` and returns the validation errors.

You can also add more complex validation or default values to your DTO:

```python
from pydantic import BaseModel, EmailStr, Field

class UserDTO(BaseModel):
    # The "..." is used to omit unwritten code
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr | None = None
```

This adds length validation to the name, range validation to the age, and uses `EmailStr` for email validation.

I can tell you this is attractive when you’ll see the next method…

### Without a Library

You can parse JSON data into a DTO class using Python’s built-in features. Here’s how you can do it:

1. First, define your DTO class:

   ```python
   class UserDTO:
       def __init__(self, name: str, age: int, email: str | None = None):
           self.name = name
           self.age = age
           self.email = email

       @classmethod
       def from_dict(cls, data: dict):
           return cls(
               name=data.get('name'),
               age=data.get('age'),
               email=data.get('email')
           )

       def to_dict(self):
           return {
               'name': self.name,
               'age': self.age,
               'email': self.email
           }

   ```

2. Now, use this DTO in your Flask route:

   ```python
   from flask import Flask, request, jsonify

   app = Flask(__name__)

   @app.route('/user', methods=['POST'])
   def create_user():
       user_data = request.get_json()

       if not user_data:
           return jsonify({"error": "No data provided"}), 400

       try:
           user = UserDTO.from_dict(user_data)

           # Perform basic validation
           if not user.name or not isinstance(user.name, str):
               raise ValueError("Invalid name")
           if not isinstance(user.age, int) or user.age < 0:
               raise ValueError("Invalid age")
           if user.email is not None and not isinstance(user.email, str):
               raise ValueError("Invalid email")

           # Save data...

           # Return the response
           return jsonify({"message": "User created", "user": user.to_dict()}), 201

       except ValueError as e:
           return jsonify({"error": str(e)}), 400

   if __name__ == '__main__':
       app.run(debug=True)
   ```

Here are the explanation, step by step, of the code above:

1. Defines a `UserDTO` class with a constructor and methods for creating an instance from a dictionary (`from_dict`) and converting an instance to a dictionary (`to_dict`).
2. In the route handler, it gets the JSON data using `request.get_json()`.
3. It creates a `UserDTO` instance using the `from_dict` class method.
4. It performs basic validation manually. You can add more complex validation as needed.
5. If the data is valid, it returns a success message along with the user data.
6. If the data is invalid, it catches the `ValueError` and returns an error message.

This method requires more manual work compared to using Pydantic, especially for validation. However, it gives you full control over the process and doesn’t require additional libraries.

## Conclusion

Keep in mind that this quick introduction doesn’t handle all edge cases, but this is how I got started with Python and REST API last year. For a production environment, you might want to add more robust error handling and validation.

Is it maintenable on large applications? Maybe not… I’ll talk about it as I progress with Python programming.

In the meantime, for more on Python, use the tag at the bottom of the page ⬇️

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

<!-- more -->
