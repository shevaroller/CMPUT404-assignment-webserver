#  coding: utf-8 
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Modifications copyright 2016 Oleksii Shevchenko (shevaroller.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        header = self.data.split("\n")
        request = header[0].split(" ")
        if request[0] == "GET":
             url = request[1]
             self.getUrl(url)
        else:
             print "Error\nGET is expected instead of " + request[0]
             self.getUrl("404")

    def getUrl(self, url):
        print "Get this url: " + url

        # construct path to requested file
        path = "www"
        path += url
        if os.path.isdir(path):
            if url[-1] == "/":
                path += "index.html"
            else:
                path += "/index.html"

        print "Trying to serve " + path
        try:
            f = open(path, 'r')
            absolutePath = os.path.abspath(f.name)
            # security check
            print "file path = " + absolutePath
            baseDirectory = os.path.dirname(os.path.abspath(__file__))
            servePath = baseDirectory + "/www/"
            if not absolutePath.startswith(servePath):
                raise FileNotFoundError("You don't have permissions to access file " + f.name)
            data = f.read()
            # consulted with http://www.tutorialspoint.com/http/http_responses.htm
            header = "HTTP/1.1 200 OK\n"
            mime = path.split(".")[-1]
            print "Respond with 200 OK\n\n"
        except:
            header = "HTTP/1.1 404 Not Found\n"
            data = "<h1>404 Not Found</h1>"
            mime = "html"
            print "Respond with 404 Not Found\n\n"
        header += "Content-Length: " + str(len(data)) + "\n"
        header += "Content-Type: text/" + mime + "\n"
        header += "Connection: Closed\r\n\r\n"
        self.sendResponse(header, data)


    def sendResponse(self, header, data):
            self.request.sendall(header + "\n" + data)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
