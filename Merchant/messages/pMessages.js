// Preparation messages
// BRW

let getPRequest = () => {
    return {
        "threeDSServerRefNumber": "3DS_LOA_SER_PPFU_020100_00008",
        "threeDSServerOperatorID": "1jpeeLAWgGFgS1Ri9tX9",
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "messageType": "PReq",
        "messageVersion": "2.1.0",
        "serialNum": "66lM7xWInwjdqG1SSFk5"
    }
}

let getPResponse = () => {
    return {
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "dsTransID": "f25084f0-5b16-4c0a-ae5d-b24808a95e4b",
        "messageType": "PRes",
        "messageVersion": "2.1.0",
        "serialNum": "3q9oaApFqmznys47ujRg",
        "dsStartProtocolVersion": "2.1.0",
        "dsEndProtocolVersion": "2.1.0",
        "cardRangeData": [{
            "startRange": "1000000000000000",
            "endRange": "9999999999999999",
            "actionInd": "A",
            "acsStartProtocolVersion": "2.1.0",
            "acsEndProtocolVersion": "2.1.0",
            "threeDSMethodURL": "https://www.acs.com/script"
        }]
    }
}

module.exports = {
    getPRequest,
    getPResponse
}