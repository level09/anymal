// websocket-plugin.js
import ReconnectingWebSocket from 'reconnecting-websocket';

const websocket = new ReconnectingWebSocket(`ws://localhost:8000/ws`, [], {
  connectionTimeout: 2000,
  maxRetries: 15,
  debug: true
});

const WebsocketPlugin = {
  install(app) {
    // Attach the websocket instance to the global properties
    // so that it's available to all components as this.$websocket
    app.config.globalProperties.$websocket = websocket;
  }
};

export default WebsocketPlugin;
