const express = require('express')
const bodyParser = require('body-parser')
const path = require('path')
const config = require('./config')

// const https = require('https')

const merchantroute = require('./routes/merchant')
const threeDSroute = require('./routes/threeDSComponent')
const threeDSUtils = require('./utils/threeDSUtils')

const app = express()
const port = config.port()

app.use(bodyParser.json())
app.use(express.static(path.join(__dirname, 'static')));

app.use('/merchant', merchantroute)
app.use('/threedsserver', threeDSroute)

app.listen(port)

// call at server application startup and every 1h (3600000 millisecond)
setInterval(threeDSUtils.requestThreeDSServerConfig, 3600000)

threeDSUtils.requestThreeDSServerConfig()

console.log(`Started app on port ${port}`);

module.exports = app;