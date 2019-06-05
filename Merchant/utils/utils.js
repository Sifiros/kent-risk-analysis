const validator = require('validator')

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
    isEmailValid
}