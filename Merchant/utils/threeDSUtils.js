const fetch = require('node-fetch')
const config = require('../config')

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
                if (!appData.checkThreeDSVersion(response.messageVersion)) { return { 'status': 'ko' } }

                console.log("\n3DS SERVER: RECIEVED A PRES:");
                console.log(JSON.stringify(response));
                

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