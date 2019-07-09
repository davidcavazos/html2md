import unittest

from html2md import convert

# TODO: make unit tests!

class Html2MdTest(unittest.TestCase):
  def test_html_page(self):
    html = '''
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Title of the document</title>
      </head>

      <body>
      HTML body!
      </body>
      </html>
    '''
    expected = 'HTML body!'
    self.assertEqual(convert(html), expected)

  def test_code_block(self):
    html = "Code block<pre><code>print('hello')</pre></code>"
    expected = '\n'.join([
        'Code block',
        '',
        '```',
        "print('hello')",
        "```",
    ])
    self.assertEqual(convert(html), expected)

  def test_code_block_with_lang(self):
    html = '''Code block<pre class="py"><code>print('hello')</pre></code>'''
    expected = '\n'.join([
      'Code block',
      '',
      '```py',
      "print('hello')",
      "```",
    ])
    self.assertEqual(convert(html), expected)

  def test_hyperlinks(self):
    html = 'Hyperlink <a href="href">text</a>'
    expected = 'Hyperlink [text](href)'
    self.assertEqual(convert(html), expected)

  def test_hyperlinks_no_href(self):
    html = 'Hyperlink <a>text</a>'
    expected = 'Hyperlink [text](text)'
    self.assertEqual(convert(html), expected)

  def test_image(self):
    html = 'Image <img alt="alt" src="src" />'
    expected = 'Image ![alt](src)'
    self.assertEqual(convert(html), expected)

  def test_image_no_alt_src(self):
    html = 'Image <img />'
    expected = 'Image ![]()'
    self.assertEqual(convert(html), expected)

  def test_italics(self):
    html = 'Italics <i>i</i> <em>em</em>'
    expected = 'Italics *i* *em*'
    self.assertEqual(convert(html), expected)

  def test_bold(self):
    html = 'Bold <b>b</b> <strong>strong</strong>'
    expected = 'Bold **b** **strong**'
    self.assertEqual(convert(html), expected)

  def test_deleted(self):
    html = 'Deleted <del>del</del>'
    expected = 'Deleted ~~del~~'
    self.assertEqual(convert(html), expected)

  def test_deleted(self):
    html = 'Deleted <del>del</del>'
    expected = 'Deleted ~~del~~'
    self.assertEqual(convert(html), expected)

  def test_code(self):
    html = 'Code <code>code</code>'
    expected = 'Code `code`'
    self.assertEqual(convert(html), expected)

  def test_nested(self):
    html = 'Nested <code><del><b><i>nested</i></b></del></code>'
    expected = 'Nested `~~***nested***~~`'
    self.assertEqual(convert(html), expected)

  def test_inline_empty(self):
    html = 'Inline empty <code></code><del></del><b></b><i></i>'
    expected = 'Inline empty'
    self.assertEqual(convert(html), expected)

  def test_headers(self):
    html = '\n'.join([
        '<h1>H1</h1>',
        '<h2>H2</h2>',
        '<h3>H3</h3>',
        '<h4>H4</h4>',
        '<h5>H5</h5>',
        '<h6>H6</h6>',
    ])
    expected = '\n'.join([
        '# H1',
        '',
        '## H2',
        '',
        '### H3',
        '',
        '#### H4',
        '',
        '##### H5',
        '',
        '###### H6',
    ])
    self.assertEqual(convert(html), expected)

  def test_horizontal_ruler(self):
    html = 'Horizontal ruler<hr>'
    expected = '\n'.join([
        'Horizontal ruler',
        '',
        '---',
    ])
    self.assertEqual(convert(html), expected)

  def test_paragraph(self):
    html = 'Paragraph<p>a</p><p>b</p>'
    expected = '\n'.join([
        'Paragraph',
        '',
        'a',
        '',
        'b',
    ])
    self.assertEqual(convert(html), expected)

  @unittest.skip("TODO: multiline paragraphs not implemented")
  def test_paragraph_multiline(self):
    html = '''Paragraph<p>
        multi
        line

        paragraph
      </p>
    '''
    expected = '\n'.join([
        'Paragraph',
        '',
        'multi',
        'line',
        'paragraph',
    ])
    self.assertEqual(convert(html), expected)

  def test_quotes(self):
    html = 'Quotes<blockquote>blockquote</blockquote>'
    expected = '\n'.join([
        'Quotes',
        '',
        '> blockquote',
    ])
    self.assertEqual(convert(html), expected)

  @unittest.skip("TODO: nested quotes not implemented")
  def test_quotes_nested(self):
    html = '''Nested quotes<blockquote>
      blockquote
      <blockquote>nested</blockquote>
      <blockquote>
        nested
        <blockquote>nested double</blockquote>
      </blockquote>
    </blockquote>'''
    expected = '\n'.join([
        'Nested quotes',
        '',
        '> blockquote',
        '> > nested',
        '> > nested',
        '> > > nested double',
    ])
    self.assertEqual(convert(html), expected)

  def test_lists_ordered_empty(self):
    html = 'Ordered list<ol></ol>'
    expected = 'Ordered list'
    self.assertEqual(convert(html), expected)

  def test_lists_ordered(self):
    html = '''Ordered list<ol>
      <li>item 1</li>
      <li>item 2</li>
    </ol>'''
    expected = '\n'.join([
        'Ordered list',
        '',
        '1. item 1',
        '1. item 2',
    ])
    self.assertEqual(convert(html), expected)

  def test_lists_unordered_empty(self):
    html = 'Unordered list<ul></ul>'
    expected = 'Unordered list'
    self.assertEqual(convert(html), expected)

  def test_lists_unordered(self):
    html = '''Unordered list<ul>
      <li>item 1</li>
      <li>item 2</li>
    </ul>'''
    expected = '\n'.join([
        'Unordered list',
        '',
        '* item 1',
        '* item 2',
    ])
    self.assertEqual(convert(html), expected)

  def test_lists_nested(self):
    html = '''Nested list<ol>
      <li>item 1</li>
      <li>item 2
        <ul>
          <li>item 2.1</li>
          <li>item 2.2
            <ul>
              <li>item 2.2.1</li>
            </ul>
          </li>
        </ul>
      </li>
    </ol>'''
    expected = '\n'.join([
        'Nested list',
        '',
        '1. item 1',
        '1. item 2',
        '   * item 2.1',
        '   * item 2.2',
        '     * item 2.2.1',
    ])
    self.assertEqual(convert(html), expected)

  @unittest.skip("TODO: nested tags not implemented")
  def test_nested_tags_in_lists(self):
    html = '''Nested tags in lists
      <ul>
        <li>item
          <pre><code>b</code></pre>
          <a href="href">text</a>
          <img alt="alt" src="src" />
          <h1>H1</h1>
          <p>
            <i>i</i> <em>em</em> <b>b</b> <strong>strong</strong>
            <del>del</del> <code>code</code>
          </p>
          <blockquote>
            blockquote
            <blockquote>nested</blockquote>
          </blockquote>
          <ol>
            <li>ordered list item</li>
            <li>
              <p>
                <i>i</i> <em>em</em> <b>b</b> <strong>strong</strong>
                <del>del</del> <code>code</code>
              </p>
            </li>
          </ol>
          <ul>
            <li>unordered list item</li>
            <li>
              <p>
                <i>i</i> <em>em</em> <b>b</b> <strong>strong</strong>
                <del>del</del> <code>code</code>
              </p>
            </li>
          </ul>
        </li>
      </ul>
    '''
    expected = '\n'.join([
    ])
    self.assertEqual(convert(html), expected)

if __name__ == '__main__':
  unittest.main()
