// Конфигурация Nuxt: Tailwind-модуль, Google Fonts и мета-теги страницы
export default defineNuxtConfig({
  compatibilityDate: '2026-07-01',

  modules: ['@nuxtjs/tailwindcss'],

  // Модуль по умолчанию ищет assets/css/tailwind.css от корня проекта, а не
  // от app/ (srcDir в Nuxt 4). Без явного пути он тихо не находит файл и
  // подставляет пустой дефолтный CSS — весь кастомный @layer components
  // из tailwind.css в сборку не попадает.
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css'
  },

  // Адрес бэкенда для server/routes/api/[...].ts. Через runtimeConfig, а не
  // через routeRules.proxy — тот читает process.env один раз при сборке
  // (bun run build) и намертво запекает значение в собранный образ, так что
  // NUXT_API_BASE из docker-compose на уже собранный контейнер не повлияет.
  // runtimeConfig, наоборот, читается при старте сервера — один образ можно
  // деплоить с разным NUXT_API_BASE без пересборки.
  runtimeConfig: {
    apiBase: process.env.NUXT_API_BASE || 'http://localhost:8000'
  },

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
