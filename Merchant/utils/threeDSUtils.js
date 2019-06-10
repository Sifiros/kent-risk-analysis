const fetch = require('node-fetch')
const config = require('../config')
const utils = require('./utils')
const pMessages = require('../messages/pMessages')
const appData = require('../utils/appData')

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

                if (!response.cardRangeData) { // TODO check and log where does it pass
                    appData.data.isCarRanges = false
                    return { 'status': 'ko' }
                }
                threeDSSServerData.PResponseHeader = response
                return response
            }
            return { 'status': 'ko' }
        })
}

module.exports = {
    requestThreeDSServerConfig
}