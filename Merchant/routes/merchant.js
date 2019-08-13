const express               = require('express')
const utils                 = require('../utils/utils')
const threeDSUtils          = require('../process/threeDSUtils')
const threeDSComponent      = require('./threeDSComponent')
const clientData            = require('../utils/appData').clientdata
const router                = express.Router()

//handler of the 3dsmethod client side initial request
router.post('/init', (request, response) => {
    
    if (request && request.body) {
        console.log(request.body)
    }

    if (!request.body || !request.body.cc_number) {
        response.json(utils.jsonError('request error or card number not present'))
        return
    }
    console.log('INIT called, waiting for get3DSMethod');
    
    
    threeDSUtils.get3DSMethod(request.body.cc_number)
        .then((formData) => {
            console.log(formData);
            response.json(formData)
        })
        .catch((error) => response.json(error))
})

let checkPaymentData = (body) => {
    if (!body.cc_number || !body.email ||
        !body.cvv || !body.cc_date ||
        !body.price || !body.name ||
        !body.postcode || !body.city_name ||
        !body.phone_number || !body.address ||
        !body.threeDSServerTransID) {
        return {
            'status': 'ko',
            'message': 'missing one or more field'
        }
    }
    body.status = 'ok'
    return body
}


// Payment route that handle and store the payment information
router.post('/pay', (request, response) => {
    
    if (!request || !request.body) {
        response.json({
            'status': 'ko',
            'message': 'Missing cc_number, date, price or cvv field'
        })
        return
    }

    let checkeddData = checkPaymentData(request.body)
    if (checkeddData.status === 'ko') {
        response.json(checkeddData)
        return
    }

    // store the data and response for future use
    clientData.paymentData = checkeddData
    clientData.response = response
    console.log("\nMERCHANT: RECIEVED COMPLETE INITIAL PAYMENT REQUEST\nWaiting for 3DSMethod completion");

})

// Very end of the protocol, notify that everything went well
router.post('/notification', (request, response) => {
    if (!request && !request.body) {
        response.json( utils.jsonError('request failed'))
        console.log('NOTIFICATION: REQUEST FAILED');
        return
    }

    console.log('\nNOTIFICATION: RECIEVED: CRES :');
    console.log(request.body);
    

    // TODO potential fail
    if (request.body.challengeCompletionInd === 'Y') {
        clientData.confirmationObj.response.json({'status': 'ok'})
    } else {
        clientData.confirmationObj.response.json({'status': 'ko'})
    }

    response.json({
        'status': 'ok',
        'message': 'received'
    })
})

// save the response for afterCres confirmation
router.post('/requestConfirmation', (request, response) => {
    if (!request || !request.body) {
        response.json({ 'status': 'ko' })
        return
    }
    let confirmationObj = {}
    confirmationObj.acsTransID = request.body.acsTransID
    confirmationObj.response = response
    clientData.confirmationObj = confirmationObj
    return
})

// Handle the notification request and tell the client that the Iframe challenge can be closed
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
    
    // ici il est probable qu'on doive repondre au client pour confirmer tout TODO

    response.json({
        'status': 'ok',
        'message': 'ok'
    })

})

module.exports = router