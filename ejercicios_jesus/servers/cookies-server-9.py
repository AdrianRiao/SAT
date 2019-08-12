#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Simple HTTP Server
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# January 2019
#
# Important: Run with Python 3.6 or higher
#
# Server sending a cookie when the content of the text form
# is received, and showing in the screen the text in the
# cookie (if any).

import argparse
import http.server
import http.cookies
import random
import socketserver
import string
import urllib

PORT = 1234

PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Hello!</p>
    <form action="/" method="GET">
      Say something: <input name="content" type="text" />
    <input type="submit" value="Submit" />
    <p>Content in form: {content}.</p>
    <p>Last content in form (from content cookie): {last_from_content}.</p>
    <p>Last content in form (from id cookie): {last_from_id}.</p>
    <p>Content cookie: {content_cookie}.</p>
    <p>Id cookie: {id_cookie}.</p>
    </form>
  </body>
</html>
"""

# Dictionary for texts for each id
text = {}

def parse_args ():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('-p', '--port', type=int, default=PORT,
                        help="TCP port for the server")
    args = parser.parse_args()
    return args

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        print("Received: GET " + self.path)
        parsed_resource = urllib.parse.urlparse(self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/html")

        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))

        content_cookie = ""
        if 'content' in cookies:
            content_cookie = cookies['content'].value
            last_from_content = content_cookie
        else:
            content_cookie = 'None'
            last_from_content = 'None'

        if 'id' in cookies:
            id_cookie = cookies['id'].value
            id = id_cookie
        else:
            id_cookie = 'None'
            id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
            cookie = http.cookies.SimpleCookie()
            cookie['id'] = id
            self.send_header("Set-Cookie", cookie.output(header='', sep=''))

        if id in text:
            last_from_id = text[id]
        else:
            last_from_id = 'None'

        content = 'None'
        if parsed_resource.query:
            qs = urllib.parse.parse_qs(parsed_resource.query)
            if 'content' in qs:
                content = qs['content'][0]
                cookie = http.cookies.SimpleCookie()
                cookie['content'] = content
                self.send_header("Set-Cookie", cookie.output(header='', sep=''))
                text[id] = content

        self.end_headers()
        self.wfile.write(bytes(PAGE.format(content=content,
                                           last_from_content=last_from_content,
                                           last_from_id=last_from_id,
                                           content_cookie=content_cookie,
                                           id_cookie=id_cookie),
                               'utf-8'))

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()
