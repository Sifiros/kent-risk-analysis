#!/usr/local/bin/python3

import json

class AcsPacketFactory():

    @staticmethod
    def get_pResp_packet(threeDSServerTransID, threeDSMethodURL, dsTransID='f25084f0-5b16-4c0a-ae5d-b24808a95e4b', serialNum='3q9oaApFqmznys47ujRg', messageVersion='2.1.0'):
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
                "threeDSMethodURL": threeDSMethodURL
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
    def get_hResp_packet(iframe_url):
        return {
            "iframeUrl": iframe_url
        }
    
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
    def get_notification_method_url_packet(threeDSTransID, status):
        nmu_packet  = {
            "methodStatus": status,
            "threeDSServerTransID": threeDSTransID
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
            "interactionCounter": "1",
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

    ##### MOCKS #####

    @staticmethod
    def get_gReq_packet():
        gReq_packet = {
            "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
            "doNotTrack": 1,
            "screenSize": "1920:1080",
            "plugins": ["Adblocks", "Google"],
            "position": {
                "lat": 95,
                "lng": 1.234525
            },
            "browser": {"appName": "Netscape", "major": "67", "name": "Firefox", "version": "67.0"},
            "cpu": { "architecture": "amd64" },
            "os": { "name": "Windows", "version": "10" }
        }
        return gReq_packet

    @staticmethod
    def get_aReq_packet():
        aReq_packet = {
            "threeDSCompInd": "U",
            "threeDSRequestorID": "az0123456789",
            "threeDSRequestorName": "threeDSDemonstrator",
            "threeDSRequestorURL": "localhost:4242/merchant",
            "acquirerBIN": "868491",
            "acquirerMerchantID": "mGm6AJZ1YotkJJmOk0fx",
            "addrMatch": "N",
            "cardExpiryDate": "1910",
            "acctNumber": "8944988785642183",
            "billAddrCity": "Bill City Name",
            "billAddrCountry": "840",
            "billAddrLine1": "Bill Address Line 1",
            "billAddrLine2": "Bill Address Line 2",
            "billAddrLine3": "Bill Address Line 3",
            "billAddrPostCode": "Bill Post Code",
            "billAddrState": "CO",
            "email": "example@example.com",
            "notificationURL" : 'http://localhost:4242/merchant/notification',
            "homePhone": {
                "cc": "123",
                "subscriber": "123456789"
            },
            "mobilePhone": {
                "cc": "123",
                "subscriber": "123456789"
            },
            "cardholderName": "Cardholder Name",
            "shipAddrCity": "Ship City Name",
            "shipAddrCountry": "840",
            "shipAddrLine1": "Ship Address Line 1",
            "shipAddrLine2": "Ship Address Line 2",
            "shipAddrLine3": "Ship Address Line 3",
            "shipAddrPostCode": "Ship Post Code",
            "shipAddrState": "CO",
            "workPhone": {
                "cc": "123",
                "subscriber": "123456789"
            },
            "deviceChannel": "02",
            "browserAcceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "browserIP": "192.168.1.11",
            "browserJavaEnabled": True,
            "browserLanguage": "en",
            "browserColorDepth": "48",
            "browserScreenHeight": "400",
            "browserScreenWidth": "600",
            "browserTZ": "0",
            "browserUserAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)Gecko/20100101 Firefox/47.0",
            "mcc": "5411",
            "merchantCountryCode": "840",
            "merchantName": "UL TS BV",
            "messageCategory": "01",
            "messageType": "AReq",
            "messageVersion": "2.1.0",
            "purchaseAmount": "101",
            "purchaseCurrency": "978",
            "purchaseExponent": "2",
            "purchaseDate": "20170316141312",
            "transType": "01",
            "threeDSServerURL": "http://localhost:4242/threedsserver",
            "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
            "threeDSServerRefNumber": "3DS_LOA_SER_PPFU_020100_00008",
            "threeDSRequestorAuthenticationInd": "03",
            "threeDSRequestorAuthenticationInfo": {
                "threeDSReqAuthMethod": "02",
                "threeDSReqAuthTimestamp": "201711071307",
                "threeDSReqAuthData": "validlogin at UL TS BV"
            },
            "threeDSRequestorChallengeInd": "02",
            "threeDSRequestorPriorAuthenticationInfo": {
                "threeDSReqPriorRef": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
                "threeDSReqPriorAuthMethod": "02",
                "threeDSReqPriorAuthTimestamp": "201710282113",
                "threeDSReqPriorAuthData": "cKTYtrvvKU7gUoiqbbO7Po"
            },
            "threeDSServerOperatorID": "1jpeeLAWgGFgS1Ri9tX9",
            "acctType": "03",
            "acctInfo": {
                "chAccAgeInd": "03",
                "chAccDate": "20140328",
                "chAccChangeInd": "04",
                "chAccChange": "20160712",
                "chAccPwChangeInd": "02",
                "chAccPwChange": "20170328",
                "shipAddressUsageInd": "04",
                "shipAddressUsage": "20160714",
                "txnActivityDay": "1",
                "txnActivityYear": "21",
                "provisionAttemptsDay": "0",
                "nbPurchaseAccount": "11",
                "suspiciousAccActivity": "01",
                "shipNameIndicator": "02",
                "paymentAccInd": "04",
                "paymentAccAge": "20160917"
            },
            "acctID": "personal account",
            "dsReferenceNumber": "DS_LOA_DIS_PPFU_020100_00010",
            "dsTransID": "1jpe0dc0-i9t2-4067-bcb1-nmt866956sgd",
            "dsURL": "http://localhost:4242/ds",
            "payTokenInd": True,
            "purchaseInstalData": "024",
            "merchantRiskIndicator": {
                "shipIndicator": "02",
                "deliveryTimeframe": "01",
                "deliveryEmailAdresse": "deliver@email.com",
                "reorderItemsInd": "01",
                "preOrderPurchaseInd": "02",
                "preOrderDate": "20170519",
                "giftCardAmount": "337",
                "giftCardCurr": "840",
                "giftCardCount": "02"
            },
            "messageExtension": [{
                "name": "msgextname",
                "id": "501341592B_0001_4567",
                "criticalityIndicator": False,
                "data": {
                    "valueOne": "messageextensiondata",
                    "valueTwo": "moremessageextensiondata"
                }
            }],
            "recurringExpiry": "20180131",
            "recurringFrequency": "6",
            "broadInfo": { "message": "TLS 1.x will be turned off starting summer 2019" }
        }
        return aReq_packet

    @staticmethod
    def get_cReq_packet():
        cReq_packet = {
            "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
            "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
            "messageType": "CReq",
            "messageVersion": "2.1.0",
            "sdkTransID": "b2385523-a66c-4907-ac3c-91848e8c0067",
            "sdkCounterStoA": "001"
        }
        return cReq_packet

    @staticmethod
    def get_json_from_packet(packet):
        return json.loads(packet)