#!/usr/local/bin/python3

import json

class AcsPacketFactory():

    @staticmethod
    def get_pResp_packet(threeDSServerTransID, dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', serialNum='3q9oaApFqmznys47ujRg', messageVersion='2.1.0'):
        pRest_packet = {
            "messageType": "PRes",
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "dsTransID": dsTransID, # Unique ds transaction Identifier - Irrelevant
            "messageVersion": messageVersion,
            "serialNum": serialNum, # Irrelevant
            "dsStartProtocolVersion": "2.1.0", # Irrelevant
            "dsEndProtocolVersion": "2.1.0", # Irrelevant
            "cardRangeData": [{ # Card range
                "startRange": "1000000000000000",
                "endRange": "9999999999999999",
                "actionInd": "A",
                "acsStartProtocolVersion": "2.1.0",
                "acsEndProtocolVersion": "2.1.0",
                "threeDSMethodURL": "https://www.acs.com/script"
            }]
        }
        return pRest_packet

    @staticmethod
    def get_aResp_packet(threeDSServerTransID, transStatus, acsChallengeMandated, acsURL, acsTransID='d7c1ee99-9478-44a6-b1f2-391e29c6b340', dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', 
    acsReferenceNumber='3DS_LOA_ACS_PPFU_020100_00009', acsOperatorID='AcsOpId 4138359541', dsReferenceNumber='DS_LOA_DIS_PPFU_020100_00010',
    authenticationType='01', messageVersion='2.1.0'):
        aResp_packet = {
            "messageType": "ARes",
            "messageVersion": messageVersion,
            "dsTransID": dsTransID, # Unique ds transaction Identifier - Irrelevant
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "acsTransID": acsTransID, # Unique ACS transaction Identifier
            "acsReferenceNumber": acsReferenceNumber, # Irrelevant
            "acsOperatorID": acsOperatorID, # Irrelevant
            "dsReferenceNumber": dsReferenceNumber, # Irrelevant
            "transStatus": transStatus, # Indicates whether a transaction qualifies as an authenticated transaction or account verification (Y, N, U, A, C, D, R)
            "acsChallengeMandated": acsChallengeMandated, # Indication of whether a challenge is required for the transaction to be authorised due to local/regional mandates or other variable. (Y, N)
            "acsURL": acsURL, # Fully qualified URL of the ACS to be used for the challenge
            "authenticationType": authenticationType # Irrelevant
        }
        return aResp_packet

    @staticmethod
    def get_cResp_packet(threeDSServerTransID, challengeCompletionInd, acsTransID='d7c1ee99-9478-44a6-b1f2-391e29c6b340', messageVersion='2.1.0'):
        cResp_packet = {
            "messageType": "CRes",
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "acsTransID": acsTransID, # Unique ACS transaction Identifier
            "challengeCompletionInd": challengeCompletionInd, # Indicator of the state of the ACS challenge (Y, N)
            "notificationURL": "link",
            "messageVersion": messageVersion,
        }
        return cResp_packet

    @staticmethod
    def get_sResp_packet(isValid):
        sResp_packet = {
            "messageType": "SRes",
            "isValid": isValid
        }
        return sResp_packet

    @staticmethod
    def get_hResp_packet():
        hcResp_packet = {
            "messageType": "HRes"
        }
        return hcResp_packet
    
    @staticmethod
    def get_html_cResp_packet():
        htmlcResp_packet = {
            "messageType": "HTMLCRes"
        }
        return htmlcResp_packet

    @staticmethod
    def get_gResp_packet():
        gRest_packet = {
            "messageType": "GRes",
            "status": True
        }
        return gRest_packet

    @staticmethod
    def get_notification_method_url_packet(threeDSTransID):
        nmu_packet  = {
            "methodStatus": "ok",
            "threeDSTransID": threeDSTransID
        }
        return nmu_packet



    @staticmethod
    def get_rReq_packet(threeDSServerTransID, transStatus, acsTransID='d7c1ee99-9478-44a6-b1f2-391e29c6b340', acsRenderingType={"acsInterface": "01","acsUiTemplate": "01"}, authenticationMethod='02',
    authenticationType='02', authenticationValue='MTIzNDU2Nzg5MDA5ODc2NTQzMjE=', dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', interactionCounter='02',
        messageCategory='01', messageVersion='2.1.0'):
        rReq_packet = {
            "messageType": "RReq",
            "messageVersion": messageVersion,
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "acsTransID": acsTransID, # Unique ACS transaction Identifier
            "acsRenderingType": acsRenderingType, # Irrelevant
            "authenticationMethod": authenticationMethod, # Irrelevant 
            "authenticationType": authenticationType, # Irrelevant 
            "authenticationValue": authenticationValue, # Irrelevant 
            "dsTransID": dsTransID, # Unique ds transaction Identifier - Irrelevant
            "eci": "05", # Payment System-specific value provided by the ACS or DS to indicate the results of the attempt to authenticate the Cardholder - Irrelevant
            "interactionCounter": interactionCounter,
            "messageCategory": messageCategory, # Irrelevant
            "transStatus": transStatus # Indicates whether a transaction qualifies as an authenticated transaction or account verification (Y, N, U, A, C, D, R)
        }
        return rReq_packet

    @staticmethod
    def get_error_packet(threeDSServerTransID, errorCode, errorDescription, errorMessageType, errorDetail=None, 
    acsTransID='d7c1ee99-9478-44a6-b1f2-391e29c6b340', dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', messageVersion='2.1.0'):
        error_packet = {
            "messageType": "Erro",
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "acsTransID": acsTransID, # Unique ACS transaction Identifier
            "dsTransID": dsTransID, # Unique ds transaction Identifier - Irrelevant
            "errorCode": errorCode, # Type of problem identified in the message
            "errorComponent": "A", # 3-D Secure component that identified the error
            "errorDescription": errorDescription, # Text describing the problem identified in the message
            "errorDetail": errorDetail, # Additional detail 
            "errorMessageType": errorMessageType, # Identifies the Message Type that was identified as erroneous
            "messageVersion": messageVersion
        }
        return error_packet

    @staticmethod
    def get_json_from_packet(packet):
        return json.loads(packet)