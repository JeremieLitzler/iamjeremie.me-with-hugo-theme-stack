---
title: "My cheatsheet for Python Programming After 4 Months "
description: "So far... I've a lot more to come as I compile all the awesome snippets and techniques I've learned recently."
image: images/2024-08-23-a-real-python.jpg
imageAlt: A real python
date: 2024-08-23
categories:
  - Web Development
tags:
  - Python
---

## Making a destructurable list of value

I love this one and it makes me think about the destructuring in JavaScript.

With `Tuple[type, type]` and a wrapping it in a list, you can use a `for...of` loop:

```python
times: list[Tuple[int, int]] = [
	(8,0),
	(12,0),
	(14,0),
	(18,0)
]

for hour, minutes of times
	print(f"It is {hour}:{minute}.")
```

## Replacing Substrings in Strings

To replace a substring in a string, you can use the `replace()` method. Here’s how you can replace `http` with `https` in Python:

```python
original_string = "This is an <http://example.com> link"
new_string = original_string.replace("http", "https", 1)
print(new_string)

```

This will output:

```
This is an <https://example.com> link

```

The third argument is the number of times you want to replace the target substring. Very handy!

## Sanitizing A String

Let say you have an endpoint in a REST API that must return an XML response.

Now the content of the XML response looks like the following:

```python
@twiml.route('/instructions/call/<string:caller>', methods=['POST', 'GET'])
@need_xml_output()
def get_call_instructions(caller: str):
    assert isinstance(current_app, OnCallApp)

    # Validate and sanitize the caller input
    caller = sanitize_phone_number(caller)

    response = VoiceResponse()
    message = f'The caller <say-as interpret-as="telephone">{caller}</say-as> '
                     f'has called you. '
                     f'A text was sent to you with his/her phone number to call the person back. '
                     f'Thanks.'
    response.say(message)
    return response.to_xml()
```

The code above represents an endpoint to return call instructions Twilio must speak to the person called.

As it stands right now, the `<say-as interpret-as="telephone">` and `</say-as>` will become encoded when Twilio receives it. That won’t give the expected result.

To avoid that, you need to tell Flask that `message` contains markup and that it shouldn’t be encoded.

However, the `caller` value is coming from outside, so we need to sanitize it.

The end result becomes:

```python
    message = Markup(f'The caller <say-as interpret-as="telephone">{escape(caller)}</say-as> '
                     f'has called you. '
                     f'A text was sent to with his/her phone number to call the person back. '
                     f'Thanks.'
```

`Markup` makes sure the `<say-as>` opening and closing tags aren’t encoded and the `escape` method sanitizes the `caller` value since it comes from outside. Never trust outside sources.

## `str` vs `LiteralString`

### The Differences

The main differences between `str` and `LiteralString` in Python are:

1. Purpose:
   - `str` is the built-in string type in Python.
   - `LiteralString` is a type hint introduced in Python 3.11 for static type checking.
2. Usage:
   - `str` is used for actual string objects in Python code.
   - `LiteralString` is used in type annotations to indicate that a string is known at compile time.
3. Runtime behavior:
   - `str` is a concrete type that exists at runtime.
   - `LiteralString` is erased at runtime and doesn’t affect program execution.
4. Type checking:
   - `LiteralString` is more restrictive than `str` in type checking.

Here’s an example to illustrate:

```python
from typing import LiteralString

def safe_query(query: LiteralString) -> None:
# This function only accepts string literals
    print(f"Executing query: {query}")

# This is fine
safe_query("SELECT * FROM users")

user_input = input("Enter query: ")
# This would raise a type error in static type checking
safe_query(user_input)
```

In this example, `safe_query` only accepts `LiteralString`, which helps prevent SQL injection by ensuring only literal strings are used for queries.

### How do you convert a LiteralString to str in python

To convert a LiteralString to a regular str in Python, you can simply use the built-in `str()` function. Here’s how you can do it:

```python
from typing import LiteralString

# Example LiteralString
literal_string: LiteralString = "Hello, world!"

# Convert to regular str
regular_string: str = str(literal_string)

print(type(literal_string))  # <class 'str'>
print(type(regular_string))  # <class 'str'>

```

## Encoding URL In Python

To encode a URL in Python, you can use the `urllib.parse.quote()` function. Here’s how you can do it:

```python
from urllib.parse import quote

url = "<http://localhost:5000/api/call/someone/+41123456789>"
encoded_url = quote(url, safe=':/')

print(encoded_url)

```

This will output:

```text
<http://localhost:5000/api/call/someone/%2B41123456789>

```

## Accessing Query String in Flask 3 POST Requests

To get the query string values from a POST request with the Content-Type `application/x-www-form-urlencoded` in Flask 3, you can use the `request.form` object. Here’s how you can do it:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/your-route', methods=['POST'])
def handle_post():
    # Access form data
    form_data = request.form

    # Get specific values
    value1 = form_data.get('key1')
    value2 = form_data.get('key2')

    # Or iterate through all form data
    for key, value in form_data.items():
        print(f"{key}: {value}")

    # Your logic here

    return "Data received"

if __name__ == '__main__':
    app.run(debug=True)

```

In this example:

1. We import `request` from Flask.
2. We define a route that accepts POST requests.
3. Inside the route handler, we use `request.form` to access the form data.
4. You can get specific values using `request.form.get('key')`. To avoid possible errors, you can use the default parameter in the second parameter of the `get` method: `request.form.get('key', None)`.
5. Alternatively, you can iterate through all form data using a loop.

Remember that `request.form` is a MultiDict, so if you expect multiple values for the same key, you can use `request.form.getlist('key')`.

## Switch…case

Python doesn’t have a built-in switch…case statement like some other programming languages, but there are a few ways to achieve similar functionality:

### Using dictionaries (most common approach)

```python
def switch_case(argument):
    switcher = {
        1: "One",
        2: "Two",
        3: "Three"
    }
    return switcher.get(argument, "Invalid number")

print(switch_case(2))  # Output: Two

```

### Using if-elif-else statements

```python
def switch_case(argument):
    if argument == 1:
        return "One"
    elif argument == 2:
        return "Two"
    elif argument == 3:
        return "Three"
    else:
        return "Invalid number"

print(switch_case(2))  # Output: Two

```

### Using Python 3.10+ match-case statement

That’s the closest to the `switch...case` you probably know.

```python
def switch_case(argument):
    match argument:
        case 1:
            return "One"
        case 2:
            return "Two"
        case 3:
            return "Three"
        case _:
            return "Invalid number"

print(switch_case(2))  # Output: Two

```

The dictionary method is often preferred for its simplicity and efficiency. The match-case statement is a newer feature and provides more advanced pattern matching capabilities.

## Subtracting Time From a Datetime

To remove a day from a `datetime` object in Python, you can use the `timedelta` class from the `datetime` module. Here’s how you can do it:

```python
from datetime import datetime, timedelta

# Create a datetime object
date = datetime(2024, 7, 24)  # Year, Month, Day

# For example, remove one day
new_date = date - timedelta(days=1)

print(f"Original date: {date}")
print(f"Date after removing one day: {new_date}")

```

This code will subtract one day from the given date. If you want to remove more than one day, you can change the `days` parameter in the `timedelta` function.

## Removing the First Item From a Python List

This one is pretty cool. You have 3 ways to do it and coming from years of .NET programming in C# or JavaScript, I love how Python enables you to perform the task.

### Using the `pop()` method:

This one feels like JavaScript:

```python
my_list = [1, 2, 3, 4, 5]
first_item = my_list.pop(0)
```

### Using list slicing

```python
my_list = [1, 2, 3, 4, 5]
my_list = my_list[1:]
```

### Using the `del` statement

```python
my_list = [1, 2, 3, 4, 5]
del my_list[0]
```

### Conclusion

Which method do you prefer?

## Initializing Datetime with Timezone

You can initialize a `datetime` object in Python with a string and a time zone. Here’s how you can do it using the `datetime` module and `pytz` library:

```python
from datetime import datetime
import pytz

# Define the date/time string and timezone
date_string = "2024-07-22 14:30:00"
timezone = pytz.timezone("Europe/Zurich")

# Parse the string and make it timezone-aware
dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
dt_with_tz = timezone.localize(dt)

print(dt_with_tz)

```

This code will create a timezone-aware `datetime` object for the specified date and time in the “Europe/Zurich” time zone.

A few things to note:

1. You need to install the `pytz` library if you haven’t already. You can do this with `pip install pytz`.
2. The `strptime` method parses the string according to the format you specify. Make sure your format string matches your input string.
3. The `localize` method of the time zone object is used to attach the time zone information to the `datetime` object.
4. If you want to convert this `datetime` to another time zone, you can use the `astimezone` method.

## Get the Index In A _For Loop_

To get the index in a _for loop_, you can use the `enumerate()` function in Python. Here’s a simple example:

```python
fruits = ['apple', 'banana', 'cherry']

for index, fruit in enumerate(fruits):
    print(f"Index: {index}, Fruit: {fruit}")
```

This code will output:

```text
Index: 0, Fruit: apple
Index: 1, Fruit: banana
Index: 2, Fruit: cherry
```

The `enumerate()` function returns pairs of (index, item) for each item in the iterable. You can then use these values directly in your loop.

If you want to start the index from a number other than 0, you can pass a start parameter to `enumerate()`. For example:

```python
for index, fruit in enumerate(fruits, start=1):
    print(f"Index: {index}, Fruit: {fruit}")
```

This will start the indexing from 1 instead of 0.

## Accessing Tuple Values by Index

To access values in a tuple from an index, you can use the square bracket notation, just like you would with a list. Here’s how you can access values from the tuples in a sample list:

```python
list_of_tuples: List[Tuple[int, int, int, int, int, int]] = [
    (2024, 8, 13, 18, 0, 0),
    (2024, 8, 13, 6, 0, 0),
    (2024, 8, 13, 1, 0, 0),
    (2024, 8, 13, 0, 1, 0),
    (2024, 8, 13, 23, 59, 0)
]

# Access the first tuple in the list
first_tuple = list_of_tuples[0]
print(first_tuple)  # Output: (2024, 8, 13, 18, 0, 0)

# Access a specific value within a tuple
year = first_tuple[0]
month = first_tuple[1]
day = first_tuple[2]
hour = first_tuple[3]
minute = first_tuple[4]
second = first_tuple[5]

print(f"Date: {year}-{month}-{day}, Time: {hour}:{minute}:{second}")
# Output: Date: 2024-8-13, Time: 18:0:0

# You can also access values directly from the list of tuples
third_tuple_hour = list_of_tuples[2][3]
print(third_tuple_hour)  # Output: 1

```

In this example, we first access a tuple from the list using its index, then access individual values within the tuple using their respective indices. Remember that tuple indices, like list indices, start at 0.

You can also use tuple unpacking to assign all values to variables at once:

```python
year, month, day, hour, minute, second = list_of_tuples[0]
```

This assigns each value in the first tuple to a separate variable in order.

## Conclusion

You know other tips and cool Python syntax to perform great things? Share them on X!

{{< blockcontainer jli-notice-tip "Follow me">}}

Thanks for reading this article. Make sure to [follow me on X](https://x.com/LitzlerJeremie), [subscribe to my Substack publication](https://iamjeremie.substack.com/) and bookmark my blog to read more in the future.

{{< /blockcontainer >}}

Credit: Photo by [Pixabay](https://www.pexels.com/photo/green-snake-45246/).
