const fetch         = require('node-fetch')
const express       = require('express')
const clientData    = require('../utils/appData').clientdata
const aRequests     = require('../messages/aRequests')
const router        = express.Router()

let startAuthentication = (aReq) => {

    return threeDSSServerData.AResponseHeader = fetch(appData.baseUrl + '/ds/authrequest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(aReq)
    })
}

let getAresStatus = (response) => {

    if (!appData.checkThreeDSVersion(response.messageVersion)) { return 'Bad Version' }
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
                    threeDSUtils.respondChallenge(response, oldResponse, authStatus);
                    break;
                case 'Authentified':
                    threeDSUtils.respondAuthentified(response, oldResponse, authStatus); // OK
                    break;
                case 'Attempt':
                    threeDSUtils.respondAttempt(response, oldResponse, authStatus); // Tentative d'auth, on connais pas le résultat mais ça passe il est auth
                    break;
                case 'NonAuth': // KO
                    threeDSUtils.respondNop(response, oldResponse, authStatus);
                    break;
                default:
                    threeDSUtils.respondWithError(response, oldResponse, authStatus);
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
    if (clientData.methodStatus == 'ok') {
        updatedAreq.threeDSCompInd = 'Y'
    }

    console.log("\n3DS SERVER: RECIEVED INITIAL PAYMENT REQUEST FROM MERCHANT");

    if (updatedAreq.status === 'ko') { response.json(updatedAreq); return }
    if (!utils.isCreditCardInRange(request.body.cc_number)) { response.json(utils.jsonError('Credit card number is not in 3DS2 range')); return }
    if (!appData.checkThreeDSVersion(updatedAreq.messageVersion)) { response.json(utils.jsonError('Not compatible version')); return }

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
    startTransaction(clientData, response)

    response.json({ 'status': 'ok' })
})