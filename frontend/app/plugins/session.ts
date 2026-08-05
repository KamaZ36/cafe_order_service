// Подгружает текущего пользователя и корзину один раз при старте приложения
// (на SSR — с прокидыванием cookie запроса). useAsyncData с фиксированным
// ключом гарантирует, что при гидратации на клиенте повторного запроса не будет —
// данные приедут в пейлоаде с сервера.

export default defineNuxtPlugin(async () => {
  await useAsyncData('bootstrap-session', async () => {
    await Promise.allSettled([fetchCurrentUser(), fetchCart()])
    return true
  })
})
