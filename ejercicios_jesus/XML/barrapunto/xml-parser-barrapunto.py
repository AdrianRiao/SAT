from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
import urllib.request

html_template = """<!DOCTYPE html>
<html lang="en" >
  <head>
    <meta charset="utf-8" />
    <title>HTML BARRAPUNTO</title>
  </head>
  <body>
    {content}
  </body>
</html>
"""

content = ""


class CounterHandler(ContentHandler):

    def __init__(self):
        self.inContent = 0
        self.theContent = ""
        self.title = ""
        self.in_item = False

    def startElement(self, name, attrs):
        if name == 'item':
            self.in_item = True
        elif name == 'title' and self.in_item:
            self.inContent = 1
        elif name == 'link' and self.in_item:
            self.inContent = 1

    def endElement(self, name):
        global content

        if name == 'item':
            self.in_item = False
        elif name == 'title' and self.in_item:
            self.title = self.theContent
        elif name == 'link' and self.in_item:
            content += ("<a href=" + self.theContent +
                        ">" + self.title + "</a><br/>")
        if self.inContent:
            self.inContent = 0
            self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


BarraPuntoParser = make_parser()
BarraPuntoHandler = CounterHandler()
BarraPuntoParser.setContentHandler(BarraPuntoHandler)

xmlFile = urllib.request.urlopen("http://barrapunto.com/index.rss")
BarraPuntoParser.parse(xmlFile)

print(html_template.format(content=content))
