// here we get the URL + 3dsServerTransID
// We spawn the iframe (get ID, request wait response and message)
// in the message handler we send the startPayment request

let getIframeContent = (threeDSServerTransID, threeDSMethodURL, notificationMethodURL) => {
    let rContent = {}
    rContent.threeDSServerTransID = threeDSServerTransID
    rContent.notificationMethodURL = notificationMethodURL
    
    return fetch(threeDSMethodURL, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(rContent)
    })
    .then((response) => response.text())
    .then((response) => response)
}

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
    getThreeDSMethod_URL() 
    .then((response) => {
        if (response.status !== 'ok') {
            alert('Server error, your card may not be enrolled to 3DS2')
            return
        } else {
            startAuthentication(response.threeDSServerTransID, trans_details)
            getIframeContent(response.threeDSServerTransID, response.threeDSMethodURL, response.notificationMethodURL)
            .then((htmlContent) => {
                document.getElementById('methodIframe').contentDocument.write(htmlContent)
            })
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

// CReq content hardcoded
let CReq = {
    "threeDSServerTransID": "",
    "acsTransID": "d7c1ee99-9478-44a6-b1f2-391e29c6b340",
    "messageType": "CReq",
    "messageVersion": "2.1.0",
}

// will be used to close the auth Iframe later
let savedIframe = {}

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

let sendConfirmationRequest = (acsTransID) => {
    
    let identifier = {}
    identifier.acsTransID = acsTransID
    
    fetch('http://localhost:4242/merchant/requestConfirmation', {
    method: 'POST',
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(identifier)
    })
    .then((response) => response.json())
    .then((response) => {
        if (response.status === 'authentified') {
            window.setTimeout(function () { savedIframe.close(); }, 2400);
        }
    })
}

// send the CReq and spawn the auth Iframe containing the plaintext HTML response
let sendcReq = (acsURL, acsTransID, threeDSServerTransID) => {
    
    CReq.acsTransID = acsTransID
    CReq.threeDSServerTransID = threeDSServerTransID
    fetch(acsURL, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(CReq)
    })
    .then((response) => response.text())
    .then((response) => {
        sendConfirmationRequest(acsTransID)
        savedIframe = window.$.featherlight(response, defaults)
    })
    .catch((error) => alert(error))
}

// send the form to the merchant server to initiate the transaction
let startAuthentication = (threeDSServerTransID, trans_details) => {
    
    let paymentData = getPaymentData(threeDSServerTransID, trans_details)
    
    // assert that all inputs are filled
    for (var key in paymentData) {
        if (!paymentData[key]) { return false }
    }
    
    fetch('http://localhost:4242/merchant/pay', {
    method: 'POST',
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(paymentData)
})
.then((response) => response.json())
.then((response) => {
    console.log(response);
    if (response.data.messageType == 'ARes' && response.what == 'Challenge') {
        sendcReq(response.data.acsURL, response.data.acsTransID, response.data.threeDSServerTransID)
    } else {
        if (response.data.messageType === 'ARes') { alert('TODO'); return }
        alert('ERROR')
    }
})
}

export default startThreeDSProtocol;

// Recieve message from Auth Iframe and 3DSMethod_URL Iframe
// window.addEventListener("message", receiveMessage, false);

// function receiveMessage(event) {

//     let NOTIFICATION_URL = ""

//     if (event.origin !== "http://localhost:9094") {
//         return;
//     }

//     if (event.data) {
//         if (event.data.messageType == 'CRes') {  // classic auth case (CReq/Cres)
//             NOTIFICATION_URL = event.data.notificationURL

//             fetch(NOTIFICATION_URL, {
//                 method: 'POST',
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify(event.data)
//             })
//                 .then((response) => response.json())
//                 .then((response) => {
//                     console.log(response)
//                     window.setTimeout(function () { savedIframe.close(); }, 2400);

//                 })
//                 .catch((error) => console.log(error))
//         }
//         // else if (event.data.status) {  // 3DS method case
//         //     console.log("starting authentication");

//         //     startAuthentication()
//         // }
//     }


// }