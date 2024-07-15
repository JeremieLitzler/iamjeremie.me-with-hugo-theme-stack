---
title: "Build a Python REST API project"
description: "In this guide, I’ll provide you the steps to get started with Python and Flask to build a hello world REST API. This was my first experience."
image: images/2024-07-15-someone-holding-a-post-it-with-python-written-on-it.jpg
imageAlt: "Someone holding a post-it with Python written on it"
date: 2024-07-15
categories:
  - Web Development
tags:
  - Python
---

I didn’t have any experience using Python before. So I used Gemini AI to help me get started.

{{< blockcontainer jli-notice-warning "About using AI">}}

Though it was helpful, it’s good double-check the facts and ask for validation from a more senior developer.

{{< /blockcontainer >}}

## Prerequisites

You need to understand what is a REST API.

First, **REST, or Representational State Transfer is a** software architectural style for creating web services that are easy to develop and integrate with.

Then, a REST API **exposes resources** that represent data or functionality (e.g., users, products, orders).

It usually uses several **HTTP Methods** to define actions on the resources (GET, POST, PUT, DELETE for retrieving, creating, updating, and deleting data).

In 2024, the most common data format used, for exchanging data between clients and servers, is JSON, though you can still find XML in legacy web services or specific integration with third parties still expecting XML.

## Choosing a Web Framework

Flask provides all the tools to start with because it’s described as lightweight and flexible, good for smaller projects.

You could use Django as well, but we usually use it to build MVC Web Applications, with the frontend included.

Finally, you could use FastAPI if you need high performance, automatic data validation, modern design principles.

When making your choice, consider factors like project size, complexity, and your familiarity with each framework.

I’ve chosen Flask to start my Python journey.

## Setup your IDE

I used Visual Studio Code because it’s flexible and free.

I also recommend creating a Python-specific profile to make sure you don’t end up with an extension mess. I personally have 3 profiles for my daily activities:

- Writing: when I write, it’s done essentially in Markdown.
- Vue: when developing Vue applications.
- Python: when developing Python applications.

Once you created your Python profile, install:

- `advanced-new-file`: to use `CTRL+ALT+N` to create a new file quickly without going to the _Explore View_.
- `Python Extension Pack`: to install a bundle of recommended extension.
  - Uninstall `IntelliCode`, `Dlango` and `Jinja` though as you don’t need it.
- `Python Debugger`: to debug easily your Python apps.
- `REST Client`: to test your endpoints using a very simple `.http` or `.rest` file.
- `Todo Tree`: to keep track of the code sections that need work.
- `Black Formatter`: to format your code.

  - Enable it using `CTRL+SHIFT+P`
  - Type _Configure Language Specific Settings_ to filter and select _Python_.
  - In the opened tab, filter the settings with _format_,
  - Make sure:

    - to select the `defaultFormatter` as _Black Formatter_ for Python
    - to check _Format on save_ in the settings.
    - otherwise, copy and paste the following in your `settings.json` file:

      ```json
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.formatOnSave": true
        }
      ```

{{< blockcontainer jli-notice-note "About PyCharm">}}

This note was added 2 months after I wrote the original content of this article.

I have a new opportunity to code a Web API with Python again with a colleague and this time, he encouraged me to use PyCharm ([available as portable through Scoop.sh](https://scoop.sh/#/apps?q=pycharm)).

I find it’s much quicker to start developing. I still needed to configure the key maps to match Visual Studio Code (I don’t have time to relearn all the short cuts…) and understand a few things in the new IDE.

{{< /blockcontainer >}}

## Create a new repository

The first step to initialize a Flask project is to **create a new project.**

Let’s start with creating a new Git repository on GitHub or your preferred version control.

_Make sure to select `Python` for the `.gitignore` template._

Open Visual and clone your repository.

## Create a Virtual Environment

Then, before you code anything, you need to create a Virtual Environment.

A virtual environment helps isolate project dependencies and avoid conflicts with other Python installations or libraries on your system. It’s a good practice to use virtual environments for managing dependencies in Flask projects.

If you run the following command, it’ll output the system-wide environment and the Python version installed on your system:

```bash
which python
```

For me, since I use [Scoop.sh](http://Scoop.sh), it outputs:

```bash
/c/Users/jlitzler/scoop/apps/python/current/python
```

Here’s how to create one (choose the method that suits your operating system):

```bash
# Replace 'venv' with your desired virtual environment name
python3 -m venv venv
# Activate the virtual environment
source venv/Scripts/activate
```

Now, the python version is sourced from your project-specific environment:

```bash
which python
# Outputs /c/Git/<your-project-name>/venv/Scripts/python
```

## Install Flask

Run the command in your terminal:

```bash
pip install Flask
```

You’ll need to _freeze_ your dependencies using the _pip_ command and export the output to `requirements.txt`:

```bash
pip freeze > requirements.txt
```

When you clone a fresh copy of your repository, you will simply run the install command using the `requirements.txt` content to install the dependencies:

```bash
pip install -r requirements.txt
```

{{< blockcontainer jli-notice-warning "">}}

⚠️ Make sure to run the freeze command to save the new dependencies you install.

{{< /blockcontainer >}}

## Create a basic API

I used the following file structure:

- create a file `app.py`
- create a file `api.py`
- create a file `controllers/api-hello-world.py`

### In `app.py`

Because we often organize our API code into controllers, we will create the Flask application instance in a file that does nothing else. It will avoid multiple Flask instances and bugs.

```python
from flask import Flask
app = Flask(__name__)
```

### In `controllers/api_hello_world.py`

```python
from flask import request, jsonify
from app import app

import json

@app.route("/api/v1.0/hello/<string:gretting>", methods=["GET"])
def api_hello_say_something(greeting):
    return jsonify({"message": f"Hello {message}", "method": f"{request.method}"})

@app.route("/api/v1.0/hello", methods=["POST"])
def api_hello_say_something():
		data = data = request.get_json()
    return jsonify({"message": f"Hello {data.get('greeting')}", "method": f"{request.method}"})
```

### In `api.py`

```python
from app import app
# import and register the routes of the controller
from controllers.api_hello_world import *

if __name__ == '__main__':
    app.run(debug=True)
```

## Test your _hello world_ API

You don’t need a Postman: using the extension `REST Client`, you run a request for each endpoint of the API:

- create a file `request-api-hello-world.rest` and paste the following:

```rest
###
GET http://127.0.0.1:5000/api/v1.0/hello/Jeremie HTTP/1.1
content-type: application/json

###
POST http://127.0.0.1:5000/api/v1.0/hello HTTP/1.1
Content-Type: application/json

{
  "greeting": "Jeremie"
}
```

- open `api.py` and select `Start debugging` under the `Run` menu or press `F5`.
- run each request in the `request-api-hello-world.rest` by clicking _Send Request_ that appears below the `###`. You should get a `HTTP 200` with the expected JSON data.

I’ll continue the series soon with the implementation of a more complex REST API. It will show how to use an ORM-like library called _SQLAlchemy_ and Swagger to API documentation.

Stay tuned!

Credit: Photo by [Hitesh Choudhary](https://unsplash.com/@hiteshchoudhary?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/person-holding-sticky-note-D9Zow2REm8U?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash).
.
