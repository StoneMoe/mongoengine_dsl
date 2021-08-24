![Logo](docs/assets/logo.png)

<div style="text-align: center;">
<a href="https://pypi.python.org/pypi/mongoengine_dsl">
    <img src="https://img.shields.io/pypi/v/mongoengine_dsl.svg" alt="Release Status">
</a>

<a href="https://github.com/StoneMoe/mongoengine_dsl/actions">
    <img src="https://github.com/StoneMoe/mongoengine_dsl/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<a href="https://mongoengine-dsl.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/mongoengine-dsl/badge/?version=latest" alt="Documentation Status">
</a>
</div>

DSL to MongoEngine Q

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

More: <https://stonemoe.github.io/mongoengine_dsl>
