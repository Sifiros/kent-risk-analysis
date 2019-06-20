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
        super().__init__(*args, directory="Harvester/", **kwargs)    

    def send_cors_header(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            self.client_address_to_url()
            jsonPacket = AcsPacketFactory.get_json_from_packet(body)
            self.route_parser(jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(404, json.dumps(AcsPacketFactory.get_error_packet('Unknown', 101, 'Unable to parse the current Json', 'Unknown')))

    def do_HEAD(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()

    def do_OPTIONS(self):           
        self.send_response(200)
        self.send_cors_header()
        self.end_headers()

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

    def route_parser(self, packet):
        # Preq handler
        if self.path == '/updatepres':
            self.send_complete_response(200, json.dumps(AcsPacketFactory.get_pResp_packet(packet["threeDSServerTransID"], self.get_threeDSMethodURL())))
        # Hreq handler(harvester html code)
        elif self.path == '/harvestcontent':
            self.send_complete_response(200, json.dumps(AcsPacketFactory.get_hResp_packet(self.get_iframe_url(packet['threeDSServerTransID']))))
            AcsHttpSender.post_data_to_endpoint(packet["threeDSServerTransID"], packet['notificationMethodURL'], json.dumps(AcsPacketFactory.get_notification_method_url_packet(packet['threeDSServerTransID'])), self.server.on_transaction_error_while_sending)
        # Greq handler (harvester data)
        elif self.path == '/harvestrequest':
            self.server.on_gReq_packet_received(self, packet)
        # Areq handler
        elif self.path == '/authrequest':
            self.server.on_aReq_packet_received(self, packet)
        # Creq handler
        elif self.path == '/challrequest':
            self.send_complete_response(200, json.dumps(AcsPacketFactory.get_html_cResp_packet()))
        # Sreq handler
        elif self.path == '/challsubmition':
            self.server.on_sReq_packet_received(self, packet)
        else:
            self.send_complete_response(404, json.dumps(AcsPacketFactory.get_error_packet(packet["threeDSServerTransID"], 101, 'Unknown route', packet["messageType"])))
            