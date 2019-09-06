# Contribution guide

## Clone the repository

First, fork the project.

```sh
# Clone your fork into your local machine.
# This will create the `origin` remote pointing to your fork.
git clone git@github.com:<your-username>/html2md.git
cd html2md

# Add an `upstream` remote pointing to the original repository.
git remote add upstream git@github.com:davidcavazos/html2md.git
```

## Setting up your environment

Make sure you have `virtualenv` installed.

```sh
pip install -U virtualenv
```

Create and activate a new `virtualenv`.

```sh
python -m virtualenv env
source env/bin/activate
```

> **Note**: Once you are all done, you can deactivate it by running `deactivate`.

Install the requirements.

```sh
pip install -U -r requirements.txt
```

## Modifying the code

First, make sure you're on the latest version.

```sh
git checkout master
git pull upstream master
```

Now, create a new branch for your changes.
Try to use a short and descriptive name for your changes.

```sh
# Create a new branch and change to it.
git checkout -b your-branch
```

You can now modify whatever you want.

## Running tests

Make sure you add tests for any new functionality or fix you do.
If it's in a new file, append the `*_test.py` prefix to the file.

```sh
# To run all the tests.
python setup.py test

# To run a specific test suite.
# python setup.py test -s <package>.<test_file>.<TestSuite>
python setup.py test -s html2md.convert_test.ConvertTest

# To run a specific test.
# python setup.py test -s <package>.<test_file>.<TestSuite>.<test_name>
python setup.py test -s html2md.convert_test.ConvertTest.test_code_block
```

## Creating a Pull Request

After all the tests pass, you'll have to create a "Pull Request" with your changes.
You can create a single commit with all the changes.

> **Note**: You can check your changes with `git status`.

```sh
# Create a commit and push it to your fork's branch.
git add .
git commit -m 'One line description of your changes'
git push origin your-branch
```

Then you can follow the link in your terminal, or navigate to [html2md](https://github.com/davidcavazos/html2md), to create a "Pull Request".

> If you need to add further modifications, you'll have to:
>
> ```sh
> git add .
> git commit -m 'One line description of further changes'
> git push origin your-branch
> ```
>
> Afterwards, it will reflect automatically on the Pull Request.

Once everything is okay, it can be merged.

## Publishing a new version

Make sure you have some more tools installed.

```sh
pip install -U twine
```

Change the version on `setup.py`.
Then, generate the distribution archives.

```sh
# Make sure there are no previous builds.
rm -rf dist/

# Build the distribution package.
python setup.py sdist bdist_wheel

# Check any problems with the README.
twine check dist/*
```

> **Note**: It is *highly recommended* to publish to `TestPyPI` before publishing to `PyPI`.
>
> ```sh
> # To upload to TestPyI.
> twine upload --repository-url https://test.pypi.org/legacy/ dist/*
>
> # To install from TestPyPI.
> pip install --index-url https://test.pypi.org/simple/ --no-deps html2md
> ```
>
> If everything is working correctly, go ahead and publish to `PyPI`.

To upload to `PyPI`.

```sh
twine upload dist/*
```
