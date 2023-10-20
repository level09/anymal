/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from './vuetify'
import router from '../router'
import {pinia} from "./pinia";
import WebsocketPlugin from "./websocket";
import Websocket from "./websocket";

export function registerPlugins(app) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
    .use(WebsocketPlugin)

}



