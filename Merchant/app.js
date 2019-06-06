const express       = require('express')
const bodyParser    = require('body-parser')
const path          = require('path')
const config        = require('./config')

// const https = require('https')

const merchantroute = require('./routes/merchant')
const threeDSroute = require('./routes/threeDSComponent')
const threeDSUtils = require('./process/threeDSUtils')

const app = express()
const port = config.port()

app.use(bodyParser.json())
app.use(express.static(path.join(__dirname, 'static')));

app.use('/merchant', merchantroute)
app.use('/threeDSComponent', threedscomponent)

app.listen(port)

// call at server application startup and every 1h (3600000 millisecond)
setInterval(threeDSUtils.requestThreeDSServerConfig, 3600000)

status = threeDSUtils.requestThreeDSServerConfig()
if (status.status && status.status === 'ko') {
    console.log("server could not fetch Pres");
}

console.log(`Started app on port ${port}`);

module.exports = app;