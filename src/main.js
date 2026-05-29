import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import router from './router/index.js'

// Читаем сохранённую тему из localStorage (по умолчанию тёмная)
const savedTheme = localStorage.getItem('theme') || 'dark'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: savedTheme,
    themes: {
      dark: {
        dark: true,
        colors: {
          background: '#08060f',
          surface:    '#110e24',
          primary:    '#6d28d9',
          secondary:  '#a78bfa',
          error:      '#ef4444',
          success:    '#22c55e',
        },
      },
      light: {
        dark: false,
        colors: {
          background: '#f5f3ff',
          surface:    '#ffffff',
          primary:    '#6d28d9',
          secondary:  '#7c3aed',
          error:      '#ef4444',
          success:    '#16a34a',
        },
      },
    },
  },
})

createApp(App).use(vuetify).use(router).mount('#app')
