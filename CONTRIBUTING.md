# Contributing

Contributions are welcome and greatly appreciated!
This page will also guide you to contribute bugfix or new feature from scratch, check [Start to code](#start-coding).

## Contribute in many ways

### Report Bugs

Report bugs at https://github.com/StoneMoe/mongoengine_dsl/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

MongoEngine DSL could always use more documentation, whether as part of the
official MongoEngine DSL docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/StoneMoe/mongoengine_dsl/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Start coding

Ready to contribute some code?
Here's how to set up `mongoengine_dsl` for local development.

1. Fork the `mongoengine_dsl` repo on GitHub.
2. Clone your fork locally

```bash
git clone git@github.com:your_name_here/mongoengine_dsl.git
cd mongoengine_dsl
```

3. Ensure [poetry](https://python-poetry.org/docs/) is installed.

```bash
pipx install poetry  # use pipx
pip install poetry  # use pip
brew install poetry  # use macOS with Homebrew
```

4. Ensure antlr4 tool is installed:

```bash
# it's recommended to match version between antlr4 tool and runtime
# to avoid unexpected behavior 
brew install antlr  # use macOS with Homebrew
apt-get install antlr4  # use Linux with APT
```

5. Install dependencies and start your virtualenv:

```bash
poetry install -E test -E doc -E dev
poetry shell
```

6. Install pre-commit hook:

```bash
pre-commit install
```

7. Create a branch for local development:

```bash
git checkout -b name-of-your-bugfix-or-feature
```

   Now you can make your changes locally.

8. When you're done making changes, run tests:

```bash
antlr -o mongoengine_dsl/lexer -Dlanguage=Python3 mongoengine_dsl/lexer/MongoEngineDSL.g4
tox
```

9. Add your name and GitHub profile link to `AUTHORS.md` :D
10. Commit your changes and push your branch to GitHub:

```bash
git add .
git commit -m "Your detailed description of your changes."
# Some files may be modified by hooks. If so, please add these files and commit again.
git push origin name-of-your-bugfix-or-feature
```

11. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 3.6, 3.7, 3.8, 3.9 and for PyPy. Check
   https://github.com/StoneMoe/mongoengine_dsl/actions
   and make sure that the tests pass for all supported Python versions.

## Tips
To run a subset of tests.
```bash
pytest tests.test_mongoengine_dsl
```

## Deploying & Release

A reminder for the maintainers on how to deploy.

1. check out release branch, merge all changes from master/main to release

2. Update HISTORY.md

    Be noticed that github workflow will generate a changelog for you automatically.

3. Commit the changes:

    > ``` bash
    > git add HISTORY.md
    > git commit -m "Changelog for upcoming release 0.1.1."
    > ```

4. Update version number

    > ``` bash
    > poetry patch [major|minor|patch]
    > ```

5. Run the tests:

    > ``` bash
    > tox
    > ```

6. Push the commit to release branch:

    > ``` bash
    > git push
    > ```

7. Push the tags, creating the new release on both GitHub and PyPI:

    > ``` bash
    > git tag %tag_name%
    > git push --tags
    > ```

    tag_name has to be started with 'v'(lower case), to leverage github release workflow.

8. Check the PyPI listing page to make sure that the README, release
    notes, and roadmap display properly. If tox test passed, this should be ok, since
    we have already run twine check during tox test.

For full checklist: <https://zillionare.github.io/cookiecutter-pypackage/pypi_release_checklist/>
