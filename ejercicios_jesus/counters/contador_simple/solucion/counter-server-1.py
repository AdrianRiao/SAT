#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Simple HTTP Counter
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# February 2019
#
# Important: Run with Python 3.6 or higher
#
# Counter version 1.

import argparse
import http.server
import http.cookies
import random
import string
import socketserver
import urllib

PORT = 1234

PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Countdown!</p>
    <p>Current count: {count}.</p>
  </body>
</html>
"""

PAGE_NOT_FOUND = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <p>Resource not found: {resource}.</p>
  </body>
</html>
"""

# Dictionary for texts for each id
count = 5

def parse_args ():
    parser = argparse.ArgumentParser(description="Simple HTTP Server")
    parser.add_argument('-p', '--port', type=int, default=PORT,
                        help="TCP port for the server")
    args = parser.parse_args()
    return args

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        global count
        resource = self.path

        if resource == '/':
            self.send_response(200)
            page = PAGE.format(count=count)
            count = (count-1) % 6
        else:
            self.send_response(404)
            page = PAGE_NOT_FOUND.format(resource=resource)

        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page, 'utf-8'))

def main():
    args = parse_args()
    with socketserver.TCPServer(("", args.port), Handler) as MyServer:
        print("serving at port", args.port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()
