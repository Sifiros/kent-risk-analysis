let port = () => {
    return 4242
}

let origin = () => {
    return "http://localhost:4242"
}

let acsAddr = () => {
    return "http://localhost:8484"
}

module.exports = {
    port,
    origin,
    acsAddr
}