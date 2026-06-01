import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import router from './router/index.js'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'archiveLight',
    themes: {
      archiveLight: {
        dark: false,
        colors: {
          background: '#cccccc',
          surface:    '#ffffff',
          primary:    '#3a3a6a',
          secondary:  '#1a5a96',
          error:      '#c62828',
          success:    '#2e7d32',
          warning:    '#e65100',
          info:       '#1565c0',
        },
      },
    },
  },
})

createApp(App).use(vuetify).use(router).mount('#app')
