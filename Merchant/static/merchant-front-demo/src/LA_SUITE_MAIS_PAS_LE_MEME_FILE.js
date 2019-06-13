//disable automation concerning the auth Iframe
$.featherlight.autoBind = false

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
    beforeOpen: $.noop,
    beforeContent: $.noop,
    beforeClose: $.noop,
    afterOpen: $.noop,
    afterContent: $.noop,
    afterClose: $.noop,
    onKeyUp: $.noop,
    onResize: $.noop,
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

let getPaymentData = () => {
    return {
        cc_number: $('#cc-number-input').val(),
        email: $('#email-input').val(),
        cvv: $('#cvv-input').val(),
        cc_date: $('#date-input').val(),
        price: '90',
        name: $('#name-input').val(),
        postcode: $('#post-code-input').val(),
        city_name: $('#city-input').val(),
        phone_number: $('#tel-input').val(),
        address: $('#address-input').val(),
        challengeOption: $('#challenge-input').val(),
        // variable comes from threeDSMethod.js
        threeDSServerTransID: threeDSServerTransID_global
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
            savedIframe = $.featherlight(response, defaults)
        })
        .catch((error) => alert(error))
}

// send the form to the merchant server to initiate the transaction
let startAuthentication = (threeDSServerTransID) => {

    let paymentData = getPaymentData()

    // assert that all inputs are filled
    $.each(paymentData, (i, value) => {
        if (!value) { return false }
    })

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

export default startAuthentication;

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
