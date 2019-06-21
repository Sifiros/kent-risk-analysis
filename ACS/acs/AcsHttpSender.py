#!/usr/local/bin/python3

import requests

from .AcsPacketFactory import AcsPacketFactory

class AcsHttpSender():
    @staticmethod
    def post_data_to_endpoint(transaction_id, url, data, err_callback, timeout=None, callback=None):
            try:
                print('SENDING : request ' + data + ' to ' + url)
                session = requests.Session()
                session.trust_env = False
                response = session.post(url = url, headers= AcsHttpSender.get_header(), data = data, timeout=timeout) 
                print('RESPONSE : ' + str(response.content))
                # This callback is only used to handle the response for the resulte request
                if callback is not None:
                    jsonPacket = AcsPacketFactory.get_json_from_packet(response.content)
                    callback(jsonPacket)
            except requests.exceptions.ReadTimeout:
                err_callback(transaction_id)

    @staticmethod
    def get_header():
        return {
            'Content-Type':  'application/json'
        }