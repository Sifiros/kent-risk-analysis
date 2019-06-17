#!/usr/local/bin/python3

import requests

from .AcsPacketFactory import AcsPacketFactory

class AcsHttpSender():
    @staticmethod
    def post_data_to_endpoint(url, data, timeout=None, callback=None):
            try:
                response = requests.post(url = url, headers= AcsHttpSender.get_header(), data = data, timeout=timeout) 
                if callback is not None:
                    jsonPacket = AcsPacketFactory.get_json_from_packet(response.content)
                    callback(jsonPacket)
            except requests.exceptions.ReadTimeout: 
                pass

    @staticmethod
    def get_header():
        return {
            'Content-Type':  'application/json'
        }