#!/usr/local/bin/python3

import json
import enum
from http.server import HTTPServer
from AcsHttpRequestHandler import AcsHttpRequestHandler
from transaction import TransactionController
from AcsPacketFactory import AcsPacketFactory
from AcsHttpSender import AcsHttpSender

class AccessControlServer(HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        self.transaction_ctrl = TransactionController(self.send_response)
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

    def remove_entry_from_transaction_list(self, transaction_id):
        self.m_request_list.pop(transaction_id, None)

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

    ##### AcsHttpSender callbacks #####

    def on_rRes_packet_received(self, packet):
        # rRes received, post back response to creq
        self.get_transaction_from_list(packet["threeDSServerTransID"]).send_complete_response(200, json.dumps("{}")) #TODO : send back final cres
        self.remove_entry_from_transaction_list(packet["threeDSServerTransID"])

    ##### TransactionController callbacks #####
    
    def send_response(self, transaction_id, packet):
        if packet["messageType"] == "ARes":
            # Send Ares Response
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            # Then if the current transaction does not need auth chall, post final resul request
            if packet["transStatus"] == "Y":
                AcsHttpSender.post_data_to_endpoint(self.get_transaction_from_list(transaction_id).client_address_to_url(), json.dumps("{}"), 10,  self.on_rRes_packet_received) # TODO : send final Rreq
            self.remove_entry_from_transaction_list(transaction_id)
        elif packet["messageType"] == "CRes":
            # Chall successful, post final Rreq and wait for its response to send final Cres
            AcsHttpSender.post_data_to_endpoint(self.get_transaction_from_list(transaction_id).client_address_to_url(), json.dumps("{}"), 10,  self.on_rRes_packet_received) # TODO : post  final Rreq
        elif packet["messageType"] == "SRes":
            # Chall failed, send Sres to notify client
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            self.remove_entry_from_transaction_list(transaction_id)

if __name__ == "__main__":
    AccessControlServer('localhost', 8484)