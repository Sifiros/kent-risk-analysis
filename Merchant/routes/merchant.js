const express = require('express')
const utils = require('../utils/utils')
const threeDSUtils = require('../utils/threeDSUtils')
const router = express.Router()


//handler the 3dsmethod client side initial request
router.post('/init', (request, response) => {
    if (!request.body || !request.body.cc_number) {
        response.json(utils.jsonError('request error or card number not present'))
        return
    }
    get3DSMethodURL(request.body)
        .then((threeDSMethodInfo) => {
            response.json(threeDSMethodInfo)
            return
        })
})

router.post('/pay', (request, response) => {

})

// Very end of the protocol, notify that everything went well
router.post('/notification', (request, response) => {
    if (!request && !request.body) {
        response.json({
            'status': 'ko',
            'message': 'request failed'
        })
        console.log('NOTIFICATION: REQUEST FAILED');

        return
    }

    console.log('\nNOTIFICATION: RECIEVED: CRES :');

    console.log(request.body);
    
    let userData = search.getUserWithoutAresByTransID(request.body.acsTransID, clients)
    if (userData != null) {
        userData.confirmationResponse.json({ 'status': 'authentified' })
    }

    response.json({
        'status': 'ok',
        'message': 'ok'
    })

})

// save the response for afterCres confirmation
router.post('/requestConfirmation', (request, response) => {
    if (!request || !request.body) {
        response.json({ 'status': 'ko' })
        return
    }
    let userData = {}
    userData.acsTransID = request.body.acsTransID
    userData.confirmationResponse = response
    clients.push(userData)
    return
})