// ARes message samples
// Not sure about where does it goes and comes from
// TODO lean about it

// authentication mesages 

// getter for BRW Challenge flow
// BRW

let getBRWChallengeFlow = () => {
    return {
        "messageVersion": "2.1.0",
        "dsTransID": "f25084f0-5b16-4c0a-ae5d-b24808a95e4b",
        "messageType": "ARes",
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
        "acsReferenceNumber": "3DS_LOA_ACS_PPFU_020100_00009",
        "acsOperatorID": "AcsOpId 4138359541",
        "dsReferenceNumber": "DS_LOA_DIS_PPFU_020100_00010",
        "transStatus": "C",
        "acsChallengeMandated": "Y",
        "acsURL": "http://localhost:4242/acs/providechallenge",
        "authenticationType": "01"
    }
}

module.exports = {
    getBRWChallengeFlow
}