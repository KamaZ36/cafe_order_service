// Конфигурация Nuxt: Tailwind-модуль, Google Fonts и мета-теги страницы
export default defineNuxtConfig({
  compatibilityDate: '2026-07-01',

  modules: ['@nuxtjs/tailwindcss'],

  app: {
    head: {
      htmlAttrs: { lang: 'ru' },
      title: 'Мясная деревня — кафе, магазин, своё производство',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Мясная деревня — собственное производство мясных деликатесов полного цикла, кафе и магазин. Натуральные продукты без добавок.'
        }
      ],
      link: [
        // Подключение Google Fonts: Cormorant Garamond (заголовки) и Albert Sans (текст)
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Albert+Sans:wght@300;400;500;600&display=swap'
        }
      ]
    }
  }
})
