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
  # Helper testing methods.
  def check_tag(self, html, markdown):
    expected = 'Start{}End'.format(markdown)
    html = 'Start{}End'.format(html)
    actual = convert(html)
    self.assertEqual(expected, actual, '\n\n>> Tag: ' + html)

  def check_paragraph_tag(self, html, markdown):
    expected = 'Start\n\n{}\n\nEnd'.format(markdown).replace('\n\n\n\n', '\n\n')
    html = '<p>Start</p><p>{}</p><p>End</p>'.format(html)
    actual = convert(html)
    self.assertEqual(expected, actual, '\n\n>> Paragraph tag: ' + html)

  def check_nested_tag(self, html):
    expected = 'Start\n\n<table><tr><td>{}</td></tr></table>End'.format(html)
    html = 'Start<table><tr><td>{}</td></tr></table>End'.format(html)
    actual = convert(html)
    self.assertEqual(expected, actual, '\n\n>> Nested tag: ' + html)

  def check(self, html, markdown):
    self.maxDiff = None
    self.check_tag(html, markdown)
    self.check_paragraph_tag(html, markdown)
    self.check_nested_tag(html)

  # HTML documents: <html>
  def test_html_document(self):
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

  # Italics: <i> <em>
  def test_italics_i(self):
    html = '<i>i</i>'
    markdown = '*i*'
    self.check(html, markdown)

  def test_italics_em(self):
    html = '<em>em</em>'
    markdown = '*em*'
    self.check(html, markdown)

  # Bold: <b> <strong>
  def test_bold_b(self):
    html = '<b>b</b>'
    markdown = '**b**'
    self.check(html, markdown)

  def test_bold_strong(self):
    html = '<strong>strong</strong>'
    markdown = '**strong**'
    self.check(html, markdown)

  # Deleted: <del>
  def test_del(self):
    html = '<del>del</del>'
    markdown = '~~del~~'
    self.check(html, markdown)

  # Code: <code>
  def test_code(self):
    html = '<code>code</code>'
    markdown = '`code`'
    self.check(html, markdown)

  # Inline nested: <code> <del> <b> <i>
  def test_inline_nested(self):
    html = '<code><del><b><i>nested</i></b></del></code>'
    markdown = '`~~***nested***~~`'
    self.check(html, markdown)

  # Inline empty: <code> <del> <b> <i>
  def test_inline_empty(self):
    html = '<code/><del/><b/><i/>'
    markdown = ''
    self.check(html, markdown)

  # Code block: <pre><code>
  def test_code_block(self):
    html = "<pre><code>print('hello')</code></pre>"
    markdown = "\n\n```\nprint('hello')\n```\n\n"
    self.check(html, markdown)

  def test_code_block_with_lang(self):
    html = '''<pre class="py"><code>print('hello')</code></pre>'''
    markdown = "\n\n```py\nprint('hello')\n```\n\n"
    self.check(html, markdown)

  # Hyperlink: <a>
  def test_hyperlink(self):
    html = '<a href="href">text</a>'
    markdown = '[text](href)'
    self.check(html, markdown)

  def test_hyperlink_no_href(self):
    html = '<a>text</a>'
    markdown = '[text](text)'
    self.check(html, markdown)

  def test_hyperlink_no_text(self):
    html = '<a href="href"/>'
    markdown = '[href](href)'
    self.check(html, markdown)

  def test_hyperlink_no_href_text(self):
    html = '<a/>'
    markdown = '[]()'
    self.check(html, markdown)

  # Image: <img>
  def test_image(self):
    html = '<img alt="alt" src="src"/>'
    markdown = '![alt](src)'
    self.check(html, markdown)

  def test_image_no_alt(self):
    html = '<img src="domain.com/path/to/image.png"/>'
    markdown = '![image](domain.com/path/to/image.png)'
    self.check(html, markdown)

  def test_image_no_src(self):
    html = '<img alt="alt"/>'
    markdown = '![alt](alt)'
    self.check(html, markdown)

  def test_image_no_alt_src(self):
    html = '<img/>'
    markdown = '![]()'
    self.check(html, markdown)

  # Header: <h1> <h2> <h3> <h4> <h5> <h6>
  def test_headers(self):
    for i in [1, 2, 3, 4, 5, 6]:
      html = '<h{}>h{}</h{}>'.format(i, i, i)
      markdown = '\n\n{} h{}\n\n'.format('#'*i, i)
      self.check(html, markdown)

  # Horizontal ruler: <hr>
  def test_horizontal_ruler(self):
    html = '<hr/>'
    markdown = '\n\n---\n\n'
    self.check(html, markdown)

if __name__ == '__main__':
  unittest.main()
