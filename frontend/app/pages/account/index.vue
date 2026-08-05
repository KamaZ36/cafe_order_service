<script setup lang="ts">
import type { OrderDTO, OrderListDTO } from '~/types/order'

definePageMeta({ middleware: 'account-auth' })
useHead({ title: 'Личный кабинет — Мясная деревня' })

const user = useCurrentUser()

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: orderList, refresh } = await useFetch<OrderListDTO>('/api/users/@me/orders', {
  query: { limit: 50, offset: 0 },
  headers
})

const activeStatuses: OrderDTO['status'][] = ['PENDING', 'CONFIRMED', 'READY']

const activeOrders = computed(
  () => orderList.value?.orders.filter((order) => activeStatuses.includes(order.status)) ?? []
)
const pastOrders = computed(
  () => orderList.value?.orders.filter((order) => !activeStatuses.includes(order.status)) ?? []
)

const isCancelling = ref<string | null>(null)

const cancelOrder = async (orderId: string) => {
  isCancelling.value = orderId
  try {
    await $fetch(`/api/users/@me/orders/${orderId}/cancel`, { method: 'PATCH' })
    await refresh()
  } catch {
    // Заказ уже нельзя отменить (не PENDING) — просто обновим список
    await refresh()
  } finally {
    isCancelling.value = null
  }
}

const logout = async () => {
  await $fetch('/api/users/logout', { method: 'POST' })
  user.value = null
  await navigateTo('/')
}
</script>

<template>
  <div>
    <Header />

    <main class="min-h-screen bg-milk pt-32 pb-24">
      <div class="mx-auto max-w-3xl px-4 sm:px-8">
        <h1 class="font-display text-4xl font-semibold text-coal">Личный кабинет</h1>

        <!-- Профиль -->
        <div class="card mt-6 flex items-center justify-between gap-4 p-6">
          <div class="flex items-center gap-4">
            <div
              class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-sand font-display text-lg font-semibold text-coal"
              aria-hidden="true"
            >
              {{ user?.phone_number?.slice(-2) }}
            </div>
            <div>
              <p class="text-xs font-medium uppercase tracking-wide text-warmgray">Телефон</p>
              <p class="font-display text-lg font-semibold text-coal">{{ user?.phone_number }}</p>
            </div>
          </div>
          <button
            type="button"
            class="text-sm font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra"
            @click="logout"
          >
            Выйти
          </button>
        </div>

        <!-- Пусто -->
        <p v-if="!orderList?.orders.length" class="mt-12 text-warmgray">
          Заказов пока нет.
          <NuxtLink to="/cafe" class="text-olive underline">Перейти в меню</NuxtLink>
        </p>

        <template v-else>
          <!-- Текущие заказы -->
          <section v-if="activeOrders.length" class="mt-12">
            <h2 class="font-display text-2xl font-semibold text-coal">
              Текущие заказы
              <span class="ml-1 text-lg font-normal text-warmgray">({{ activeOrders.length }})</span>
            </h2>
            <div class="mt-6 space-y-4">
              <OrderCard
                v-for="(order, i) in activeOrders"
                :key="order.id"
                :order="order"
                :cancelling="isCancelling === order.id"
                :index="i"
                @cancel="cancelOrder"
              />
            </div>
          </section>

          <!-- История заказов -->
          <section v-if="pastOrders.length" class="mt-12">
            <h2 class="font-display text-2xl font-semibold text-coal">История заказов</h2>
            <div class="mt-6 space-y-4">
              <OrderCard
                v-for="(order, i) in pastOrders"
                :key="order.id"
                :order="order"
                :cancelling="false"
                :index="i"
              />
            </div>
          </section>
        </template>
      </div>
    </main>

    <Footer />
  </div>
</template>
