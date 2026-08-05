<script setup lang="ts">
definePageMeta({ middleware: 'admin-auth' })

// Права у ADMIN и MANAGER теперь одинаковые (меню + заказы), это просто
// разная стартовая страница по типичному сценарию использования
const user = await fetchCurrentUser()
await navigateTo(user?.role === 'ADMIN' ? '/admin/categories' : '/admin/orders')
</script>

<template>
  <div />
</template>
