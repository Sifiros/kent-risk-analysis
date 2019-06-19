#!/usr/local/bin/python3

import requests

from .AcsPacketFactory import AcsPacketFactory

class AcsHttpSender():
    @staticmethod
    def post_data_to_endpoint(url, data, timeout=None, callback=None):
            try:
                print('SENDING : request ' + data + ' to ' + url)
                response = requests.post(url = url, headers= AcsHttpSender.get_header(), data = data, timeout=timeout) 
                print('RESPONSE : ' + str(response.content))
                if callback is not None:
                    jsonPacket = AcsPacketFactory.get_json_from_packet(response.content)
                    callback(jsonPacket)
            except requests.exceptions.ReadTimeout:
                # TODO : MANAGE TRANSACTION GIVE UP
                pass

    @staticmethod
    def get_header():
        return {
            'Content-Type':  'application/json'
        }