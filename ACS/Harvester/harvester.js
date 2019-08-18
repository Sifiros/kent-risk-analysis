function isCanvasSupported() {
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));                
}

function getCanvasFingerprint() {
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');                                    // https://www.browserleaks.com/canvas#how-does-it-work
  var txt = 'CANVAS_FINGERPRINT';
  ctx.textBaseline = "top";
  ctx.font = "14px 'Arial'";
  ctx.textBaseline = "alphabetic";
  ctx.fillStyle = "#f60";
  ctx.fillRect(125,1,62,20);
  ctx.fillStyle = "#069";
  ctx.fillText(txt, 2, 15);
  ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
  ctx.fillText(txt, 4, 17);
  return canvas.toDataURL();
}

var getUrlParameter = function getUrlParameter(sParam) {                // take the parameter's name, return its value if present, otherwise return undefined
    let sPageURL = window.location.search.substring(1)
    let sURLVariables = sPageURL.split('&')
    let sParameterName
    let i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};
 

let info = {}
info.threeDSServerTransID = decodeURIComponent(getUrlParameter('trID'))

window.sendFingerPrintToACS = () => {
    return fetch(decodeURIComponent(getUrlParameter('posturl')), {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(info)
        }).then((response) => response.json())
}

let getAllInfo = (uaparser) => {
    info.screenSize = screen.width + ":" + screen.height            // monitor's resolution
    info.innerSize = window.innerWidth + ":" + window.innerHeight   // size of the part of the window where the website is displayed
    info.outerSize = window.outerWidth + ":" + window.outerHeight   // total size of the window (including navigation bar, borders, etc)
    if (!navigator.doNotTrack) {
        info.doNotTrack = 0
    } else {
        info.doNotTrack = 1
    }

    info.uaInfo = uaparser.getResult()                              // using a library returning the parsed user agent, makes for easier use of its info

    info.uaInfo.browser.appName = navigator.appName

    info.plugins = []
    let plugins = navigator.plugins                                 // list of plugins installed on the browser. Does not include extensions. 
    for (i = 0; i < plugins.length; i++) {
        info.plugins.push(plugins[i].name)
    }
    info.timezoneOffset = new Date().getTimezoneOffset()            // in minutes, negative values for positive UTC timezones

    info.colorDepth = screen.colorDepth
    try {                                                           // getting Canvas if possible
        if (!isCanvasSupported()) {
            info.canvas = false
        } else {
            info.canvas = getCanvasFingerprint()
        }
    } catch (error) {
        console.log('An exception occured')
        console.log(error)
    }

    info.position = {}
    return new Promise(resolve => {                                 // country request is asynchronous so we return a promise
        navigator.geolocation.getCurrentPosition((position) => {    // this will trigger the browser's geolocation permission. If refused, go to error
            info.position.latitude = position.coords.latitude
            info.position.longitude = position.coords.longitude
            fetch("http://api.geonames.org/countryCodeJSON?lat=" + info.position.latitude + "&lng=" + info.position.longitude + "&username=riskassessdemo")
            .then(response => {return response.json()})
            .then(body => {
                info.position.countryCode = body.countryCode        // we get the country based on the geolocation
                resolve(info)
            })
        }, (positionError) => {
            console.log(positionError)
            resolve(info)
        })
    })
}
