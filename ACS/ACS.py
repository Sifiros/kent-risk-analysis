#!/usr/local/bin/python3
import json
import enum
from http.server import HTTPServer
from AcsHttpRequestHandler import AcsHttpRequestHandler
from transaction import TransactionController
from AcsPacketFactory import AcsPacketFactory

class AccessControlServer(HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        self.transaction_ctrl = TransactionController()
        self.m_request_list = {}
        HTTPServer.__init__(self, (self.m_ip, self.m_port), AcsHttpRequestHandler)
        print('Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

    def get_transaction_from_list(self, transaction_id):
        if transaction_id in self.m_request_list:
            return self.m_request_list[transaction_id]
        else:
            print('ERROR : Unable to find the ID ' + transaction_id + ' into request list')
            return None

    ##### AcsHttpRequestHandler callbacks #####

    def on_aReq_packet_received(self, handler, packet):
        self.m_request_list[packet["threeDSServerTransID"]] = handler
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)

    def on_gReq_packet_received(self, handler, packet):
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)
        handler.send_complete_response(200, json.dumps(AcsPacketFactory.get_gResp_packet()))

    def on_sReq_packet_received(self, handler, packet):
        self.m_request_list[packet["threeDSServerTransID"]] = handler
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)        

    ##### TransactionController callbacks #####
    
    def send_response(self, transaction_id, packet):
        if packet["messageType"] == "ARes":
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            self.remove_entry_from_transaction_list(transaction_id)
        elif packet["messageType"] == "CRes":
            # TODO : send RReq, wait for the response and then send CRes
            pass
        elif packet["messageType"] == "SRes":
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            self.remove_entry_from_transaction_list(transaction_id)

    def remove_entry_from_transaction_list(self, transaction_id):
        self.m_request_list.pop(transaction_id, None)