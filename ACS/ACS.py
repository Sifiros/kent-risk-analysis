#!/usr/local/bin/python3

import json
from http.server import HTTPServer
from AcsHttpRequestHandler import AcsHttpRequestHandler

class AccessContronServer():
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port
        self.m_httpd = HTTPServer((self.m_ip, self.m_port), AcsHttpRequestHandler)
        self.start_server()

    def start_server(self):
        print('Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.m_httpd.serve_forever()

if __name__ == "__main__":
    AccessContronServer('localhost', 8484)