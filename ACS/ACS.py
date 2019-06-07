#!/usr/local/bin/python3

import json
import enum
import requests
from http.server import HTTPServer
from AcsHttpRequestHandler import AcsHttpRequestHandler
from transaction import TransactionController

class AccessControlServer(HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        self.m_request_list = {}
        self.m_long_polling_request_list = {}
        HTTPServer.__init__(self, (self.m_ip, self.m_port), AcsHttpRequestHandler)
        print('Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

        self.transaction_ctrl = TransactionController()

    def post_data_to_endpoint(self, url, data):
        json = data
        try:
            requests.post(url = url, data = data, timeout=0.0000000001) 
        except requests.exceptions.ReadTimeout: 
            pass
    
    ##### AcsHttpRequestHandler callbacks #####

    def on_aReq_packet_received(self, handler, packet):
        self.m_request_list[packet["threeDSServerTransID"]] = handler

    def on_cReq_packet_received(self, handler, packet):
        self.m_long_polling_request_list[packet["threeDSServerTransID"]] = handler

    ##### TransactionController callbacks #####
    
    def send_response(self, transactionId, packet):
        if packet["messageType"] == "CRes":
            if transactionId in self.m_long_polling_request_list:
                self.m_long_polling_request_list[transactionId].send_complete_response(200, json.dumps(packet))
                self.remove_entry_from_transaction_list(transactionId, True)
            else:
                print('ERROR : Unable to find the ID ' + transactionId + ' into long polling request list')
        elif packet["messageType"] == "ARes" or packet["messageType"] == "SRes":
            if transactionId in self.m_request_list:
                self.m_request_list[transactionId].send_complete_response(200, json.dumps(packet))
                self.remove_entry_from_transaction_list(transactionId, False)
            else:
                print('ERROR : Unable to find the ID ' + transactionId + ' into request list')
            
    def remove_entry_from_transaction_list(self, transactionId, isLongPolling):
        if isLongPolling:
            self.m_long_polling_request_list.pop(transactionId, None)
        else:
            self.m_request_list.pop(transactionId, None)

if __name__ == "__main__":
    AccessControlServer('localhost', 8484)