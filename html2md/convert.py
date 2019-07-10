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

import re
from pyquery import PyQuery

# TODO: support nested tags in lists to be correctly indented.

whitespaces_re = re.compile(r'\n[ \t\f\v]*\n')
multiple_newlines_re = re.compile(r'\n{3,}')

trim_whitespaces_tags = 'ol|ul|li'
trim_whitespaces_open_re = re.compile(r'\s*<({})>\s*'.format(trim_whitespaces_tags))
trim_whitespaces_close_re = re.compile(r'\s*</({})>\s*'.format(trim_whitespaces_tags))

markdown_translate = {
    'h1': '#',
    'h2': '##',
    'h3': '###',
    'h4': '####',
    'h5': '#####',
    'h6': '######',
    'hr': '---',
    'p': '\n',
    'blockquote': '>',
}

markdown_translate_inline = {
    'i': '*',
    'em': '*',
    'b': '**',
    'strong': '**',
    'del': '~~',
    "code": '`',
}


def convert(html):
  # Normalize nested html since Markdown is space-sensitive.
  html = trim_whitespaces_open_re.sub(r'<\1>', html)
  html = trim_whitespaces_close_re.sub(r'</\1>', html)

  doc = PyQuery(html)
  doc('head').remove()
  if not doc.find('body'):
    doc = PyQuery('<body>{}</body>'.format(doc.html()))
  doc = doc('body')

  # pre code
  for e in doc('pre code'):
    parent = e.getparent()
    lang = parent.attrib.get('class', '')
    text = '\n```{}\n{}\n```\n'.format(lang, e.text.strip('\n'))
    doc(parent).replace_with(text)

  # a
  for e in doc('a'):
    text = '[{}]({})'.format(e.text, e.attrib.get('href', e.text))
    doc(e).replace_with(text)

  # img
  for e in doc('img'):
    text = '![{}]({})'.format(e.attrib.get('alt', ''), e.attrib.get('src', ''))
    doc(e).replace_with(text)

  # i,em,b,strong,del,code
  # Note: we iterate on reversed order so nested tags can be processed in the
  # correct order: <b><i>hello</i></b> will process the <b> tag after the <i>
  for e in reversed(doc(','.join(markdown_translate_inline.keys()))):
    if e.text:
      surround = markdown_translate_inline[e.tag]
      text = surround + e.text + surround
    else:
      text = ''
    doc(e).replace_with(text)

  # h1,h2,h3,h4,h5,h6,hr,p,blockquote
  for e in doc(','.join(markdown_translate.keys())):
    text = markdown_translate[e.tag]
    if e.tag != 'p':
      text += ' '
    text += e.text or ''
    text = '\n{}\n'.format(text)
    doc(e).replace_with(text)

  # ol,ul
  md_list_tag = lambda tag: '1. ' if tag == 'ol' else '* ' if tag == 'ul' else ''
  for e in reversed(doc('ol,ul')):
    indents = 0
    for parent in PyQuery(e).parents():
      indents += len(md_list_tag(parent.tag))

    items = []
    items_tag = md_list_tag(e.tag)
    for child in PyQuery(e).children():
      if child.tag == 'li':
        child_text = child.text or ''
        items.append(' '*indents + items_tag + child_text)

    text = '\n' + '\n'.join(items) + '\n'
    doc(e).replace_with(text)

  return multiple_newlines_re.sub('\n\n', doc.html()).strip()
