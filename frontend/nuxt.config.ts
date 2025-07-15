// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  future: {
    compatibilityVersion: 4,
  },
  modules: ["@nuxt/eslint", "@nuxt/icon", "@nuxt/image", "@nuxt/test-utils"],
  vite: {
    server: {
      proxy: {
        "/api": {
          target: "http://localhost:8000",
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
        },
        "/media": {
          target: "http://localhost:8000",
          changeOrigin: true,
        },
      },
    },
  },
});
