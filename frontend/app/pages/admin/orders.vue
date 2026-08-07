<script setup lang="ts">
import type { OrderDTO, OrderListDTO } from '~/types/order'

definePageMeta({ middleware: 'admin-auth', layout: 'admin' })
useHead({ title: 'Заказы — Админка' })

const route = useRoute()
const router = useRouter()

const TAB_KEYS = ['queue', 'completed'] as const
type TabKey = (typeof TAB_KEYS)[number]

function isTabKey(value: unknown): value is TabKey {
  return typeof value === 'string' && (TAB_KEYS as readonly string[]).includes(value)
}

const activeTab = ref<TabKey>(isTabKey(route.query.tab) ? route.query.tab : 'queue')

function selectTab(key: string) {
  activeTab.value = key as TabKey
  router.replace({ query: { ...route.query, tab: key === 'queue' ? undefined : key } })
}

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

// Вкладка «В очереди» — сервер сам отдаёт только активные статусы
// (PENDING/CONFIRMED/READY), старые первыми.
const { data: queueList, refresh: refreshQueue } = await useFetch<OrderListDTO>('/api/orders', {
  query: { limit: 50, offset: 0 },
  headers
})

// Вкладка «Завершённые» — отдельный запрос с явным фильтром по статусу
// (тем самым включается сортировка «недавние первыми», см. бэкенд),
// подгружается постранично.
const COMPLETED_PAGE_SIZE = 20

async function fetchCompletedPage(offset: number) {
  return await $fetch<OrderListDTO>('/api/orders', {
    method: 'GET',
    query: { status: ['COMPLETED', 'CANCELLED'], limit: COMPLETED_PAGE_SIZE, offset },
    headers
  })
}

const firstCompletedPage = await fetchCompletedPage(0)
const completedOrders = ref<OrderDTO[]>(firstCompletedPage.orders)
const completedTotal = ref(firstCompletedPage.total_count)
const isLoadingMoreCompleted = ref(false)
const hasMoreCompleted = computed(() => completedOrders.value.length < completedTotal.value)

const loadMoreCompleted = async () => {
  isLoadingMoreCompleted.value = true
  try {
    const page = await fetchCompletedPage(completedOrders.value.length)
    completedOrders.value.push(...page.orders)
  } finally {
    isLoadingMoreCompleted.value = false
  }
}

const refreshCompletedFirstPage = async () => {
  const page = await fetchCompletedPage(0)
  completedOrders.value = page.orders
  completedTotal.value = page.total_count
}

const tabs = computed(() => [
  { key: 'queue', label: 'В очереди', count: queueList.value?.orders.length ?? 0 },
  { key: 'completed', label: 'Завершённые', count: completedTotal.value }
])

const nextEndpoint: Record<string, string> = {
  PENDING: 'confirm',
  CONFIRMED: 'ready',
  READY: 'complete'
}

const busyOrderId = ref<string | null>(null)

const advanceOrder = async (orderId: string) => {
  const order = queueList.value?.orders.find((o) => o.id === orderId)
  const endpoint = order && nextEndpoint[order.status]
  if (!endpoint) return

  busyOrderId.value = orderId
  try {
    await $fetch(`/api/orders/${orderId}/${endpoint}`, { method: 'PATCH' })
    await refreshQueue()
    if (endpoint === 'complete') await refreshCompletedFirstPage()
  } finally {
    busyOrderId.value = null
  }
}

const cancellingOrder = ref<OrderDTO | null>(null)

const openCancelModal = (orderId: string) => {
  cancellingOrder.value = queueList.value?.orders.find((o) => o.id === orderId) ?? null
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
    await refreshQueue()
    await refreshCompletedFirstPage()
  } finally {
    busyOrderId.value = null
  }
}

// Поллинг очереди: заказ может прийти от клиента в любой момент, отдельного
// пуша (вебсокет/SSE) пока нет — раз в 7с просто перезапрашиваем список.
// Для одной точки продаж такой задержки более чем достаточно. Историю
// завершённых не поллим — она никуда не убегает.
let pollTimer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  pollTimer = setInterval(refreshQueue, 7000)
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

    <AdminTabs class="mt-8" :tabs="tabs" :model-value="activeTab" @update:model-value="selectTab" />

    <div
      v-if="activeTab === 'queue'"
      id="admin-tabpanel-queue"
      role="tabpanel"
      aria-labelledby="admin-tab-queue"
      class="mt-8"
    >
      <p v-if="!queueList?.orders.length" class="card px-5 py-8 text-center text-warmgray">
        Активных заказов нет — можно выдохнуть.
      </p>
      <TransitionGroup
        v-else
        tag="div"
        class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        enter-active-class="transition duration-400 ease-out"
        enter-from-class="opacity-0 -translate-y-3"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in absolute"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        move-class="transition duration-300 ease-out"
      >
        <StaffOrderCard
          v-for="order in queueList.orders"
          :key="order.id"
          :order="order"
          :busy="busyOrderId === order.id"
          @advance="advanceOrder"
          @cancel="openCancelModal"
        />
      </TransitionGroup>
    </div>

    <div
      v-else
      id="admin-tabpanel-completed"
      role="tabpanel"
      aria-labelledby="admin-tab-completed"
      class="mt-8"
    >
      <p v-if="!completedOrders.length" class="card px-5 py-8 text-center text-warmgray">
        Завершённых заказов пока нет.
      </p>
      <template v-else>
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StaffOrderCard
            v-for="order in completedOrders"
            :key="order.id"
            :order="order"
            :busy="false"
            class="opacity-70"
          />
        </div>
        <div v-if="hasMoreCompleted" class="mt-6 text-center">
          <button
            type="button"
            :disabled="isLoadingMoreCompleted"
            class="text-xs font-medium uppercase tracking-wide text-olive transition-colors duration-200 hover:text-olive-dark disabled:opacity-50"
            @click="loadMoreCompleted"
          >
            {{ isLoadingMoreCompleted ? 'Загружаем…' : 'Показать ещё' }}
          </button>
        </div>
      </template>
    </div>

    <CancelOrderModal
      v-if="cancellingOrder"
      :order-number="cancellingOrder.order_number"
      @close="cancellingOrder = null"
      @confirm="confirmCancelOrder"
    />
  </div>
</template>
