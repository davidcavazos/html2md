import argparse
import fileinput

import html2md


def main(argv=None):

  parser = argparse.ArgumentParser()
  parser.add_argument('file', default='-', nargs='?', help='HTML file to convert to Markdown')
  args = parser.parse_args(argv)

  html = ''.join([line for line in fileinput.input(args.file)])
  print(html2md.convert(html))


if __name__ == '__main__':
  main()
