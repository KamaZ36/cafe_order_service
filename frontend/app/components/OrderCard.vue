<script setup lang="ts">
import type { OrderDTO } from '~/types/order'

defineProps<{ order: OrderDTO; cancelling: boolean; index?: number }>()
defineEmits<{ cancel: [orderId: string] }>()

const { el, visible } = useReveal()

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
  <article
    ref="el"
    class="card p-6 transition-all duration-500 ease-out hover:shadow-md"
    :class="[
      visible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0',
      { 'opacity-70': order.status === 'CANCELLED' }
    ]"
    :style="{ transitionDelay: visible ? `${Math.min(index ?? 0, 8) * 60}ms` : '0ms' }"
  >
    <div class="flex flex-wrap items-center justify-between gap-2">
      <div>
        <span class="font-display text-lg font-semibold text-coal">
          Заказ №{{ order.order_number }}
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

    <ul class="mt-4 space-y-1 border-t border-dashed border-coal/15 pt-4 text-sm text-coal">
      <li v-for="item in order.items" :key="item.product_id" class="flex justify-between">
        <span>{{ item.name }} × {{ item.quantity }}</span>
        <span class="text-warmgray">{{ formatPrice(item.item_total_price) }}</span>
      </li>
    </ul>

    <p v-if="order.comment" class="mt-3 text-sm text-warmgray">
      Комментарий: {{ order.comment }}
    </p>

    <p v-if="order.status === 'CANCELLED' && order.cancel_reason" class="mt-3 text-sm text-warmgray">
      Причина отмены: {{ order.cancel_reason }}
    </p>

    <div class="mt-4 flex items-center justify-between border-t border-sand pt-4">
      <span class="font-display text-lg font-semibold text-terra">
        {{ formatPrice(order.total_amount) }}
      </span>
      <button
        v-if="order.status === 'PENDING'"
        type="button"
        :disabled="cancelling"
        class="text-sm font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra disabled:opacity-50"
        @click="$emit('cancel', order.id)"
      >
        Отменить
      </button>
    </div>
  </article>
</template>
