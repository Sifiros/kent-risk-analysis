// This example contains data before encryption as a JWE.
// APP

let getCRequest = () => {
    return {
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
        "messageType": "CReq",
        "messageVersion": "2.1.0",
        "sdkTransID": "b2385523-a66c-4907-ac3c-91848e8c0067",
        "sdkCounterStoA": "001"
    }
}

// This example contains data before encryption as a JWE.
// APP

let getCResponse = () => {
    return {
        "threeDSServerTransID": "8a880dc0-d2d2-4067-bcb1-b08d1690b26e",
        "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
        "challengeAddInfo": "Additional information to be shown.",
        "challengeCompletionInd": "N",
        "challengeInfoHeader": "Header information",
        "challengeInfoLabel": "One-time-password",
        "challengeInfoText": "Please enter the received one-time-password",
        "challengeInfoTextIndicator": "N",
        "expandInfoLabel": "Additional instructions",
        "expandInfoText": "The issuer will send you via SMS a one-time password.Please enter the value in the designated input field above and press continueto complete the 3-D Secure authentication process.",
        "issuerImage": {
            "medium": "https://acs.com/medium_image.svg",
            "high": "https://acs.com/high_image.svg",
            "extraHigh": "https://acs.com/extraHigh_image.svg"
        },
        "messageType": "CRes",
        "messageVersion": "2.1.0",
        "psImage": {
            "medium": "https://ds.com/medium_image.svg",
            "high": "https://ds.com/high_image.svg",
            "extraHigh": "https://ds.com/extraHigh_image.svg"
        },
        "resendInformationLabel": "Send new One-time-password",
        "submitAuthenticationLabel": "Continue",
        "whyInfoLabel": "Why using 3-D Secure?",
        "whyInfoText": "Some explanation about why using 3-D Secure is an excellent idea as part of an online payment transaction",
        "acsCounterAtoS": "001"
    }
}

module.exports = {
    getCRequest,
    getCResponse
}