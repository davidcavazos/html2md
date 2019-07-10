# html2md

HTML to Markdown converter

## Installation

```sh
pip install -U html2md
```

## Usage

As a command line tool:

```sh
# To convert a file.
html2md examples/hello.html

# To convert from stdin.
cat examples/hello.html | html2md
```

From a Python script:

```py
import html2md

html = '''
<h1>Header</h1>
<b><i>Hello</i></b> from <code>html2md</code>
<pre class="py"><code>
print('Hello')
</code></pre>
'''

md = html2md.convert(html)
print(md)
```

## Contributing

### Clone the repository

First, fork the project.

```sh
# Clone your fork into your local machine.
# This will create the `origin` remote pointing to your fork.
git clone git@github.com:<your-username>/html2md.git

# Add an `upstream` remote pointing to the original repository.
git remote add upstream git@github.com:davidcavazos/html2md.git
```

### Modifying the code

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

### Running tests

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

### Creating a Pull Request

After all the tests pass, you'll have to create a "Pull Request" with your changes.
You can create a single commit with all the changes.

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
