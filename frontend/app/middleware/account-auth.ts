// Личный кабинет доступен только с подтверждённым телефоном — анонимную
// сессию без телефона отправляем на главную (там есть кнопка «Войти»).

export default defineNuxtRouteMiddleware(async () => {
  const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

  const user = useCurrentUser()
  try {
    user.value = await $fetch('/api/users/@me', { headers })
  } catch {
    user.value = null
  }

  if (!user.value?.phone_number) {
    return navigateTo('/')
  }
})
