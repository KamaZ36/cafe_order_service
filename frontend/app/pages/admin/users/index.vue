<script setup lang="ts">
import type { StaffUserListDTO } from '~/types/user'

definePageMeta({ middleware: ['admin-auth', 'admin-only'], layout: 'admin' })
useHead({ title: 'Пользователи — Админка' })

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: userList } = await useFetch<StaffUserListDTO>('/api/users', {
  query: { limit: 100, offset: 0 },
  headers
})

const roleLabel: Record<string, string> = {
  ADMIN: 'Админ',
  MANAGER: 'Менеджер',
  CUSTOMER: 'Клиент'
}

const roleBadgeClass: Record<string, string> = {
  ADMIN: 'bg-terra/10 text-terra',
  MANAGER: 'bg-olive/10 text-olive-dark',
  CUSTOMER: 'bg-coal/10 text-warmgray'
}
</script>

<template>
  <div>
    <span class="kicker">Персонал</span>
    <h1 class="font-display text-3xl font-semibold text-coal">Пользователи</h1>

    <!-- Список строк вместо таблицы: на узком экране колонки просто некуда
         сжимать, а с таблицей это оборачивается горизонтальным скроллом.
         Каждая строка — цельная ссылка, чтобы не целиться в мелкий текст. -->
    <ul class="mt-8 space-y-3">
      <li v-for="user in userList?.users" :key="user.id">
        <NuxtLink
          :to="`/admin/users/${user.id}`"
          class="card flex min-h-[44px] items-center justify-between gap-3 px-5 py-4 transition-shadow duration-200 hover:shadow-md"
        >
          <span class="font-medium text-coal">
            {{ user.phone_number ?? '—' }}
          </span>
          <span class="flex items-center gap-3">
            <span
              class="rounded-full px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide"
              :class="roleBadgeClass[user.role]"
            >
              {{ roleLabel[user.role] }}
            </span>
            <svg class="h-4 w-4 shrink-0 text-warmgray" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </span>
        </NuxtLink>
      </li>
      <li v-if="!userList?.users.length" class="card px-5 py-8 text-center text-warmgray">
        Пользователей пока нет.
      </li>
    </ul>
  </div>
</template>
