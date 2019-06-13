let threeDSServerTransID_global = ""

// here we get the URL + 3dsServerTransID
// We spawn the iframe (get ID, request wait response and message)
// in the message handler we send the startPayment request

$(document).ready(() => {

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

    let getThreeDSMethod_URL = () => {
        return fetch('http://localhost:4242/merchant/init', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ cc_number: $('#cc-number-input').val() })
        })
            .then((response) => response.json())
            .then((response) => response)
    }

    // make the request with the CC number to the merchant to get the ACS url of 3ds method
    $('#button-iframe').click(() => {
        getThreeDSMethod_URL()
            .then((response) => {
                if (response.status !== 'ok') {
                    alert('Server error, your card may not be enrolled to 3DS2')
                    return
                } else {
                    threeDSServerTransID_global = response.threeDSServerTransID
                    startAuthentication(response.threeDSServerTransID)
                    getIframeContent(response.threeDSServerTransID, response.threeDSMethodURL, response.notificationMethodURL)
                        .then((htmlContent) => {
                            
                            document.getElementById('methodIframe').contentDocument.write(htmlContent)
                        })
                }
            })
    })
});
