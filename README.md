<!--intro-start-->
<center>

![Logo](docs/assets/logo.png)

<a href="https://pypi.python.org/pypi/mongoengine_dsl">
    <img src="https://img.shields.io/pypi/v/mongoengine_dsl.svg" alt="Release Status">
</a>

DSL to MongoEngine Q

</center>

## Features

* Build your mongoengine query from DSL syntax
* Convert your data at build time via transform hook

## Quickstart

Install

```bash
pip install mongoengine_dsl
```

Use

```python
from mongoengine import Document, StringField
from mongoengine_dsl import Query


class User(Document):
    fullname = StringField()


User(fullname="Tom").save()
User(fullname="Dick").save()
User(fullname="Harry").save()

assert User.objects(
    Query("fullname: Dick")
).first().fullname == "Dick"

assert User.objects(
    Query("fullname: dick", transform={
        "fullname": lambda x: x.title()
    })
).first().fullname == "Dick"
```
<!--intro-end-->
## More
Full Documentation: <https://stonemoe.github.io/mongoengine_dsl>
