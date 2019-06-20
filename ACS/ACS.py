#!/usr/local/bin/python3

import json
import enum
from http.server import HTTPServer
from transaction import TransactionController
from acs import AcsPacketFactory, AcsHttpSender, AcsHttpRequestHandler
from socketserver import ThreadingMixIn

rReq_rte = '/threeDSComponent/resrequest'
cRes_rte = '/threeDSComponent/challresponse'

class AccessControlServer(ThreadingMixIn, HTTPServer):
    def __init__(self, ip, port):
        self.m_ip = ip
        self.m_port = port

        self.transaction_ctrl = TransactionController(self.send_response)
        self.m_request_list = {}
        self.m_cRes_packets_wainting = {}

        ThreadingMixIn.__init__(self)
        HTTPServer.__init__(self, (self.m_ip, self.m_port), AcsHttpRequestHandler)
        print('INFO : Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

    def get_transaction_from_list(self, transaction_id):
        if transaction_id in self.m_request_list:
            return self.m_request_list[transaction_id]
        else:
            print('ERROR : Unable to find the ID ' + transaction_id + ' into request list')
            return None

    def add_transaction_in_transaction_list(self, transaction_id, handler):
        print("INFO : Adding transaction "  + transaction_id)
        self.m_request_list[transaction_id] = handler

    def remove_entry_from_transaction_list(self, transaction_id):
        print("INFO : Removing transaction "  + transaction_id)
        self.m_request_list.pop(transaction_id, None)

    def get_packet_in_cRes_packet_waiting_list(self, transaction_id):
        if transaction_id in self.m_request_list:
            return self.m_request_list[transaction_id]
        else:
            print('ERROR : Unable to find the ID ' + transaction_id + ' into cRes packet wainting list')
            return None

    def add_packet_in_cRes_packet_waiting_list(self, transaction_id, packet):
        print("INFO : Adding wainting cRes for transaction "  + transaction_id)
        self.m_cRes_packets_wainting[transaction_id] = packet

    def remove_packet_in_cRes_packeT_waiting_list(self, transaction_id, packet):
        print("INFO : Removing wainting cRes for transaction "  + transaction_id)
        self.m_cRes_packets_wainting.pop(transaction_id, None)
    
    ##### AcsHttpRequestHandler callbacks #####

    def on_aReq_packet_received(self, handler, packet):
        self.add_transaction_in_transaction_list(packet["threeDSServerTransID"], handler)
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)

    def on_gReq_packet_received(self, handler, packet):
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)
        handler.send_complete_response(200, json.dumps(AcsPacketFactory.get_gResp_packet()))

    def on_sReq_packet_received(self, handler, packet):
        self.add_transaction_in_transaction_list(packet["threeDSServerTransID"], handler)
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)        

    ##### AcsHttpSender callbacks #####

    def on_transaction_error_while_sending(self, transaction_id):
        print("TIMEOUT : " + transaction_id + " Aborting transaction...")
        # TODO : ABORT TRANSACTION INTO TM

    def on_rRes_packet_received(self, packet):
        # rRes received, post back final response to creq
        self.get_transaction_from_list(packet["threeDSServerTransID"]).send_complete_response(200, json.dumps(self.get_packet_in_cRes_packet_waiting_list(packet["threeDSServerTransID"])))
        self.remove_entry_from_transaction_list(packet["threeDSServerTransID"])
        self.remove_packet_in_cRes_packeT_waiting_list(packet["threeDSServerTransID"])

    ##### TransactionController callbacks #####
    
    def send_response(self, transaction_id, packet):
        if packet["messageType"] == "ARes":
            # Send Ares Response
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            # Then if the current transaction does not need auth chall, post final resul request
            if packet["transStatus"] == "Y":
                self.add_packet_in_cRes_packet_waiting_list(transaction_id, packet)
                AcsHttpSender.post_data_to_endpoint(packet["threeDSServerTransID"], self.get_transaction_from_list(transaction_id).client_address_to_url() + cRes_rte, json.dumps(AcsPacketFactory.get_rReq_packet(transaction_id, packet["transStatus"])), self.on_transaction_error_while_sending, 10,  self.on_rRes_packet_received)
            else:
                self.remove_entry_from_transaction_list(transaction_id)
        elif packet["messageType"] == "CRes":
            # Chall successful, post final Rreq and wait for its response to send final Cres
            AcsHttpSender.post_data_to_endpoint(packet["threeDSServerTransID"], self.get_transaction_from_list(transaction_id).client_address_to_url() + rReq_rte, json.dumps(packet), self.on_transaction_error_while_sending, 10,  self.on_rRes_packet_received)
        elif packet["messageType"] == "SRes":
            # Chall failed, send Sres to notify client
            self.get_transaction_from_list(transaction_id).send_complete_response(200, json.dumps(packet))
            self.remove_entry_from_transaction_list(transaction_id)
