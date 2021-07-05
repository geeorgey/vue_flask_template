import Vue from 'vue'

import Vuetify from 'vuetify/lib'
import store from '../store'
import ja from '@/locale/ja'
import en from '@/locale/en'
Vue.use(Vuetify)

export default new Vuetify({
  lang: {
    locales: { ja, en },
    current: 'ja'
  },
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
      light: {
        primary: store.getters.getThemeColor,
        secondary: '#424242',
        accent: '#82B1FF',
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FFC107',
      },
    },
  },
})
