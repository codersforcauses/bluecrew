import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { mdi } from 'vuetify/iconsets/mdi'

import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Object to store colour theme hexcodes
const colourTheme = {
  colors: {
    primaryBlue: '#193855',
    lightBlue: '#3FBEE0',
    creamWhite: '#E9DAC4',
    primaryGrey: '#4F4F4F',
    primaryBrown: '#EDE1D0',
    primaryWhite: '#FFFFFF',
    primaryGreen: '#007D85',
  },
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'colourTheme',
    themes: {
      colourTheme,
    },
  },
  icons: {
    defaultSet: 'mdi',
    sets: {
      mdi,
    },
  },
})

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
