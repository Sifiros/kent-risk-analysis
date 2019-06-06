const fetch = require('node-fetch')
const config = require('../config')
const utils = require('../utils/utils')
const pMessages = require('../messages/pMessages')
const appData = require('../utils/appData')

let get3DSMethod = (cc_number) => {

    let methodData = {}
    methodData.status = 'ok'
    pRes = appData.PResponseHeader;
    methodData.threeDSMethodURL = null

    if (!cc_number) {
        return new Promise((resolve, reject) => reject(utils.jsonError('cc_number not present to get 3DS method')))
    }

    // select the good method url using the cc_number
    pRes.cardRangeData.forEach(elem => {
        if (cc_number >= elem.startRange && cc_number <= elem.endRange) {
            methodData.threeDSMethodURL = elem.threeDSMethodURL;
        }
    })

    if (methodData.threeDSMethodURL == null) {
        return new Promise((resolve, reject) => reject(utils.jsonError('no methodURL found for this cc_number')))
    }

    methodData.threeDSServerTransID = uuidv1()
    methodData.notificationMethodURL = appData.baseUrl + '/threedscomponent/notificationMethod'
    return new Promise(provide => provide(methodData))
}

let requestThreeDSServerConfig = () => {

    return threeDSSServerData.PResponseHeader = fetch(config.acsAddr() + '/updatepres', {
        method: 'POST',
        credentials: 'none',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(pMessages.getPRequest())
    })
        .then((response) => response.json())
        .then((response) => {
            if (response) {
                if (!utils.checkThreeDSVersion(response.messageVersion)) { return utils.jsonError('Version not compatible') }

                console.log("\n3DS SERVER: RECIEVED A PRES:");
                console.log(response);

                if (!response.cardRangeData) { return utils.jsonError('Missing cardRangeDara in PRES') }
                if (!response.cardRangeData[0].threeDSMethodURL) { return utils.jsonError('Missing cardRangeData in Pres') }
                threeDSSServerData.PResponseHeader = response
                return response
            }
            return { 'status': 'ko' }
        })
}

module.exports = {
    requestThreeDSServerConfig,
    get3DSMethod
}