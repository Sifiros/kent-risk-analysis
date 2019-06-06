

let getRRequest = () => {

    return {
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
        "acsRenderingType": {
            "acsInterface": "01",
            "acsUiTemplate": "01"
        },
        "authenticationMethod": "02",
        "authenticationType": "02",
        "authenticationValue": "MTIzNDU2Nzg5MDA5ODc2NTQzMjE=",
        "dsTransID": "f25084f0-5b16-4c0a-ae5d-b24808a95e4b",
        "eci": "05",
        "interactionCounter": "02",
        "messageCategory": "01",
        "messageType": "RReq",
        "messageVersion": "2.1.0",
        "transStatus": "Y"
    }
}

let getRResponse = () => {
    return {
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
        "dsTransID": "f25084f0-5b16-4c0a-ae5d-b24808a95e4b",
        "messageType": "RRes",
        "messageVersion": "2.1.0",
        "resultsStatus": "01"
    }
}

module.exports = {
    getRRequest,
    getRResponse
}