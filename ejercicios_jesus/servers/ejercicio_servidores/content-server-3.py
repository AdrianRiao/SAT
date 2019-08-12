#!/usr/bin/env python3

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
    <p>Tell me something to remember</p>
    <form action="/" method="GET">
      <input name="content" type="text" />
    <input type="submit" value="Submit" />
    </form>
    <p>The last content I remember is: {last_content}.</p>
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

        last_content = ""
        if 'id' in cookies:
            id = cookies['id'].value
        else:
            id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
            cookie = http.cookies.SimpleCookie()
            cookie['id'] = id
            self.send_header("Set-Cookie", cookie.output(header='', sep=''))
            
        if id in text:
            last_content = text[id]

        if parsed_resource.query:
            qs = urllib.parse.parse_qs(parsed_resource.query)
            if 'content' in qs:
                content = qs['content'][0]
                last_content = content
                text[id] = content

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
