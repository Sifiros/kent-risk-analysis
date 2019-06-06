#!/usr/local/bin/python3

import uuid

class UuidUtils():
    @staticmethod
    def get_new_uuid():
        return uuid.uuid4()