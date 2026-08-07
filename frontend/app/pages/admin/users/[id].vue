<script setup lang="ts">
import type { StaffUserDetailDTO, StaffUserPaymentListDTO, UserPaymentDTO } from '~/types/user'

definePageMeta({ middleware: ['admin-auth', 'admin-only'], layout: 'admin' })

const route = useRoute()
const userId = route.params.id as string

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: user } = await useFetch<StaffUserDetailDTO>(`/api/users/${userId}`, { headers })

useHead({ title: () => `${user.value?.phone_number ?? 'Пользователь'} — Админка` })

const PAYMENTS_PAGE_SIZE = 20

const { data: firstPaymentsPage } = await useFetch<StaffUserPaymentListDTO>(
  `/api/users/${userId}/payments`,
  { query: { limit: PAYMENTS_PAGE_SIZE, offset: 0 }, headers }
)

const payments = ref<UserPaymentDTO[]>(firstPaymentsPage.value?.payments ?? [])
const paymentsTotal = ref(firstPaymentsPage.value?.total_count ?? 0)
const isLoadingMorePayments = ref(false)
const hasMorePayments = computed(() => payments.value.length < paymentsTotal.value)

const loadMorePayments = async () => {
  isLoadingMorePayments.value = true
  try {
    const page = await $fetch<StaffUserPaymentListDTO>(`/api/users/${userId}/payments`, {
      query: { limit: PAYMENTS_PAGE_SIZE, offset: payments.value.length }
    })
    payments.value.push(...page.payments)
  } finally {
    isLoadingMorePayments.value = false
  }
}

const roleLabel: Record<string, string> = {
  ADMIN: 'Админ',
  MANAGER: 'Менеджер',
  CUSTOMER: 'Клиент'
}

const paymentStatusLabel: Record<string, string> = {
  PENDING: 'Ожидает оплаты',
  CONFIRMED: 'Оплачен',
  CANCELED: 'Отменён'
}

const paymentStatusClass: Record<string, string> = {
  PENDING: 'bg-coal/10 text-warmgray',
  CONFIRMED: 'bg-olive/10 text-olive-dark',
  CANCELED: 'bg-terra/10 text-terra'
}

const formatDate = (value: string) =>
  new Date(value).toLocaleString('ru-RU', { dateStyle: 'medium', timeStyle: 'short' })

const formatAmount = (kopecks: number) => `${(kopecks / 100).toFixed(2)} ₽`
</script>

<template>
  <div>
    <NuxtLink
      to="/admin/users"
      class="text-xs font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra"
    >
      ← Все пользователи
    </NuxtLink>

    <div class="mt-4 flex flex-wrap items-center gap-3">
      <h1 class="font-display text-3xl font-semibold text-coal">
        {{ user?.phone_number ?? '—' }}
      </h1>
      <span
        v-if="user"
        class="rounded-full bg-terra/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-terra"
      >
        {{ roleLabel[user.role] }}
      </span>
    </div>

    <section class="mt-10">
      <h2 class="font-display text-xl font-semibold text-coal">Сессии</h2>
      <!-- Строки вместо таблицы — на телефоне колонки с датами и IP просто
           не помещаются в ширину, пришлось бы скроллить по горизонтали -->
      <ul class="mt-4 space-y-3">
        <li
          v-for="session in user?.sessions"
          :key="session.session_id"
          class="card flex flex-wrap items-center gap-x-6 gap-y-1 px-5 py-4"
        >
          <span class="font-medium text-coal">{{ session.ip_address ?? '—' }}</span>
          <span class="text-sm text-warmgray">Создана: {{ formatDate(session.created_at) }}</span>
          <span class="text-sm text-warmgray">Истекает: {{ formatDate(session.expires_at) }}</span>
        </li>
        <li v-if="!user?.sessions.length" class="card px-5 py-8 text-center text-warmgray">
          Сессий пока нет.
        </li>
      </ul>
    </section>

    <section class="mt-10">
      <h2 class="font-display text-xl font-semibold text-coal">Платежи</h2>
      <ul class="mt-4 space-y-3">
        <li
          v-for="payment in payments"
          :key="payment.id"
          class="card flex flex-wrap items-center gap-x-6 gap-y-2 px-5 py-4"
        >
          <span class="font-medium text-coal">№{{ payment.order_number }}</span>
          <span class="text-coal">{{ formatAmount(payment.amount) }}</span>
          <span
            class="rounded-full px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide"
            :class="paymentStatusClass[payment.status]"
          >
            {{ paymentStatusLabel[payment.status] }}
          </span>
          <span class="text-sm text-warmgray">{{ formatDate(payment.created_at) }}</span>
        </li>
        <li v-if="!payments.length" class="card px-5 py-8 text-center text-warmgray">
          Платежей пока нет.
        </li>
      </ul>
      <div v-if="hasMorePayments" class="mt-4 text-center">
        <button
          type="button"
          :disabled="isLoadingMorePayments"
          class="text-xs font-medium uppercase tracking-wide text-olive transition-colors duration-200 hover:text-olive-dark disabled:opacity-50"
          @click="loadMorePayments"
        >
          {{ isLoadingMorePayments ? 'Загружаем…' : 'Показать ещё' }}
        </button>
      </div>
    </section>
  </div>
</template>
