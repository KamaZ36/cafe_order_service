// Прокси на бэкенд кафе: запросы с фронтенда идут на свой же домен (/api/**),
// этот хендлер сам перенаправляет их на API по адресу из runtimeConfig.apiBase
// (читается из NUXT_API_BASE в рантайме, не запекается при сборке — см.
// nuxt.config.ts). Так браузер никогда не обращается к API напрямую — не
// нужен CORS, cookie сессии остаются same-origin.

export default defineEventHandler((event) => {
  const { apiBase } = useRuntimeConfig()
  // event.path включает исходную query-строку — не нужно пересобирать её вручную
  const targetPath = event.path.replace(/^\/api/, '')

  return proxyRequest(event, apiBase + targetPath)
})
