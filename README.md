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
