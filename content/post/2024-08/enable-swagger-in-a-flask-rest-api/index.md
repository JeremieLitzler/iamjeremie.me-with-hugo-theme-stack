---
title: "Enable Swagger in a Flask REST API"
description: "Swagger provides a nice UI to interact with a REST API. Here’s how to do it."
image: images/2024-27-08-swagger-with-python.svg
imageAlt: Swagger with Python
date: 2024-08-27
categories:
  - Web Development
tags:
  - Python
---

## Why Swagger

Integrating Swagger with Flask can significantly enhance API development and documentation.

This powerful combination allows developers to create well-documented, interactive APIs that are easier to understand, test, and maintain.

The benefits of using Swagger:

- **Improved Developer Experience:** Swagger provides clear and concise API documentation, making it easier for developers to understand and interact with your API.
- **Reduced Errors:** By allowing developers to test API calls directly from the Swagger UI, it can help identify and fix potential integration issues early on.
- **Increased Accessibility:** Swagger makes your API more discoverable and user-friendly for a wider developer audience.

Yet, I’d prefer the REST Client extension on Visual Studio Code.

## Getting started

Here’s how you can integrate it with your Flask API:

### **1. Flask-RESTful Extensions:**

Several Flask extensions simplify Swagger integration. Popular options include:

- **Flask-RESTPlus:** This extension offers automatic Swagger UI generation alongside functionalities like request/response decorators and data marshaling (https://flask-restplus.readthedocs.io/en/stable/swagger.html).
- **Flask-RESTful-Swagger:** This extension focuses specifically on Swagger integration, providing functionalities like endpoint documentation and interactive UI generation (https://flask-restx.readthedocs.io/en/latest/swagger.html).

{{< blockcontainer jli-notice-warning "">}}

⚠️ Below, I will detail the “**Flask-RESTful-Swagger**” option, because [Flask-RESTPlus is dead](https://stackoverflow.com/a/61645532/3910066) apparently.

{{< /blockcontainer >}}

### **2. Manual Integration:**

While extensions offer convenience, you can also integrate Swagger manually. Here’s the general approach:

- **Define API specification:** use the OpenAPI Specification (OAS) format (a successor to Swagger) to define your API’s endpoints, data models, and functionalities. Tools like Swagger Editor (https://editor.swagger.io/) can aid this process.
- **Serve the specification:** Flask allows serving static files. You can configure your Flask app to serve the generated OAS file at a specific URL (e.g. `/swagger.json`).
- **Client-side Integration:** Frontend clients can utilize Swagger UI, a web-based interface that fetches and parses the OAS file, providing an interactive API documentation explorer. You can include Swagger UI’s static files within your Flask app and serve them at a designated URL (e.g. `/swagger`).

Below, I’ll detail the implementation with an extension.

## Integrating Swagger to my REST API

{{< blockcontainer jli-notice-tip "Recommendation">}}

Use PyCharm IDE to develop in Python. It’ll save you the hassle to setup Visual Studio Code and the extensions you need.

{{< /blockcontainer >}}

First, you need to install the extension:

```bash
# Install the extension
pip install flask-restx
# Freeze the dependencies
pip freeze > requirements.txt
```

Then, you need to declare the API. I personally use:

- an `app.py` for the Flask app,
- an `api.py` for the main API entry point,
- and an individual `api_business_1.py` to separate the various APIs I have.

Introducing Swagger prompted me to introduce `api_swagger.py` that I can reuse in `api_business_1.py` to declare the route.

The full example in the doc in great to get started.

## Declaring the API

First, we need to instantiate the API with the high-level information:

```python
from flask_restx import Api

from app import app as __BOOSTED_APP__

api = Api(
    __BOOSTED_APP__,
    version="2.0",
    title="Boosted API",
    contact_url="https://iamjeremie.me/page/contact-me/",
    description='Provides a RESTFul API to record your time like the Android App "Boosted" does. The code isn´t however crafted by the Boosted Android team',
    license="GPL3",
)
```

## Implementation in a Controller

Then, you’ll need to implement your controller.

First, define the namespace for the controller:

```python
ns = api.namespace("api/v2.0/projects", description="Project operations")
```

For each action in the controller, you organize them by routes.

Below the `/` route is the root route (full route based on the namespace is therefore `api/v2.0/projects/`).

Consequently, the `POST api/v2.0/projects/` (adding a project) and `GET api/v2.0/projects` (getting all projects) will go under a class `ProjectList`.

```python
@ns.route("/")
class ProjectList(Resource):
    @ns.doc("api_project_add")
    @ns.expect(ProjectRequestSwaggerModel)
    @ns.marshal_with(ProjectResponseSwaggerModel, code=201)
    @ns.response(422, "Payload is invalid. See details in response.")
    def post(self):
        """Create a new project"""
        response = ProjectService(repository).create(api.payload)
        return response

    @ns.doc("api_project_get_all")
    @ns.marshal_with(ProjectResponseSwaggerModel)
    def get(self):
        """List all the projects"""
        projects = ProjectService(repository).get_all()
        return projects

```

Then, we deal with the single resource endpoints under the `Project` class. The full route then is `api/v2.0/projects/<string:id>`.

It groups the `GET api/v2.0/projects/<string:id>`, `PUT api/v2.0/projects/<string:id>` and `DELETE api/v2.0/projects/<string:id>`.

```python
@ns.route("/<string:id>")
@ns.response(404, "Project not found")
@ns.param("id", "The project identifier")
class Project(Resource):

    @ns.doc("api_project_get_one")
    @ns.marshal_with(ProjectResponseSwaggerModel)
    def get(self, id):
        """Retrieve a single project"""
        response = ProjectService(repository).get_one(id)
        return response

    @ns.doc("api_project_update")
    @ns.expect(ProjectRequestSwaggerModel)
    @ns.marshal_with(ProjectResponseSwaggerModel)
    @ns.response(422, "Payload is invalid. See details in response.")
    def put(self, id):
        """Update a project"""
        response = ProjectService(repository).update_one(id, api.payload)
        return response

    """Delete a project"""

    @ns.doc("api_project_delete")
    @ns.response(204, "Project deleted")
    def delete(self, id):
        response = ProjectService(repository).delete_one(id)
        return response
```

If you need, you can add other routes like the one below for getting all records for a given project.

```python
@ns.route("/<string:id>/records")
@ns.response(404, "Project not found")
@ns.param("id", "The project identifier")
class ProjectRecords(Resource):
    @ns.doc("api_project_get_records")
    @ns.marshal_with(RecordResponseSwaggerModel)
    def get(self, id):
        """List all records of the project"""
        records = RecordService(repository).get_by_project(id)
        return records
```

As you may have noticed, each route declares:

- `@ns-route` decorator to define the route path.
- `@ns.response` decorator, if needed, to define the HTTP response codes that the API could raise.
- `@ns.param` decorator to detail the input parameters the route receives.
- `@ns.doc` decorator to provide a quick description of the action.
- `@ns.expect` decorator to validate the input payload.
- `@ns.marshal_with` decorator to validate the output.

## Handling error

I discontinued my [`get_response_json`](../../2024-07/build-a-python-rest-api-project/index.md) that I used before Swagger to create two methods.

The services would use the `raise_business_error` when the code finds a business error.

```python
def raise_business_error(
    id: int,
    success: bool,
    message: str = "null",
    httpCode=200,
    underlyingEx: Exception = None,
):
    """Standardize the response when not returning actual records

    Args:
        id (int): the record id
        success (bool): the result of the operation
        message (str, optional): the message to explicit the operation result. Defaults to "null".
        httpCode (int, optional): the http code to use. Defaults to 200.

    Returns:
        str: The JSON object
    """
    if httpCode - 200 < 99:
        return None

    underlyingExMessage = None
    # if underlyingEx is not None and underlyingEx.args is not None:
    #     underlyingExMessage = underlyingEx.args[0]

    abort(httpCode, message)
```

The usage could be:

```python
raise_business_error(data.id, False, "start date is required", 422)
```

Then, the `handle_ex`, as a generic catch all, including business error, normalized the API response. It was a challenge to code this one, but I’ve learned a few things about the native utilities in Python.

```python
def handle_ex(ex: any):
    underlyingExMessage = ""
    if ex.args is not None and len(ex.args) > 0:
        underlyingExMessage = ex.args[0]

    httpCode = 500
    if hasattr(ex, "code"):
        try:
            httpCode = int(ex.code)
        except TypeError:
            httpCode = 500
        except ValueError:
            httpCode = 500

    message = "Internal Error. See details."
    if hasattr(ex, "message"):
        message = ex.message

    inner_message = ""
    if hasattr(ex, "data"):
        inner_message = ex.data.get("message", None)
        message = "Business Error. See details."

    description = ""
    if hasattr(ex, "description"):
        description = ex.description

    abort(
        httpCode,
        message,
        details={
            "inner_message": f"{inner_message}",
            "description": f"{description}",
            "inner_exception_message": f"{underlyingExMessage}",
        },
    )
```

The usage in the services is simple:

```python
from utils.api_utils import handle_ex

def my_service_method(self):
    try:
        # Business logic...
    except Exception as ex:
        print(ex)
        handle_ex(ex)
    finally:
        print("finished calling service_record.create")
```

As I look at this, three months after the development, I think a decorator would be better. Then I’d have one single `try...expect` and the syntax would look like:

```python
from utils.api_utils import handle_ex

@handle_ex(ex, "my_service_method")
def my_service_method(self):
    # Business logic...
```

## Conclusion

There you have it!

Swagger provides a neat documentation and testing capabilities. Though I’d not use for testing large API, it comes in handy when you want to check an endpoint definition or to test an endpoint.

I hope you enjoyed this article.

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Python logo of the header image is from WorldVectorLogo. You can find the original images [here](https://worldvectorlogo.com/logo/python-4): I built the image with [Sketchpad](https://sketch.io/sketchpad/) of Sketch.io.
