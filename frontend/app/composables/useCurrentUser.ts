// Текущий авторизованный пользователь (клиент или сотрудник).
// null означает «сессии нет или она анонимная без телефона».

export interface CurrentUser {
  id: string
  phone_number: string | null
  role: 'CUSTOMER' | 'ADMIN' | 'MANAGER'
}

export const useCurrentUser = () => useState<CurrentUser | null>('currentUser', () => null)

export const fetchCurrentUser = async () => {
  const user = useCurrentUser()
  const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

  try {
    user.value = await $fetch<CurrentUser>('/api/users/@me', { headers })
  } catch {
    user.value = null
  }

  return user.value
}
