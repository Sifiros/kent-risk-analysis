function isCanvasSupported() {
    var elem = document.createElement('canvas');
    return !!(elem.getContext && elem.getContext('2d'));                
}
function getCanvasFingerprint() {
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');
  // https://www.browserleaks.com/canvas#how-does-it-work
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

let info = {}
info.threeDSServerTransID = "#!3DS_TRANS_ID!#"
info.notificationMethodURL = "#!NOTIFICATION_METHOD_URL!#"

let sendFingerPrintToACS = () => {
    return fetch('http://localhost:4242/merchant/toto', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(info)
        }).then((response) => response.json())
}

let getAllInfo = (uaparser, deployJava) => {
    info.screenSize = screen.width + ":" + screen.height
    info.innerSize = window.innerWidth + ":" + window.innerHeight
    info.outerSize = window.outerWidth + ":" + window.outerHeight
    info.doNotTrack = navigator.doNotTrack

    info.uaInfo = uaparser.getResult()

    info.uaInfo.browser.appName = navigator.appName

    info.plugins = []
    let plugins = navigator.plugins
    for (i = 0; i < plugins.length; i++) {
        info.plugins.push(plugins[i].name)
    }
    info.timezoneOffset = new Date().getTimezoneOffset()

    info.javaVersions = deployJava.getJREs()
    info.colorDepth = screen.colorDepth
    if (!isCanvasSupported()) {
        info.canvas = false
    } else {
        info.canvas = getCanvasFingerprint()
    }

    info.position = {}
    return new Promise(resolve => {
        navigator.geolocation.getCurrentPosition((position) => {
            info.position.latitude = position.coords.latitude
            info.position.longitude = position.coords.longitude
            fetch("http://api.geonames.org/countryCodeJSON?lat=" + info.position.latitude + "&lng=" + info.position.longitude + "&username=riskassessdemo")
            .then(response => {return response.json()})
            .then(body => {
                info.position.countryCode = body.countryCode
                resolve(info)
            })
        }, (positionError) => {
            console.log(positionError)
            resolve(info)
        })
    })
}
