#!/usr/local/bin/python3

import json
import enum
import requests
from http.server import HTTPServer
from AcsHttpRequestHandler import AcsHttpRequestHandler
from AcsPacketFactory import AcsPacketFactory

class AccessControlServer(HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        self.m_request_list = {}
        HTTPServer.__init__(self, (self.m_ip, self.m_port), AcsHttpRequestHandler)
        print('Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

    def post_data_to_endpoint(self, url, data):
        json = data
        try:
            requests.post(url = url, data = data, timeout=0.0000000001) 
        except requests.exceptions.ReadTimeout: 
            pass
    def get_transaction_from_list(self, transaction_id):
        if transaction_id in self.m_request_list:
            return self.m_request_list[transaction_id]
        else:
            print('ERROR : Unable to find the ID ' + transaction_id + ' into request list')
            return None

    ##### AcsHttpRequestHandler callbacks #####

    def on_aReq_packet_received(self, handler, packet):
        self.m_request_list[packet["threeDSServerTransID"]] = handler
        # TODO : Send packet to TransactionController

    def on_gReq_packet_received(self, handler, packet):
        # TODO : Send packet to TransactionController
        handler.send_complete_response(200, json.dumps(AcsPacketFactory.get_gResp_packet()))

    def on_sReq_packet_received(self, handler, packet):
        pass

    ##### TransactionController callbacks #####
    
    def send_response(self, transaction_id, packet):
        if packet["messageType"] == "ARes":
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            
    def remove_entry_from_transaction_list(self, transaction_id):
        self.m_request_list.pop(transaction_id, None)

if __name__ == "__main__":
    AccessControlServer('localhost', 8484)