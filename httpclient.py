#!/usr/bin/env python
# Copyright 2013 Abram Hindle, Bronte Lee, Stephanie Gil
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
#from urllib.parse import urlparse
import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port=80):
        """
        Makes a socket connection and returns it
        """
        # Making socket
        try:
            sockie = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
                     
        # obtaining remote ip from host
        try:
            remote_ip = socket.gethostbyname( host )
         
        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        # Making the connection
        sockie.connect((remote_ip, port))

        return sockie

    def send_message(self, sockie, req):
        """
        Sends the request through the given socket and receive the response
        """
        # Sending message
        try:
            #Set the whole string
            sockie.sendall(req)
        except socket.error:
            #Send failed
            print 'Send failed'
            sys.exit()
         
        print('Message send successfully')
         
        reply = self.recvall(sockie)
        
        print "--------------------reply--------------------"
        print reply

        sockie.close()
        return reply

    def get_code(self, data):       
        first_line = data.split('\n')[0]
        print "---------------------CODE--------------------"
        print first_line
        code = first_line.split()[1]
        return int(code)

    def get_headers(self,data):
        headers_string = data.split('\r\n\r\n', 1)[0]
        headers = headers_string.split('\r\n')
        return headers

    def get_body(self, data):
        body = data.split('\r\n\r\n', 1)[1]
        return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(4096)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        """
        Sends a GET request based on the url given
        """
        code = 500
        body = ""
        
        # Get the first(?) part of the request and the host    
        (request, host, port) = self.parse_request(url, "GET")

        socket = self.connect(host, port) 

        socket_return = self.send_message(socket, request)

        code = self.get_code(socket_return)
        body = self.get_body(socket_return)

        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        
        # Get the first(?) part of the request and the host    
        (request, host, port) = self.parse_request(url, "POST", args)

        print(request)
        socket = self.connect(host, port) 

        socket_return = self.send_message(socket, request)
        code = self.get_code(socket_return)
        body = self.get_body(socket_return)
       
        return HTTPRequest(code, body)

    def parse_request(self, url, req_type, args=None):
        """
        Takes a URL string and the type of request (GET, POST)
        and returns the first(?) part of the request and the host
        path: index 2
        host+port: index 1
        """
        url_comp = urlparse.urlsplit(url)
        path = url_comp[2][1:]
    
        print "-------------path--------------"
        print path 
        print url_comp

        if ':' in url_comp[1]:
              host, port = url_comp[1].split(':')
        else:
            host = url_comp[1]
            port = 80

        req = req_type + " /" + "{0} HTTP/1.0\r\n".format(path) + \
            "Host: {0}\r\n".format(host) 
        print req
        arg_string = ""
        if args != None:
             #arg_string += self.parse_arguments(args)
	    arg_string = urllib.urlencode(args)
        #if req == "POST":
            req +=  "Content-Length: " + str(len(arg_string)) + "\r\n" + \
            "Content-Type: application/x-www-form-urlencoded\r\n" 
        print len(arg_string)
       
        req += "\r\n" + arg_string 

	print "-----------------REQUEST-------------------------------------------"
	print req
        return (req, host, int(port))

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] ) # Switched order around
    else:
        print client.command( command, sys.argv[1] )    
