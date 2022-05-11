# Contributing
Contributions are welcome and greatly appreciated!
This page will also guide you to contribute bugfix or new feature from scratch, check [Start to code](/contributing/#start-coding).

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
```bash
# 1.fork and clone
git clone git@github.com:your_name_here/mongoengine_dsl.git
cd mongoengine_dsl

# 2.tool installation
# Poetry
pipx install poetry     # use pipx
pip install poetry      # or use pip
brew install poetry     # or use homebrew
# Antlr4
brew install antlr      # use homebrew
apt-get install antlr4  # or use apt
# it's recommended to match version between antlr4 tool and runtime
# to avoid unexpected behavior

# 3.create and start your virtualenv
poetry install -E test -E doc -E dev
poetry shell

# 4.git pre-commit hook
pre-commit install

# 5.create your own branch
git checkout -b name-of-your-bugfix-or-feature

# 6.coding

# 7.test your changes
tox

# 8.add your name to `AUTHORS.md` :D

# 9.commit and push
git add -A
git commit -m "fix: "
# some files may be modified by pre-commit. If so, please add these files and commit again.
git push origin name-of-your-bugfix-or-feature

# 10.submit a pull request
```

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

## Release
For maintainers.

### release
```bash
git checkout master
git pull
tox  # final test
poetry version [major|minor|patch]  # bump
vim CHANGELOG.md
git add CHANGELOG.md pyproject.toml
git commit -m "Release: $(poetry version --short)"
git tag -a -m "Release: $(poetry version --short)" "v$(poetry version --short)"
git push --follow-tags
# done
```

### documentation
run doc workflow from master branch manually
