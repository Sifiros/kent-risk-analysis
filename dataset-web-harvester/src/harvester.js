import UaParser from 'ua-parser-js'

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

let getAllInfo = () => {
    let uaparser = new UaParser()
    let info = {}
    
    info.screenSize = window.screen.width + ":" + window.screen.height                //end format : "width:height"
    info.innerSize = window.innerWidth + ":" + window.innerHeight       //end format : "width:height"
    info.outerSize = window.outerWidth + ":" + window.outerHeight       //end format : "width:height"
    info.doNotTrack = navigator.doNotTrack                              //end format : "1" ou "0"

    info.uaInfo = uaparser.getResult()
                                                                        /*end format :  //caution : fields can be undefined (device fields were undefined for me)
                                                                        {
                                                                            ua: "",
                                                                            browser: {
                                                                                appName: "",
                                                                                name: "",
                                                                                version: ""
                                                                            },
                                                                            engine: {
                                                                                name: "",
                                                                                version: ""
                                                                            },
                                                                            os: {
                                                                                name: "",
                                                                                version: ""
                                                                            },
                                                                            device: {
                                                                                model: "",
                                                                                type: "",
                                                                                vendor: ""
                                                                            },
                                                                            cpu: {
                                                                                architecture: ""
                                                                            }
                                                                        }*/
    info.uaInfo.browser.appName = navigator.appName

    info.plugins = []                                                   //end format : ["name1", "name2", "name3"]
    let plugins = navigator.plugins                                  //or empty array if no detected plugin
    for (var i = 0; i < plugins.length; i++) {
        info.plugins.push(plugins[i].name)
    }
    info.timezoneOffset = new Date().getTimezoneOffset()                //end format : plain value (can be negative)

    //info.javaVersions = deployJava.getJREs()
    info.colorDepth = window.screen.colorDepth
    if (!isCanvasSupported()) {
        info.canvas = false
    } else {
        info.canvas = getCanvasFingerprint()
    }

    info.position = {}                                                  //end format : {latitude: value, longitude: value, countryCode: "code"}
    return new Promise(resolve => {
        navigator.geolocation.getCurrentPosition((position) => {            //or an empty object if location refused
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

export default getAllInfo;