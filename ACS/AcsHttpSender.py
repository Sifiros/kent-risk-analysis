#!/usr/local/bin/python3
import requests
from AcsPacketFactory import AcsPacketFactory

class AcsHttpSender():
    @staticmethod
    def post_data_to_endpoint(url, data, timeout=None, callback=None):
            json = data
            try:
                response = requests.post(url = url, data = data, timeout=timeout) 
                if callback is not None:
                    jsonPacket = AcsPacketFactory.get_json_from_packet(response.content)
                    callback(jsonPacket)
            except requests.exceptions.ReadTimeout: 
                pass