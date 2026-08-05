<script setup lang="ts">
import type { OrderDTO, OrderListDTO } from '~/types/order'

definePageMeta({ middleware: 'admin-auth', layout: 'admin' })
useHead({ title: 'Заказы — Админка' })

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: orderList, refresh } = await useFetch<OrderListDTO>('/api/orders', {
  query: { limit: 50, offset: 0 },
  headers
})

const activeStatuses: OrderDTO['status'][] = ['PENDING', 'CONFIRMED', 'READY']

const activeOrders = computed(
  () => orderList.value?.orders.filter((order) => activeStatuses.includes(order.status)) ?? []
)
const recentOrders = computed(
  () => orderList.value?.orders.filter((order) => !activeStatuses.includes(order.status)) ?? []
)

const nextEndpoint: Record<string, string> = {
  PENDING: 'confirm',
  CONFIRMED: 'ready',
  READY: 'complete'
}

const busyOrderId = ref<string | null>(null)

const advanceOrder = async (orderId: string) => {
  const order = orderList.value?.orders.find((o) => o.id === orderId)
  const endpoint = order && nextEndpoint[order.status]
  if (!endpoint) return

  busyOrderId.value = orderId
  try {
    await $fetch(`/api/orders/${orderId}/${endpoint}`, { method: 'PATCH' })
    await refresh()
  } finally {
    busyOrderId.value = null
  }
}

const cancellingOrder = ref<OrderDTO | null>(null)

const openCancelModal = (orderId: string) => {
  cancellingOrder.value = orderList.value?.orders.find((o) => o.id === orderId) ?? null
}

const confirmCancelOrder = async (reason: string | null) => {
  const orderId = cancellingOrder.value?.id
  if (!orderId) return

  busyOrderId.value = orderId
  try {
    await $fetch(`/api/orders/${orderId}/cancel`, {
      method: 'PATCH',
      body: { reason }
    })
    await refresh()
  } finally {
    busyOrderId.value = null
  }
}

// Поллинг очереди: заказ может прийти от клиента в любой момент, отдельного
// пуша (вебсокет/SSE) пока нет — раз в 7с просто перезапрашиваем список.
// Для одной точки продаж такой задержки более чем достаточно.
let pollTimer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  pollTimer = setInterval(refresh, 7000)
})

onBeforeUnmount(() => {
  clearInterval(pollTimer)
})
</script>

<template>
  <div>
    <div class="flex items-end justify-between gap-4">
      <div>
        <span class="kicker">Очередь</span>
        <h1 class="font-display text-3xl font-semibold text-coal">Заказы</h1>
      </div>
      <span class="flex items-center gap-1.5 text-xs uppercase tracking-wide text-warmgray">
        <span class="h-1.5 w-1.5 rounded-full bg-olive" />
        Обновляется автоматически
      </span>
    </div>

    <p v-if="!orderList?.orders.length" class="card mt-8 px-5 py-8 text-center text-warmgray">
      Заказов пока нет.
    </p>

    <template v-else>
      <section v-if="activeOrders.length" class="mt-8">
        <h2 class="font-display text-xl font-semibold text-coal">
          В очереди
          <span class="ml-1 text-base font-normal text-warmgray">({{ activeOrders.length }})</span>
        </h2>
        <TransitionGroup
          tag="div"
          class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
          enter-active-class="transition duration-400 ease-out"
          enter-from-class="opacity-0 -translate-y-3"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-200 ease-in absolute"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
          move-class="transition duration-300 ease-out"
        >
          <StaffOrderCard
            v-for="order in activeOrders"
            :key="order.id"
            :order="order"
            :busy="busyOrderId === order.id"
            @advance="advanceOrder"
            @cancel="openCancelModal"
          />
        </TransitionGroup>
      </section>
      <p v-else class="mt-8 text-warmgray">Активных заказов нет — можно выдохнуть.</p>

      <section v-if="recentOrders.length" class="mt-12">
        <h2 class="font-display text-xl font-semibold text-coal">Недавно завершённые</h2>
        <div class="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StaffOrderCard
            v-for="order in recentOrders"
            :key="order.id"
            :order="order"
            :busy="false"
            class="opacity-70"
          />
        </div>
      </section>
    </template>

    <CancelOrderModal
      v-if="cancellingOrder"
      :order-number="cancellingOrder.order_number"
      @close="cancellingOrder = null"
      @confirm="confirmCancelOrder"
    />
  </div>
</template>
