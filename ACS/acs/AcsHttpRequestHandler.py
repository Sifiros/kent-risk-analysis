#!/usr/local/bin/python3

import json
import os
import urllib.parse
from io import BytesIO
from http.server import BaseHTTPRequestHandler,SimpleHTTPRequestHandler
from .AcsPacketFactory import AcsPacketFactory
from .AcsHttpSender import AcsHttpSender
from config import HTTP_PORT, PUBLIC_IP

class AcsHttpRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.request_callbacks = {
            "/updatepres": self.onPReqReceived,
            "/harvestcontent": self.onHReqReceived,
            "/harvestrequest": self.onGReqReceived,
            "/authrequest": self.onAReqReceived,
            "/challrequest": self.onCReqReceived,
            "/challsubmition": self.onSReqReceived
        }

        super().__init__(*args, directory="Harvester/", **kwargs)    

    def send_cors_header(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Accept,Content-Type,Origin")

    def do_HEAD(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()

    def do_OPTIONS(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            self.client_address_to_url()
            jsonPacket = AcsPacketFactory.get_json_from_packet(body)
            self.request_callbacks[self.path](jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(404, json.dumps(AcsPacketFactory.get_error_packet('Unknown', 101, 'Unable to parse the current Json', 'Unknown')))

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.send_cors_header()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())

    def client_address_to_url(self):
        return 'http://' + self.client_address[0] + ':' + str(self.client_address[1])

    def get_threeDSMethodURL(self):
        return 'http://{}:{}/harvestcontent'.format(PUBLIC_IP, HTTP_PORT)

    def get_iframe_url(self, transaction_id):
        preforged_url = 'http://{}:{}/harvestrequest'.format(PUBLIC_IP, HTTP_PORT)
        encoded_url = urllib.parse.quote(preforged_url ,safe='')
        encoded_id = urllib.parse.quote(transaction_id ,safe='')
        return 'http://{}:{}/harvester.html?trID={}&posturl={}'.format(PUBLIC_IP, HTTP_PORT, encoded_id, encoded_url)

    def get_challenge_iframe_url(self, acsTransId, threedsServerTransId):
        submissionUrl = 'http://{}:{}/challsubmition'.format(PUBLIC_IP, HTTP_PORT)
        submissionUrl = urllib.parse.quote(submissionUrl ,safe='')
        threedsServerTransId = urllib.parse.quote(threedsServerTransId ,safe='')
        acsTransId = urllib.parse.quote(acsTransId ,safe='')
        return 'http://{}:{}/IframeChallShortMessageService.html?acstrid={}&tdstrid={}&acsurl={}'.format(PUBLIC_IP, HTTP_PORT, acsTransId, threedsServerTransId, submissionUrl)

    ##### Requests Callbacks #####

    # Handle Pre-request packet
    def onPReqReceived(self, packet):
        self.send_complete_response(200, json.dumps(AcsPacketFactory.get_pResp_packet(packet["threeDSServerTransID"], self.get_threeDSMethodURL())))

    # Handle harvester html request
    def onHReqReceived(self, packet):
        self.server.on_hReq_packet_received(self, packet)
        self.send_complete_response(200, json.dumps(AcsPacketFactory.get_hResp_packet(self.get_iframe_url(packet['threeDSServerTransID']))))

    # Handle harvested data
    def onGReqReceived(self, packet):
        self.server.on_gReq_packet_received(self, packet)
        response = json.dumps(AcsPacketFactory.get_notification_method_url_packet(packet['threeDSServerTransID'], "ok"))
        AcsHttpSender.post_data_to_endpoint(packet["threeDSServerTransID"], self.server.get_item_from_dic(self.server.m_notification_list ,packet["threeDSServerTransID"]), response, self.server.on_transaction_error_while_sending)
        self.server.remove_item_from_dic(self.server.m_notification_list, packet["threeDSServerTransID"])

    # Handle Authentication request
    def onAReqReceived(self, packet):
        self.server.on_aReq_packet_received(self, packet)

    # Handle Challenge request
    def onCReqReceived(self, packet):

        self.send_complete_response(200, json.dumps(AcsPacketFactory.get_html_cResp_packet(
            challengeIframeUrl=self.get_challenge_iframe_url(
                acsTransId=packet['acsTransID'],
                threedsServerTransId=packet['threeDSServerTransID']            
            )
        )))

    # Handle Submition request
    def onSReqReceived(self, packet):
        print(packet)
        self.server.on_sReq_packet_received(self, packet)