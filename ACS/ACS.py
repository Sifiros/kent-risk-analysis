#!/usr/local/bin/python3

import json
import enum
import threading
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
        self.m_notification_list = {}
        self.m_cRes_packets_wainting = {}
        self.m_timer_list = {}

        ThreadingMixIn.__init__(self)
        HTTPServer.__init__(self, (self.m_ip, self.m_port), AcsHttpRequestHandler)
        print('INFO : Launching ACS HTTP server on ' + str(self.m_ip) + ':' + str(self.m_port))
        self.serve_forever()

    def get_item_from_dic(self, dic, id):
        if id in dic:
            return dic[id]
        else:
            print('ERROR : Unable to find the id {} in the dictionnary {}'.format(id, str(dic)))
            return None

    def add_item_into_dic(self, dic, id, item):
        print('INFO : Adding item id {} into dic {}'.format(id, str(dic)))
        dic[id] = item

    def remove_item_from_dic(self, dic, id):
        print('INFO : Removing item id {} into dic {}'.format(id, str(dic)))
        dic.pop(id,  None)
    
    ##### NotifTimer callbacks #####

    def notif_timeout(self, *args, **kwargs):
        print("INFO : Timeout for transaction {}".format(args[0]))
        self.remove_item_from_dic(self.m_timer_list, args[0])
        self.remove_item_from_dic(self.m_notification_list, args[0])
        self.remove_item_from_dic(self.m_request_list, args[0])
        # TODO : CLEAR TRANSATION INTO TM


    ##### AcsHttpRequestHandler callbacks #####

    def on_hReq_packet_received(self, handler, packet):
        self.add_item_into_dic(self.m_notification_list, packet["threeDSServerTransID"], packet["notificationMethodURL"])
        
        # Start notif timer (10sec)
        print('INFO : Starting timer for transaction {}'.format(packet["threeDSServerTransID"]))
        notif_timer = threading.Timer(2.0, self.notif_timeout, [packet["threeDSServerTransID"]])
        notif_timer.start()
        self.add_item_into_dic(self.m_timer_list, packet["threeDSServerTransID"], notif_timer)

    def on_aReq_packet_received(self, handler, packet):
        self.add_item_into_dic(self.m_request_list, packet["threeDSServerTransID"], handler)
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)

    def on_gReq_packet_received(self, handler, packet):
        # Cancel notif timer
        print('INFO : Cancelling timer for transaction {}'.format(packet["threeDSServerTransID"]))
        self.get_item_from_dic(self.m_timer_list, packet["threeDSServerTransID"]).cancel()
        self.remove_item_from_dic(self.m_timer_list, packet["threeDSServerTransID"])

        self.remove_item_from_dic(self.m_notification_list, packet["threeDSServerTransID"])
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)
        handler.send_complete_response(200, json.dumps(AcsPacketFactory.get_gResp_packet()))

    def on_sReq_packet_received(self, handler, packet):
        self.add_item_into_dic(self.m_request_list, packet["threeDSServerTransID"], handler)
        self.transaction_ctrl.handle_transaction_request(packet["threeDSServerTransID"], packet)        

    ##### AcsHttpSender callbacks #####

    def on_transaction_error_while_sending(self, transaction_id):
        print("TIMEOUT : " + transaction_id + " Aborting transaction...")
        # TODO : CLEAR TRANSATION INTO TM
        self.remove_item_from_dic(m_request_list, transaction_id)
        self.remove_item_from_dic(m_cRes_packets_wainting, transaction_id)

    def on_rRes_packet_received(self, packet):
        # rRes received, post back final response to creq
        self.get_item_from_dic(m_request_list, packet["threeDSServerTransID"]).send_complete_response(200, json.dumps(self.get_packet_in_cRes_packet_waiting_list(packet["threeDSServerTransID"])))
        self.remove_item_from_dic(m_request_list, packet["threeDSServerTransID"])
        self.remove_item_from_dic(m_cRes_packets_wainting, packet["threeDSServerTransID"])

    ##### TransactionController callbacks #####
    
    def send_response(self, transaction_id, packet):
        if packet["messageType"] == "ARes":
            # Send Ares Response
            self.get_item_from_dic(m_request_list, transaction_id).send_complete_response(200, json.dumps(packet))
            # Then if the current transaction does not need auth chall, post final resul request
            if packet["transStatus"] == "Y":
                self.add_item_into_dic(m_cRes_packets_wainting, transaction_id, packet)
                AcsHttpSender.post_data_to_endpoint(packet["threeDSServerTransID"], self.get_transaction_from_list(transaction_id).client_address_to_url() + cRes_rte, json.dumps(AcsPacketFactory.get_rReq_packet(transaction_id, packet["transStatus"])), self.on_transaction_error_while_sending, 10,  self.on_rRes_packet_received)
            else:
                self.remove_item_from_dic(m_request_list, transaction_id)
        elif packet["messageType"] == "CRes":
            # Chall successful, post final Rreq and wait for its response to send final Cres
            AcsHttpSender.post_data_to_endpoint(packet["threeDSServerTransID"], self.get_transaction_from_list(transaction_id).client_address_to_url() + rReq_rte, json.dumps(packet), self.on_transaction_error_while_sending, 10,  self.on_rRes_packet_received)
        elif packet["messageType"] == "SRes":
            # Chall failed, send Sres to notify client
            self.get_item_from_dic(m_request_list, transaction_id).send_complete_response(200, json.dumps(packet))
            self.remove_item_from_dic(m_request_list, transaction_id)
