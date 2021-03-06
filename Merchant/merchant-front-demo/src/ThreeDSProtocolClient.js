//
// here we get the URL + 3dsServerTransID
// We spawn the iframe (get ID, request wait response and message)
// in the message handler we send the startPayment request
//

// This function uses the notificationMethodURL to fetch the URL of the harvester that will be used later to gather browser data
let getIframeContent = (threeDSServerTransID, threeDSMethodURL, notificationMethodURL) => {
    let rContent = {}
    rContent.threeDSServerTransID = threeDSServerTransID
    rContent.notificationMethodURL = notificationMethodURL

    console.log('Notification URL:');
    console.log(notificationMethodURL);
    
    console.log('3DS Method URL:');
    console.log(threeDSMethodURL);
    
    return fetch(threeDSMethodURL, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(rContent)
    })
    .then((response) => response.json())
    .then((response) => response)
}

// Fetch the 3DSMethod URL from the merchant server
let getThreeDSMethod_URL = (cc_number) => {
    return fetch('http://localhost:4242/merchant/init', {
    method: 'POST',
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ cc_number: cc_number })
    })
    .then((response) => response.json())
    .then((response) => response)
}

// make the request with the CC number to the merchant to get the ACS url of 3ds method
let startThreeDSProtocol= (trans_details) => {
    return getThreeDSMethod_URL(trans_details.cc_number) 
    .then((response) => {
        if (response.status !== 'ok') {
            alert('Server error, your card may not be enrolled to 3DS2')
            return
        } else {
            startAuthentication(response.threeDSServerTransID, trans_details)

            setTimeout(() => getIframeContent(response.threeDSServerTransID, response.threeDSMethodURL, response.notificationMethodURL)
            .then((iframe) => {
                console.log(iframe)
                console.log(iframe.iframeUrl)
                document.getElementById('methodIframe').src = iframe.iframeUrl
            }), 1000)
        }
    })
}

//disable automation concerning the auth Iframe
window.$.featherlight.autoBind = false

// Iframe param object
let defaults = {
    namespace: "featherlight",
    targetAttr: "data-featherlight",
    variant: null,
    resetCss: false,
    background: null,
    openTrigger: "click",
    closeTrigger: "click",
    filter: null,
    root: "body",
    openSpeed: 250,
    closeSpeed: 250,
    closeOnClick: "background",
    closeOnEsc: true,
    closeIcon: "&#10005;",
    loading: "",
    persist: false,
    otherClose: null,
    beforeOpen: () => {},
    beforeContent: () => {},
    beforeClose: () => {},
    afterOpen: () => {},
    afterContent: () => {},
    afterClose: () => {},
    onKeyUp: () => {},
    onResize: () => {},
    type: null,
    contentFilters: ["jquery", "image", "html", "ajax", "text"],
    "jquery/image/html / ajax / text": undefined,
}

// CReq content
let CReq = {
    "threeDSServerTransID": "",
    "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
    "messageType": "CReq",
    "messageVersion": "2.1.0",
}

// will be used to close the auth Iframe later
let savedIframe = {}

// Return the populated object that will be sent to the merchant
let getPaymentData = (threeDSServerTransID, trans_details) => {
    return {
        cc_number: trans_details.cc_number,
        email: trans_details.email,
        cvv: trans_details.cvv,
        cc_date: trans_details.cc_date,
        price: trans_details.price,
        name: trans_details.name,
        postcode: trans_details.postcode,
        city_name: trans_details.city_name,
        phone_number: trans_details.phone_number,
        address: trans_details.address,
        // variable comes from threeDSMethod.js
        threeDSServerTransID: threeDSServerTransID
    }
}

// Send a request to the merchant to initiate a long polling that will be used to notify the completion of the protocol
let sendConfirmationRequest = (acsTransID) => {
    
    let identifier = {}
    identifier.acsTransID = acsTransID
    
    fetch('http://localhost:4242/merchant/requestConfirmation', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(identifier)
    })
        .then((response) => response.json())
        .then((response) => {
            window.setTimeout(function () {
                savedIframe.close();
                if (response.status === 'ok') {
                    window.$('#final_success_pay').show()
                } else {
                    window.$('#final_error_pay').show()
                }
            }, 2400); 
        })
}

// send the CReq and spawn the auth Iframe containing the plaintext HTML response
let sendcReq = (acsURL, acsTransID, threeDSServerTransID) => {

    console.log('In sendCReq, acsURL = ' + acsURL);
    
    CReq.acsTransID = acsTransID
    CReq.threeDSServerTransID = threeDSServerTransID

    fetch(acsURL, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(CReq)
    })
    .then((response) => response.json())
    .then((response) => {
        sendConfirmationRequest(acsTransID)

        // store and load the challenge Iframe
        savedIframe = window.$.featherlight(response.challengeIframeUrl, defaults)
    })
    .catch((error) => alert(error))
}

let sendPaymentData = (paymentData) => {
    return fetch('http://localhost:4242/merchant/pay', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(paymentData)
    })
}

// send the form to the merchant server to initiate the transaction
let startAuthentication = (threeDSServerTransID, trans_details) => {

    let paymentData = getPaymentData(threeDSServerTransID, trans_details)

    // assert that all inputs are filled
    for (var key in paymentData) {
        if (!paymentData[key]) { return (new Promise(function(resolve, reject) { reject("Incomplete payment information") })) }
    }
    
    sendPaymentData(paymentData)
        .then((response) => response.json())
        .then((response) => {
            console.log(response);
            if (response.data.messageType === 'ARes' && response.what === 'Challenge') {
                sendcReq(response.data.acsURL, response.data.acsTransID, response.data.threeDSServerTransID)
            } else if (response.data.messageType === 'ARes' && response.what === 'Authentified') {
                window.$('#final_success_pay').show()   
            }
        })
}

export default startThreeDSProtocol;