let getAllInfo = (uaparser, deployJava) => {
    let info = {}

    info.screenSize = screen.width + ":" + screen.height                //end format : "width:height"
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
    let plugins = navigator.plugins                                     //or empty array if no detected plugin
    if (plugins.length) {
        plugins.forEach(plugin => {
            info.plugins.push(plugin.name)
        });
    }
    info.timezoneOffset = new Date().getTimezoneOffset()                //end format : plain value (can be negative)

    info.position = {}                                                  //end format : {latitude: value, longitude: value, countryCode: "code"}
    /*navigator.geolocation.getCurrentPosition((position) => {            //or an empty object if location refused
        info.position.latitude = position.coords.latitude
        info.position.longitude = position.coords.longitude
        fetch("http://api.geonames.org/countryCodeJSON?lat=" + info.position.latitude + "&lng=" + info.position.longitude + "&username=demo")
        .then(response => {return response.json()}).then(body => {
            info.position.countryCode = body.countryCode
            console.log(info)
        })
    }, (positionError) => {
        console.log(info)
    })*/

    fetch("http://10.15.190.247:9094/webauthn/test_alex", {method: 'POST'})
        .then(response =>{ return response.json()}).then(body => {
            info.accepted_mime = body['accept'] || ""                       //end format : "type/subtype(;q=poids),type/subtype(;q=poids)"      //can be a simple "*/*"
            info.accepted_encoding = body['accept-encoding'] || ""          //end format : "encoding, encoding, encoding"
            info.accepted_languages = body['accept-language'] || ""         //end format : "langue(-locale)(;q=poids),langue(-locale)(;q=poids)"
            info.accepted_charset = body['accept-charset'] || ""            //end format : "charset(;q=poids),charset(;q=poids)"                //will usually be empty
            console.log(info)
        })
    info.javaVersion = deployJava.getJREs()
}