<script setup lang="ts">
const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: currentUser } = await useFetch<CurrentUser>('/api/users/@me', { headers })
const isAdmin = computed(() => currentUser.value?.role === 'ADMIN')

const isLoggingOut = ref(false)

const logout = async () => {
  isLoggingOut.value = true
  try {
    await $fetch('/api/users/logout', { method: 'POST' })
  } finally {
    isLoggingOut.value = false
  }
  await navigateTo('/admin/login')
}

// Общий список разделов — раньше строился в разметке дважды (верхняя
// навигация на десктопе и нижний таб-бар на мобильном), теперь один
// источник правды с иконками для таб-бара.
const navItems = computed(() => [
  { to: '/admin/orders', label: 'Заказы', icon: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01' },
  {
    to: '/admin/categories',
    label: 'Категории',
    icon: 'M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.169.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z'
  },
  {
    to: '/admin/products',
    label: 'Товары',
    icon: 'M20.25 7.5l-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z'
  },
  ...(isAdmin.value
    ? [
        {
          to: '/admin/users',
          label: 'Пользователи',
          icon: 'M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z'
        }
      ]
    : [])
])
</script>

<template>
  <div class="min-h-screen bg-milk">
    <header class="sticky top-0 z-30 border-b border-sand bg-white/90 backdrop-blur-sm">
      <div class="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-4 sm:px-8">
        <div class="flex flex-wrap items-center gap-6">
          <span class="font-display text-xl font-semibold text-coal">Админка</span>
          <!-- Навигация: десктоп, на мобильном её роль выполняет нижний таб-бар -->
          <nav class="hidden flex-wrap gap-2 lg:flex">
            <NuxtLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              class="admin-nav-link"
              active-class="admin-nav-link--active"
            >
              {{ item.label }}
            </NuxtLink>
          </nav>
        </div>
        <div class="flex items-center gap-1">
          <!-- Выход из админки на публичный сайт — отдельный уровень
               навигации от переключения разделов, поэтому не в таб-баре -->
          <NuxtLink
            to="/"
            class="flex items-center gap-1.5 rounded-full px-3 py-2 text-sm font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:bg-coal/5 hover:text-coal"
            aria-label="На сайт"
          >
            <svg class="h-5 w-5 shrink-0" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
            <span class="hidden sm:inline">На сайт</span>
          </NuxtLink>
          <button
            type="button"
            :disabled="isLoggingOut"
            class="rounded-full px-3 py-2 text-sm font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:bg-terra/10 hover:text-terra disabled:opacity-50"
            @click="logout"
          >
            Выйти
          </button>
        </div>
      </div>
    </header>

    <!-- pb с запасом под фиксированный таб-бар на мобильном -->
    <main class="mx-auto max-w-5xl px-4 py-10 pb-28 sm:px-8 lg:pb-10">
      <slot />
    </main>

    <!-- Нижний таб-бар: мобильная навигация вместо верхней, не помещающейся в ряд -->
    <nav
      class="fixed inset-x-0 bottom-0 z-30 flex border-t border-sand bg-white/95 px-2 pb-[max(theme(spacing.2),env(safe-area-inset-bottom))] pt-2 backdrop-blur-sm lg:hidden"
      aria-label="Разделы админки"
    >
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="admin-bottom-nav-link"
        active-class="admin-bottom-nav-link--active"
      >
        <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" :d="item.icon" />
        </svg>
        {{ item.label }}
      </NuxtLink>
    </nav>
  </div>
</template>
