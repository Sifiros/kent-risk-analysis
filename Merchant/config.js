let port = () => {
    return process.env.SERVER_PORT || 4242
}

let serverIp  = () => {
    return process.env.SERVER_IP || 'localhost'
}

let origin = () => {
    return process.env.PUBLIC_URL || "http://localhost:4242"
}

let internalNetworkUrl = () => {
    return process.env.INTERNAL_NETWORK_URL || "http://merchant:4242"
}

let acsAddr = () => {
    return process.env.ACS_PUBLIC_URL || "http://localhost:8484"
}

module.exports = {
    port,
    serverIp,
    origin,
    internalNetworkUrl,
    acsAddr
}