// Защита раздела /admin: пускает только сессию с ролью ADMIN или MANAGER.
// На сервере (SSR) нужно вручную прокинуть cookie входящего запроса в свой
// же fetch к /api/users/@me — Nuxt не делает это автоматически.

export default defineNuxtRouteMiddleware(async (to) => {
  const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

  let user: CurrentUser | null = null
  try {
    user = await $fetch<CurrentUser>('/api/users/@me', { headers })
  } catch {
    user = null
  }

  const isStaff = user?.role === 'ADMIN' || user?.role === 'MANAGER'

  if (to.path === '/admin/login') {
    if (isStaff) {
      return navigateTo(user?.role === 'ADMIN' ? '/admin/categories' : '/admin/orders')
    }
    return
  }

  if (!isStaff) {
    return navigateTo('/admin/login')
  }
})
