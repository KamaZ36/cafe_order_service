<script setup lang="ts">
import type { OrderDTO } from '~/types/order'

const props = defineProps<{ order: OrderDTO; busy: boolean }>()
const emit = defineEmits<{ advance: [orderId: string]; cancel: [orderId: string] }>()

const cancellableStatuses: OrderDTO['status'][] = ['PENDING', 'CONFIRMED', 'READY']
const isCancellable = computed(() => cancellableStatuses.includes(props.order.status))

const statusLabels: Record<OrderDTO['status'], string> = {
  PENDING: 'Ожидает подтверждения',
  CONFIRMED: 'Подтверждён',
  READY: 'Готов к выдаче',
  COMPLETED: 'Выполнен',
  CANCELLED: 'Отменён'
}

const statusColors: Record<OrderDTO['status'], string> = {
  PENDING: 'bg-sand text-coal',
  CONFIRMED: 'bg-olive/15 text-olive-dark',
  READY: 'bg-olive text-white',
  COMPLETED: 'bg-coal/10 text-coal',
  CANCELLED: 'bg-terra/10 text-terra'
}

// Следующий шаг очереди по текущему статусу — CONFIRMED/COMPLETED/CANCELLED
// в очереди для действий уже не показываются (см. фильтр в родителе)
const nextActionLabel: Partial<Record<OrderDTO['status'], string>> = {
  PENDING: 'Подтвердить',
  CONFIRMED: 'Готов к выдаче',
  READY: 'Выдать'
}

const formatPrice = (price: string) => `${Math.round(Number(price))} ₽`
const formatDate = (iso: string) =>
  new Date(iso).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit'
  })
</script>

<template>
  <article class="card p-6 transition-shadow duration-300 hover:shadow-md">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <div>
        <span class="font-display text-xl font-semibold text-coal">
          №{{ order.order_number }}
        </span>
        <span class="ml-3 text-sm text-warmgray">{{ formatDate(order.created_at) }}</span>
      </div>
      <span
        class="rounded-full px-3 py-1 text-xs font-medium uppercase tracking-wide"
        :class="statusColors[order.status]"
      >
        {{ statusLabels[order.status] }}
      </span>
    </div>

    <p v-if="order.customer_phone_number" class="mt-1 text-sm text-warmgray">
      Для сверки при выдаче: <span class="font-medium text-coal">{{ order.customer_phone_number }}</span>
    </p>

    <ul class="mt-4 space-y-1 border-t border-dashed border-coal/15 pt-4 text-sm text-coal">
      <li v-for="item in order.items" :key="item.product_id" class="flex justify-between">
        <span>{{ item.name }} × {{ item.quantity }}</span>
        <span class="text-warmgray">{{ formatPrice(item.item_total_price) }}</span>
      </li>
    </ul>

    <p v-if="order.comment" class="mt-3 text-sm text-warmgray">
      Комментарий: {{ order.comment }}
    </p>

    <p v-if="order.status === 'CANCELLED' && order.cancel_reason" class="mt-3 text-sm text-terra">
      Причина отмены: {{ order.cancel_reason }}
    </p>

    <div class="mt-4 border-t border-sand pt-4">
      <span class="font-display text-lg font-semibold text-terra">
        {{ formatPrice(order.total_amount) }}
      </span>

      <div v-if="isCancellable || nextActionLabel[order.status]" class="mt-3 flex items-center gap-3">
        <button
          v-if="isCancellable"
          type="button"
          :disabled="busy"
          class="shrink-0 text-sm font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra disabled:opacity-50"
          @click="emit('cancel', order.id)"
        >
          Отменить
        </button>
        <button
          v-if="nextActionLabel[order.status]"
          type="button"
          :disabled="busy"
          class="btn-primary flex-1 px-4 py-2"
          @click="emit('advance', order.id)"
        >
          {{ busy ? 'Сохраняем…' : nextActionLabel[order.status] }}
        </button>
      </div>
    </div>
  </article>
</template>
