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
# Session server 1.
# Serves a form, showing in the same page the last content of the form.
# This is a basic version, using GET for sending the contents of the form,
# and a cookie with the last content of the form.

import argparse
import http.server
import http.cookies
import socketserver
import urllib

PORT = 1234

PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Tell me something to remember</p>
    <form action="/" method="GET">
      <input name="content" type="text" />
    <input type="submit" value="Submit" />
    </form>
    <p>The last content I remember is: {last_content}.</p>
  </body>
</html>
"""

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

        last_content = ""
        if 'content' in cookies:
            last_content = cookies['content'].value

        if parsed_resource.query:
            qs = urllib.parse.parse_qs(parsed_resource.query)
            if 'content' in qs:
                content = qs['content'][0]
                last_content = content
                cookie = http.cookies.SimpleCookie()
                cookie['content'] = content
                self.send_header("Set-Cookie", cookie.output(header='', sep=''))

        self.end_headers()
        self.wfile.write(bytes(PAGE.format(last_content=last_content),
                               'utf-8'))

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()
