import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Vuetifyq
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Object to store colour theme hexcodes
const colourTheme = {
  colors: {
    primary: '#193855',
    titles: '#D12974',
    accent: '#3FBEE0',
    containers: '#E9DAC4',
    text: '#4F4F4F',
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
})

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
