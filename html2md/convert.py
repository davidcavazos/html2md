#!/usr/bin/env python

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

import lxml
import os
import re
from pyquery import PyQuery

# TODO: support nested tags in lists to be correctly indented.

whitespaces_re = re.compile(r'\n[ \t\f\v]*\n')
multiple_newlines_re = re.compile(r'\n\n\n+')

trim_whitespaces_tags = 'ol|ul|li'
trim_whitespaces_open_re = re.compile(r'\s*<({})>\s*'.format(trim_whitespaces_tags))
trim_whitespaces_close_re = re.compile(r'\s*</({})>\s*'.format(trim_whitespaces_tags))

translate_headers = {
    'h1': '#',
    'h2': '##',
    'h3': '###',
    'h4': '####',
    'h5': '#####',
    'h6': '######',
}

translate_inline = {
    'i': '*',
    'em': '*',
    'b': '**',
    'strong': '**',
    'del': '~~',
    "code": '`',
}


def is_nested(e, valid_parent_tags=None):
  valid_parent_tags = set(valid_parent_tags or {}) | {'body'}
  parents = {parent.tag for parent in e.iterancestors()}
  return len(parents - valid_parent_tags) > 0


def convert(html):
  # Normalize nested html since Markdown is space-sensitive.
  html = trim_whitespaces_open_re.sub(r'<\1>', html)
  html = trim_whitespaces_close_re.sub(r'</\1>', html)

  doc = PyQuery(html)
  doc('head').remove()
  if not doc.find('body'):
    doc = PyQuery('<body>{}</body>'.format(doc.html()))
  doc = doc('body')

  # Code block: <pre> <code>
  # Note: code blocks *must* happen before inline <code>.
  for code in doc('pre code'):
    e = code.getparent()
    if is_nested(e):
      continue
    lang = e.attrib.get('class', '')
    text = '\n\n```{}\n{}\n```\n\n'.format(lang, code.text.strip('\n'))
    doc(e).replace_with(text)

  # Inline: <i> <em> <b> <strong> <del> <code>
  # Note: we iterate on reversed order so nested tags can be processed in the
  # correct order: <b><i>hello</i></b> will process the <b> tag after the <i>
  for e in reversed(doc(','.join(translate_inline.keys()))):
    if is_nested(e, translate_inline.keys()):
      continue
    if e.text:
      surround = translate_inline[e.tag]
      text = surround + e.text + surround
    else:
      text = ''
    doc(e).replace_with(text)

  # Hyperlink: <a>
  for e in doc('a'):
    if is_nested(e):
      continue
    text = (e.text or '').strip()
    href = e.attrib.get('href', '')
    if not text:
      text = href
    elif not href:
      href = text
    text = '[{}]({})'.format(text, href)
    doc(e).replace_with(text)

  # Image: <img>
  for e in doc('img'):
    if is_nested(e):
      continue
    alt = e.attrib.get('alt', '')
    src = e.attrib.get('src', '')
    if not alt:
      alt = os.path.splitext(os.path.basename(src))[0]
    elif not src:
      src = alt
    text = '![{}]({})'.format(alt, src)
    doc(e).replace_with(text)

  # Headers: <h1> <h2> <h3> <h4> <h5> <h6>
  for e in doc(','.join(translate_headers.keys())):
    if is_nested(e):
      continue
    text = '\n\n{} {}\n\n'.format(translate_headers[e.tag], e.text or '')
    doc(e).replace_with(text)

  # Horizontal ruler: <hr>
  for e in doc('hr'):
    if is_nested(e):
      continue
    text = '\n\n---\n\n'
    doc(e).replace_with(text)

  # Don't translate <p> <blockquote>, <ul>, <ol> or <li> due to nesting.
  md = doc.html()
  md = md.replace('&gt;', '>')
  md = multiple_newlines_re.sub('\n\n', md)
  return md.strip()
