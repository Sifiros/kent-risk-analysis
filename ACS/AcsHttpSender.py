#!/usr/local/bin/python3
import requests

class AcsHttpSender():
    @staticmethod
    def post_data_to_endpoint(url, data):
            json = data
            requests.post(url = url, data = data, timeout=None)