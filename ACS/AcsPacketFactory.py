#!/usr/local/bin/python3

import json

class AcsPacketFactory():

    @staticmethod
    def get_PResp_json(threeDSServerTransID, dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', serialNum='3q9oaApFqmznys47ujRg', messageVersion='2.1.0'):
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
        return json.dumps(pRest_packet)

    @staticmethod
    def get_AResp_json(threeDSServerTransID, acsTransID, transStatus, acsChallengeMandated, acsURL, dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', 
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
        return json.dumps(aResp_packet)

    @staticmethod
    def get_CResp_json(threeDSServerTransID, acsTransID, challengeCompletionInd, messageVersion='2.1.0'):
        cResp_packet = {
            "messageType": "CRes",
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "acsTransID": acsTransID, # Unique ACS transaction Identifier
            "challengeCompletionInd": challengeCompletionInd, # Indicator of the state of the ACS challenge (Y, N)
            "notificationURL": "link",
            "messageVersion": messageVersion,
        }
        return json.dumps(cResp_packet)

    @staticmethod
    def get_RReq_json(threeDSServerTransID, acsTransID, transStatus, acsRenderingType={"acsInterface": "01","acsUiTemplate": "01"}, authenticationMethod='02',
        authenticationType='02', authenticationValue='MTIzNDU2Nzg5MDA5ODc2NTQzMjE=', dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', interactionCounter='02',
        messageCategory='01', messageVersion='2.1.0'):
        rReq_packet = {
            "messageType": "RReq",
            "threeDSServerTransID": threeDSServerTransID, # Unique 3ds transaction Identifier
            "acsTransID": acsTransID, # Unique ACS transaction Identifier
            "acsRenderingType": acsRenderingType, # Irrelevant
            "authenticationMethod": authenticationMethod, # Irrelevant 
            "authenticationType": authenticationType, # Irrelevant 
            "authenticationValue": authenticationValue, # Irrelevant 
            "dsTransID": dsTransID, # Unique ds transaction Identifier - Irrelevant
            "eci": "05", # Payment System-specific value provided by the ACS or DS to indicate the results of the attempt to authenticate the Cardholder.
            "interactionCounter": interactionCounter,
            "messageCategory": messageCategory,
            "messageVersion": messageVersion,
            "transStatus": transStatus # Indicates whether a transaction qualifies as an authenticated transaction or account verification (Y, N, U, A, C, D, R)
        }
        return json.dumps(rReq_packet)

    @staticmethod
    def get_error_json(threeDSServerTransID, acsTransID, errorCode, errorDescription, errorMessageType, errorDetail=None, 
    dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', messageVersion='2.1.0'):
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
        return json.dumps(error_packet)

    @staticmethod
    def get_json_from_packet(packet):
        return json.loads(packet)