document.addEventListener('alpine:init', () => {

    Alpine.data('websockets', () => ({
        connectWebSocket() {
            const ws = new WebSocket(WS)

            ws.addEventListener('open', (event) => {
                console.log("Connected to the ws server")
            })

            return ws
        },

        websocket: null,

        init() {
            this.websocket = this.connectWebSocket()
        }

    }))

})
