#!/usr/local/bin/python3

import json
from io import BytesIO
from http.server import BaseHTTPRequestHandler
from AcsPacketFactory import AcsPacketFactory

MessageType = {
    "PReq": "PReq",
    "PRes": "PRes",
    "CONTROL_SESSION": "CONTROL_SESSION",
    "BIOFEEDBACK": "BIOFEEDBACK",
    "INIT": "INIT"
}

class AcsHttpRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            jsonPacket = AcsPacketFactory.get_json_from_packet(body)
            self.route_parser(jsonPacket)
        except json.decoder.JSONDecodeError:
            print('ERROR: Unable to parse the current Json : ' + str(body))
            #self.send_complete_response(400, self.get_program_state_packet(False, 'Unable to parse the current Json'))

    def send_complete_response(self, code, content):
        self.send_response(code)
        self.end_headers()
        response = BytesIO()
        response.write(content.encode())
        self.wfile.write(response.getvalue())

    def route_parser(self, packet):
        if self.path == '/updatepres':
            pass
        elif self.path == '/authrequest':
            pass
        elif self.path == '/challrequest':
            pass
        else:
            #SEND ERROR
            pass