#!/usr/local/bin/python3

import json
import enum
from http.server import HTTPServer
from AcsHttpRequestHandler import AcsHttpRequestHandler

transation = ["12345432134", #client
["345234542", "23454243", "4543243234"]] #transactions

class TransactionManager():
    def __init__(self):
        self.m_client_list = []

    def is_client_into_client_list(self, newClient):
        if newClient in self.m_client_list:
            return True
        else:
            return False

    def add_client_into_client_list(self, newClient):
        if not self.is_client_into_client_list:
            self.m_client_list.append(newClient)
        else:
            print('Client ' + newClient + ' already served')
    
    def on_preq_received(self, packet, client):
        self.add_client_into_client_list(client)

class AccessControlServer():
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        self.m_httpd = HTTPServer((self.m_ip, self.m_port), AcsHttpRequestHandler)
        self.start_server()

    def start_server(self):
        print('Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.m_httpd.serve_forever()

    def on_aReq_packet_received(self, packet):
        pass

    def on_cReq_packet_received(self, packet):
        pass

if __name__ == "__main__":
    AccessControlServer('localhost', 8484)