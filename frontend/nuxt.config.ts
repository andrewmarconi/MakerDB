import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2026-01-19',
  srcDir: 'app',
  devtools: { enabled: true },
  debug: true,

  future: {
    compatibilityVersion: 4
  },

  app: {
    icon: {
      favicon: 'favicon.png'
    }
  },

  modules: [
    // '@nuxt/a11y',
    '@nuxt/eslint',
    // '@nuxt/hints', // Temporarily disabled - causing hydration reporting errors
    '@nuxt/image',
    '@nuxt/ui',
    '@nuxt/test-utils'
  ],

  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },

  nitro: {
    routeRules: {
      '/db/**': { proxy: 'http://localhost:8000/api/**' }
    }
  }

})