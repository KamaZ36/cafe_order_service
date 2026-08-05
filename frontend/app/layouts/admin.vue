<script setup lang="ts">
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
</script>

<template>
  <div class="min-h-screen bg-milk">
    <header class="sticky top-0 z-30 border-b border-sand bg-white/90 backdrop-blur-sm">
      <div class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-8">
        <div class="flex flex-wrap items-center gap-6">
          <span class="font-display text-xl font-semibold text-coal">Админка</span>
          <nav class="flex flex-wrap gap-2">
            <NuxtLink to="/admin/orders" class="admin-nav-link" active-class="admin-nav-link--active">
              Заказы
            </NuxtLink>
            <NuxtLink to="/admin/categories" class="admin-nav-link" active-class="admin-nav-link--active">
              Категории
            </NuxtLink>
            <NuxtLink to="/admin/products" class="admin-nav-link" active-class="admin-nav-link--active">
              Товары
            </NuxtLink>
          </nav>
        </div>
        <button
          type="button"
          :disabled="isLoggingOut"
          class="rounded-full px-3 py-2 text-sm font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:bg-terra/10 hover:text-terra disabled:opacity-50"
          @click="logout"
        >
          Выйти
        </button>
      </div>
    </header>

    <main class="mx-auto max-w-5xl px-4 py-10 sm:px-8">
      <slot />
    </main>
  </div>
</template>
