const validator         = require('validator')
const fetch             = require('node-fetch')
const config            = require('../config')
const data              = require('./appData')
const threeDSData       = require('../utils/appData')

let doPost = (url, data, mime = 'application/json') => {
    return fetch(config.origin() + url, {
        method: 'POST',
        headers: {
            'Content-Type': mime
        },
        body: JSON.stringify(data)
    })
    .then((response) => response.json())
    .then((response) => response)
}

let jsonError = (message) => {
    return {
        'status': 'ko',
        'message': message
    }
}

let isCreditCardInRange = (cardNumber) => {
    let pRes = threeDSData.PResponseHeader
    let isCardInRange = false

    if (!pRes || !pRes.cardRangeData) { return false }

    pRes.cardRangeData.forEach(elem => {
        if (cardNumber >= elem.startRange && cardNumber <= elem.endRange) {
            isCardInRange = true
        }

    })
    return isCardInRange
}

let checkThreeDSVersion = (version) => {
    return version === data.threeDSVersion
}

let isTransIDFormatCorrect = (transID) => {
    return validator.isUUID(transID)
}

let isCardValid = (cc_number) => {
    return validator.isCreditCard(cc_number)
}

let isEmailValid = (email) => {
    return validator.isEmail(email)
}

module.exports = {
    jsonError,
    isCreditCardInRange,
    isTransIDFormatCorrect,
    isCardValid,
    isEmailValid,
    doPost,
    checkThreeDSVersion
}