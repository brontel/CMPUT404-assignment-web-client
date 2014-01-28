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

    def connect(self, host, port):

        # Making socket
        try:
            sockie = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
                     
        print 'Socket Created'        

        # obtaining remote ip from host
        try:
            remote_ip = socket.gethostbyname( host )
         
        except socket.gaierror:
            #could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        # Making the connection
        sockie.connect((remote_ip, port))

        print("Socket connected to " + host + " on ip " + remote_ip)

        msg = "GET / HTTP/1.1\r\n\r\n"

        # Sending message
        try :
            #Set the whole string
            sockie.sendall(msg)
        except socket.error:
            #Send failed
            print 'Send failed'
            sys.exit()
         
        print('Message send successfully')
         
        #Now receive data
        reply = sockie.recv(4096)
         
        #reply = self.recvall(sockie)

        sockie.close()
        return reply

    def get_code(self, data):
        for line in data:
            print line        
        print "-----------------------"
        first_line_parts = data[0].split()
        print data[0]
        
        return None

    def get_headers(self,data):

        

        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        
        # Get the first(?) part of the request and the host    
        (request, host) = self.parse_request(url, "GET")

        print(request)

        socket_return = self.connect(host, 80) 

        self.get_code(socket_return)

        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        
        # Get the first(?) part of the request and the host    
        (request, host) = self.parse_request(url, "POST")

        print(request)

        return HTTPRequest(code, body)

    def parse_request(self, url, req_type):
        """
        Takes a URL string and the type of request (GET, POST)
        and returns the first(?) part of the request and the host
        """
        url_comp = urlparse.urlsplit(url)
        print(url_comp)

        req = req_type + " {0} HTTP/1.1\r\n".format(url_comp[2]) + \
            "Host: {0}\r\n\r\n".format(url_comp[1]) 

        return (req, url_comp[1])

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    print("==========================================================")
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] ) # Switched order around
    else:
        print client.command( command, sys.argv[1] )    
