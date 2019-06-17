#!/usr/local/bin/python3

import json
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from .AcsPacketFactory import AcsPacketFactory
from .AcsHttpSender import AcsHttpSender
from config import HTTP_PORT, HTTP_HOST

class AcsHttpRequestHandler(BaseHTTPRequestHandler):

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

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())

    def client_address_to_url(self):
        return 'http://' + self.client_address[0] + ':' + str(self.client_address[1])

    def get_threeDSMethodURL(self):
        return 'http://{}:{}/harvestcontent'.format(HTTP_HOST, HTTP_PORT)

    def route_parser(self, packet):
        # Preq handler
        if self.path == '/updatepres':
            self.send_complete_response(200, json.dumps(AcsPacketFactory.get_pResp_packet(packet["threeDSServerTransID"], self.get_threeDSMethodURL())))
        # Hreq handler(harvester html code)
        elif self.path == '/harvestcontent':
            self.send_complete_response(200, json.dumps(AcsPacketFactory.get_hResp_packet()))
            AcsHttpSender.post_data_to_endpoint(packet['notificationMethodURL'], json.dumps(AcsPacketFactory.get_notification_method_url_packet(packet['threeDSServerTransID'])))
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
            