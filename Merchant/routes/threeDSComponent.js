const fetch         = require('node-fetch')
const express       = require('express')
const config        = require('../config')
const utils         = require('../utils/utils')
const clientData    = require('../utils/appData').clientdata
const threeDSUtils  = require('../process/threeDSUtils')
const aRequests     = require('../messages/aRequests')
const rMessages     = require('../messages/pMessages')
const eMessages     = require('../messages/protocolError')
const router        = express.Router()

let startAuthentication = (aReq) => {

    return threeDSSServerData.AResponseHeader = fetch(config.acsAddr + '/authrequest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(aReq)
    })
}

let getAresStatus = (response) => {

    if (!utils.checkThreeDSVersion(response.messageVersion)) { return 'Bad Version' }
    if (response.messageType == 'Erro') { return 'Error' }
    else if (response.transStatus == 'C') { return 'Challenge' }
    else if (response.transStatus == 'Y') { return 'Authentified' }
    else if (response.transStatus == 'C') { return 'Attempt' }
    else if (response.transStatus == 'N') { return 'NonAuth' }
    else { return 'Error' }
}

let doStartAuthentication = (updatedAreq, oldResponse) => {

    startAuthentication(updatedAreq)
        .then((response) => response.json())
        .then((response) => {

            console.log("\n3DS SERVER: RECIEVED ARES");
            console.log(response);

            if (!response.threeDSServerTransID) {
                response.threeDSServerTransID = uuidv1()
            }

            let authStatus = getAresStatus(response)
            switch (authStatus) {
                case 'Bad Version':
                    threeDSUtils.respondWithError('Bad version', oldResponse, authStatus)
                    break;
                case 'Challenge':
                    threeDSUtils.aResponseToBrowser(response, oldResponse, authStatus);
                    break;
                case 'Authentified':
                    threeDSUtils.aResponseToBrowser(response, oldResponse, authStatus); // OK
                    break;
                case 'Attempt':
                    threeDSUtils.aResponseToBrowser(response, oldResponse, authStatus); // Tentative d'auth, on connais pas le résultat mais ça passe il est auth
                    break;
                case 'NonAuth': // KO
                    threeDSUtils.aResponseToBrowser(response, oldResponse, authStatus);
                    break;
                default:
                    threeDSUtils.aResponseToBrowser(response, oldResponse, authStatus);
                    break;
            }
        })
        .catch((error) => console.log('threeDSServer post to ds/authrequest error: ' + error))
}

// update AReq with merchant data
let getUpdatedAreq = (body, transID) => {
    if (!body.cc_number || !body.email ||
        !body.cvv || !body.cc_date ||
        !body.price || !body.name ||
        !body.postcode || !body.city_name ||
        !body.phone_number || !body.address) {
        return (utils.jsonError('Missing a field in request'))
    }

    let aReq = aRequests.getARequest()
    aReq.shipAddrCity = body.city_name
    aReq.email = body.email
    aReq.shipAddrPostCode = body.postcode
    aReq.cardExpiryDate = body.cc_date
    aReq.cardholderName = body.name
    aReq.threeDSServerTransID = transID
    return aReq
}

// handle the merchant request starting the protocole
let startTransaction = (clientData, response) => {

    if (!clientData.paymentData) {
        response.json(utils.jsonError('Missing payment Data for this client'))
        return
    }

    let updatedAreq = getUpdatedAreq(clientData.paymentData, clientData.threeDSServerTransID)

    if (updatedAreq.status === 'ko') { response.json(updatedAreq); return }
    if (!utils.isCreditCardInRange(request.body.cc_number)) { response.json(utils.jsonError('Credit card number is not in 3DS2 range')); return }
    if (!utils.checkThreeDSVersion(updatedAreq.messageVersion)) { response.json(utils.jsonError('Not compatible version')); return }

    if (clientData.methodStatus == 'ok') {
        updatedAreq.threeDSCompInd = 'Y'
    }

    console.log("\n3DS SERVER: RECIEVED INITIAL PAYMENT REQUEST FROM MERCHANT");

    doStartAuthentication(updatedAreq, response)
}

//
// Handle the 3DS Method Notification request and set methodStatus to 'Y' if OK
//
router.post('/notificationMethod', (request, response) => {
    if (!request || !request.body || !request.body.threeDSServerTransID ||
        !request.body.methodStatus) {
        response.json({ 'status': 'ko' })
        return
    }

    clientData.isMethodComplete = request.body.methodStatus
    clientData.threeDSServerTransID = request.body.threeDSServerTransID
    startTransaction(clientData, clientData.response)

    response.json({ 'status': 'ok' })
})

//
// Handle the RREq and return a RREs
//
router.post('/resrequest', (request, response) => {

    let Rres = rMessages.getRResponse()
    let eMessage = eMessages.getGenericFormatError()
    eMessage.errorMessageType = 'RReq'

    if (request && request.body) {
        if (!utils.checkThreeDSVersion(request.body.messageVersion)) {
            eMessage.errorDescription = 'Bad version'
            response.json(eMessage)
            return
        } else if (request.body.messageType !== 'RReq') {
            response.json(utils.jsonError('Wrong messageType'))
            return
        }

        console.log("\n3DS SERVER: RECIEVED RREQ, CHECKING AND SENDING BACK RRES:");
        console.log(request.body);

        (request.body.transStatus === 'Y' || request.body.transStatus === 'A') ? Rres.resultsStatus = '00' : Rres.resultsStatus = '01'
        Rres.threeDSServerTransID = request.body.threeDSServerTransID

        response.json(Rres)
        return
    }

    eMessage.errorDescription = 'Request failed, missing body'
    response.json(eMessage)
})

router.post('/challresponse', (request, response) => {

    let eMessage = eMessages.getGenericFormatError()
    eMessage.errorMessageType = "Cres"

    if (!request && !request.body) {
        eMessage.errorDescription = "Body not found / request failed"
        response.json(eMessage)
        return
    } else if (!utils.checkThreeDSVersion(request.body.messageVersion)) {
        eMessage.errorDescription = "Not supported version"
        response.json(eMessage)
        return
    }

    console.log("\nCRES RECIEVED BY 3DSSERVER\nTRANSACTION COMPLETE");

    response.json({'status': 'ok'})
})

module.exports = router