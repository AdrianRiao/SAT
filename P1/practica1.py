#!/usr/bin/python3

import webapp
import socket

# Dictionary that contains complete urls and their short urls
UrlsDict = {}

# Dictionary that contains short urls and their complete urls
UrlsDictInv = {}

cont = 0

formulario = '''
 <form action="" method="POST">
  URL to shorten:<br>
  <input type="text" name="url"><br><br>
  <input type="submit" value="Enviar">
</form>
'''


def cmplt_url(url):
    if url[0:13] == "http%3A%2F%2F":
        return "http://" + url[13:]
    elif url[0:14] == "https%3A%2F%2F":
        return "https://" + url[14:]
    else:
        return "http://" + url


def dict_to_str(dictionary):
    string = ""
    for url in dictionary:
        string = string + url + " => " + dictionary[url] + "<br>"
    return string


class Shortener(webapp.webApp):

    def parse(self, request):
        try:
            method, resource, _ = request.split(' ', 2)
            body = request.split('\r\n\r\n', 1)[1]
        except IndexError:
            body = ""
        except ValueError:
            method = ""
            resource = ""
            body = ""
        return method, resource, body

    def process(self, parsedRequest):

        global cont

        method, resource, body = parsedRequest

        if method == "GET" and resource == "/":
            return ("200 OK", "<html><body>" + formulario +
                    "<br>Saved URLS:<br>" + dict_to_str(UrlsDict)
                    + "</body></html>")

        if method == "POST":
            try:
                url = body.split("=", 1)[1]
            except IndexError:
                return ("400 Bad Request",
                        "<html><body>QS not supported</body></html>")

            url = cmplt_url(url)

            if url not in UrlsDict:
                short_url = "http://localhost:1234/" + str(cont)
                UrlsDict[url] = short_url
                UrlsDictInv[short_url] = url
                cont = cont + 1
            else:
                short_url = UrlsDict[url]

            return ("200 OK", "<html><body><a href=" + url +
                    ">" + url + "</a> corresponds with <a href=" +
                    short_url + ">" + short_url +
                    "</a></body></html>")

        try:
            short_url = "http://localhost:1234" + resource
            url_to_direct = UrlsDictInv[short_url]
            return ("301 Moved Permanently\r\nLocation: " +
                    url_to_direct, "")
        except KeyError:
            return ("404 Not Found",
                    "<html><body>Resource not found</body></html>")


if __name__ == "__main__":
    ShortenerWebApp = Shortener("localhost", 1234)
