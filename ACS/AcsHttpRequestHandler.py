#!/usr/local/bin/python3

import json
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from AcsPacketFactory import AcsPacketFactory
from AcsUtils import UuidUtils

class AcsHttpRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            jsonPacket = AcsPacketFactory.get_json_from_packet(body)
            self.route_parser(jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            self.send_complete_response(101, json.dumps(AcsPacketFactory.get_error_packet('Unknown', str(UuidUtils.get_new_uuid()), 101, 'Unable to parse the current Json', 'Unknown')))

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())

    def route_parser(self, packet):
        if self.path == '/updatepres':
            self.send_complete_response(200, json.dumps(AcsPacketFactory.get_PResp_packet(packet["threeDSServerTransID"])))
        elif self.path == '/authrequest':
            self.server.on_aReq_packet_received(self, packet)
        elif self.path == '/challrequest':
            self.server.on_cReq_packet_received(self, packet)
        else:
            self.send_complete_response(101, json.dumps(AcsPacketFactory.get_error_packet(packet["threeDSServerTransID"], str(UuidUtils.get_new_uuid()), 101, 'Unknown route', packet["messageType"])))
            