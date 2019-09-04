# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import unittest

from html2md import convert


class ConvertTest(unittest.TestCase):
  def test_html_page(self):
    expected = 'HTML body!'
    actual = convert('''
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
    ''')
    self.assertEqual(expected, actual)

  def test_code_block(self):
    expected = '\n'.join([
        'Code block',
        '',
        '```',
        "print('hello')",
        "```",
    ])
    actual = convert("Code block<pre><code>print('hello')</pre></code>")
    self.assertEqual(expected, actual)

  def test_code_block_with_lang(self):
    expected = '\n'.join([
      'Code block',
      '',
      '```py',
      "print('hello')",
      "```",
    ])
    actual = convert(
        '''Code block<pre class="py"><code>print('hello')</pre></code>''')
    self.assertEqual(expected, actual)

  def test_hyperlinks(self):
    expected = 'Hyperlink [text](href)'
    actual = convert('Hyperlink <a href="href">text</a>')
    self.assertEqual(expected, actual)

  def test_hyperlinks_no_href(self):
    expected = 'Hyperlink [text](text)'
    actual = convert('Hyperlink <a>text</a>')
    self.assertEqual(expected, actual)

  def test_image(self):
    expected = 'Image ![alt](src)'
    actual = convert('Image <img alt="alt" src="src" />')
    self.assertEqual(expected, actual)

  def test_image_no_alt_src(self):
    expected = 'Image ![]()'
    actual = convert('Image <img />')
    self.assertEqual(expected, actual)

  def test_italics(self):
    expected = 'Italics *i* *em*'
    actual = convert('Italics <i>i</i> <em>em</em>')
    self.assertEqual(expected, actual)

  def test_bold(self):
    expected = 'Bold **b** **strong**'
    actual = convert('Bold <b>b</b> <strong>strong</strong>')
    self.assertEqual(expected, actual)

  def test_deleted(self):
    expected = 'Deleted ~~del~~'
    actual = convert('Deleted <del>del</del>')
    self.assertEqual(expected, actual)

  def test_deleted(self):
    expected = 'Deleted ~~del~~'
    actual = convert('Deleted <del>del</del>')
    self.assertEqual(expected, actual)

  def test_code(self):
    expected = 'Code `code`'
    actual = convert('Code <code>code</code>')
    self.assertEqual(expected, actual)

  def test_nested(self):
    expected = 'Nested `~~***nested***~~`'
    actual = convert('Nested <code><del><b><i>nested</i></b></del></code>')
    self.assertEqual(expected, actual)

  def test_inline_empty(self):
    expected = 'Inline empty'
    actual = convert('Inline empty <code></code><del></del><b></b><i></i>')
    self.assertEqual(expected, actual)

  def test_headers(self):
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
    actual = convert('\n'.join([
        '<h1>H1</h1>',
        '<h2>H2</h2>',
        '<h3>H3</h3>',
        '<h4>H4</h4>',
        '<h5>H5</h5>',
        '<h6>H6</h6>',
    ]))
    self.assertEqual(expected, actual)

  def test_horizontal_ruler(self):
    expected = '\n'.join([
        'Horizontal ruler',
        '',
        '---',
    ])
    actual = convert('Horizontal ruler<hr>')
    self.assertEqual(expected, actual)

  def test_paragraph(self):
    expected = '\n'.join([
        'Paragraph',
        '',
        'a',
        '',
        'b',
    ])
    actual = convert('Paragraph<p>a</p><p>b</p>')
    self.assertEqual(expected, actual)

  @unittest.skip("TODO: multiline paragraphs not implemented")
  def test_paragraph_multiline(self):
    expected = '\n'.join([
        'Paragraph',
        '',
        'multi',
        'line',
        'paragraph',
    ])
    actual = convert('''Paragraph<p>
        multi
        line

        paragraph
      </p>
    ''')
    self.assertEqual(expected, actual)

  def test_quotes(self):
    expected = '\n'.join([
        'Quotes',
        '',
        '> blockquote',
    ])
    actual = convert('Quotes<blockquote>blockquote</blockquote>')
    self.assertEqual(expected, actual)

  @unittest.skip("TODO: nested quotes not implemented")
  def test_quotes_nested(self):
    expected = '\n'.join([
        'Nested quotes',
        '',
        '> blockquote',
        '> > nested',
        '> > nested',
        '> > > nested double',
    ])
    actual = convert('''Nested quotes<blockquote>
      blockquote
      <blockquote>nested</blockquote>
      <blockquote>
        nested
        <blockquote>nested double</blockquote>
      </blockquote>
    </blockquote>''')
    self.assertEqual(expected, actual)

  def test_lists_ordered_empty(self):
    expected = 'Ordered list'
    actual = convert('Ordered list<ol></ol>')
    self.assertEqual(expected, actual)

  def test_lists_ordered(self):
    expected = '\n'.join([
        'Ordered list',
        '',
        '1. item 1',
        '1. item 2',
    ])
    actual = convert('''Ordered list<ol>
      <li>item 1</li>
      <li>item 2</li>
    </ol>''')
    self.assertEqual(expected, actual)

  def test_lists_unordered_empty(self):
    expected = 'Unordered list'
    actual = convert('Unordered list<ul></ul>')
    self.assertEqual(expected, actual)

  def test_lists_unordered(self):
    expected = '\n'.join([
        'Unordered list',
        '',
        '* item 1',
        '* item 2',
    ])
    actual = convert('''Unordered list<ul>
      <li>item 1</li>
      <li>item 2</li>
    </ul>''')
    self.assertEqual(expected, actual)

  def test_lists_nested(self):
    expected = '\n'.join([
        'Nested list',
        '',
        '1. item 1',
        '1. item 2',
        '   * item 2.1',
        '   * item 2.2',
        '     * item 2.2.1',
    ])
    actual = convert('''Nested list<ol>
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
    </ol>''')
    self.assertEqual(expected, actual)

  @unittest.skip("TODO: nested tags not implemented")
  def test_nested_tags_in_lists(self):
    expected = '\n'.join([
    ])
    actual = convert('''Nested tags in lists
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
    ''')
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
