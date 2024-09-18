---
title: "Caveat With Model Modules and SQLAlchemy 2+"
description: "I ran into a little issue while trying the split my database models into separate files on a REST API using Python and SQLAlchemy. Let’s review the problem and its solution."
image: images/2024-07-30-a-green-bug.jpg
imageAlt: "A green bug"
date: 2024-07-30
categories:
  - Web Development
tags:
  - Python
---

## The Context

A few months ago, I was working on a simple REST API to acquire the skills of Python backend development using Flask 3, and SQL Alchemy 2.

The app I was building was a little timesheet tool where I could record the time spent on projects and tasks.

I had 3 models (excluding the base model):

- the Project model
- the Task model
- the Time Record model

While I started to code the API, I defined the models into a single file `models.py` that I imported on a file `main.py` where I had this:

```python
import os
from sqlalchemy import create_engine
from dao.models import Model

def init_engine(base_dir: str):
    """Load the engine

    Args:
        base_dir (str): The base directory where the database is stored

    Returns:
        object: The engine
    """
    db_file_name = f"sqlite:///{base_dir}{os.sep}..{os.sep}db{os.sep}sqlalchemy.db"
    engine = create_engine(db_file_name, echo=True)
    return engine

def reset_database(base_dir: str):
    """Reset the database by dropping all tables

    Args:
        base_dir (str): The base directory where the database is stored
    """
    Model.metadata.drop_all(init_engine(base_dir))

def init_database(base_dir: str):
    """Initialize the database by creating the tables that needs to be created.
    It doesn't try to recreate what already exists.

    See https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all

    Args:
        base_dir (str): _description_
    """
    Model.metadata.create_all(init_engine(base_dir))

```

It defines 3 methods. In the `app.py`, I defined a simple logic to drop everything only in development when starting the server:

```python
import os

from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

from constants.environment_vars import EnvironmentVariable

# from dal.main import init_engine
from dal.main import init_database, reset_database, init_engine

load_dotenv()

env = os.getenv(EnvironmentVariable.ENVIRONMENT)

# Create the Flask application instance
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the database engine (dependency injection)
app.config[EnvironmentVariable.DATABASE_ENGINE] = init_engine(BASE_DIR)
# Create a session maker using the injected engine
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=app.config[EnvironmentVariable.DATABASE_ENGINE],
    )
)
app.config[EnvironmentVariable.SESSION_LOCAL] = SessionLocal

if env == "dev":
    print("Environment is dev")
    # TODO: drop the database
    print("drop database...")
    reset_database(BASE_DIR)
    print("dropped database!")
    # TODO: and recreate it
    print("create database...")
    init_database(BASE_DIR)
    print("created database!")

if env == "production":
    print("Environment is production")
    # TODO: create
    print("create database...")
    init_database(BASE_DIR)
    print("created database!")
```

## The Problem

Once I completed the Project endpoints, I moved on to the Task endpoints and I wanted to split in individual files the models.

```plaintext
|__ dao/models
    |__ base_model.py
    |__ project_model.py
    |__ task_model.py
    |__ time_record_model.py
```

While it didn’t prevent from adding projects after updating the imports, it broke the database reset…

When I ran the request to create a project right after restarting the server, I notice the error about the project’s name unique constraint.

Then I notice that after the last server restart, the terminal didn’t log the usual SQL code ran by SQLAlchemy on initialization of the database after the reset.

## Why

In Python, a file corresponds to a module. Thus, the import in the `main.py` code above became :

```python
from dao.models.base_model import Model
```

Except that only `Model` is loaded, and even when adding imports for the `Project`, `Task` and `Timerecord` entities, `Model.metadata.drop_all()` would do nothing...

Therefore `Model.metadata.drop_all()` does nothing…

## How to Use Split Files and Retain the Functionality

Simply don’t. I think this is a habit of developing n .NET for 15 years. But in Python programming, and if you use the ORM SQLAlchemy, keep the code-first database schema in a single file called `database.py` or `entities.py` or whatever you wish.

Also, one other limitation to split files is that using the ORM feature that allows retrieving related items in a relationship between two models will cause you a bit of trouble.

For more on Python, [browse to the tag](../../../tags/python).

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Pixabay](https://www.pexels.com/photo/green-black-and-brown-insect-40875/).
.
