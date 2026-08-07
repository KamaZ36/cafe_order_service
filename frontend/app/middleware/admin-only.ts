// Более строгая защита поверх admin-auth: сюда пускаем только ADMIN.
// MANAGER — общий персонал (заказы/меню), но не должен видеть чужие
// сессии и платежи, поэтому его отправляем на обычную для него страницу.

export default defineNuxtRouteMiddleware(async () => {
  const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

  let user: CurrentUser | null = null
  try {
    user = await $fetch<CurrentUser>('/api/users/@me', { headers })
  } catch {
    user = null
  }

  if (user?.role !== 'ADMIN') {
    return navigateTo('/admin/orders')
  }
})
