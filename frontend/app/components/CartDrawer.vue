<script setup lang="ts">
const emit = defineEmits<{ close: [] }>()
const cart = useCart()

const isUpdating = ref<string | null>(null)

const changeQuantity = async (productId: string, quantity: number) => {
  isUpdating.value = productId
  try {
    await updateCartItemQuantity(productId, quantity)
  } finally {
    isUpdating.value = null
  }
}

const formatPrice = (price: string) => `${Math.round(Number(price))} ₽`

// Плавное закрытие: сначала transition, реальный emit('close') — после него
const visible = ref(true)
const close = () => {
  visible.value = false
}

useModalLifecycle(close)

const goToCheckout = () => {
  close()
  navigateTo('/checkout')
}
</script>

<template>
  <Transition
    enter-active-class="transition duration-250 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
    appear
    @after-leave="emit('close')"
  >
    <div v-if="visible" class="fixed inset-0 z-[60] flex justify-end bg-coal/40 backdrop-blur-sm" @click.self="close">
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="translate-x-full"
        appear
      >
        <aside v-if="visible" class="flex h-full w-full max-w-md flex-col bg-white shadow-2xl">
          <div class="flex items-center justify-between border-b border-sand px-6 py-4">
            <h2 class="font-display text-2xl font-semibold text-coal">Корзина</h2>
            <button
              type="button"
              class="flex h-11 w-11 items-center justify-center rounded-full text-warmgray transition-all duration-150 hover:bg-coal/5 hover:text-coal active:scale-90"
              aria-label="Закрыть"
              @click="close"
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto px-6 py-4">
            <p v-if="!cart?.items.length" class="text-center text-warmgray">
              Корзина пуста.
            </p>

            <TransitionGroup
              enter-active-class="transition duration-300 ease-out"
              enter-from-class="opacity-0 -translate-x-2"
              enter-to-class="opacity-100 translate-x-0"
              leave-active-class="transition duration-200 ease-in absolute"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
              move-class="transition duration-300 ease-out"
            >
              <div
                v-for="item in cart?.items"
                :key="item.product_id"
                class="flex gap-4 border-b border-sand py-4 last:border-b-0"
              >
                <div class="h-20 w-20 shrink-0 overflow-hidden rounded-lg bg-sand">
                  <img
                    v-if="item.image"
                    :src="`/api/uploads/${item.image}`"
                    :alt="item.name"
                    class="h-full w-full object-cover"
                  />
                </div>
                <div class="flex-1">
                  <h3 class="font-display text-lg font-semibold text-coal">
                    {{ item.name }}
                  </h3>
                  <p class="mt-1 text-sm text-warmgray">{{ formatPrice(item.price) }} / шт</p>
                  <div class="mt-2 flex items-center gap-3">
                    <button
                      type="button"
                      class="flex h-11 w-11 items-center justify-center rounded-full border border-coal/20 text-coal transition-all duration-200 hover:border-olive hover:bg-olive/5 active:scale-95 disabled:opacity-50"
                      :disabled="isUpdating === item.product_id"
                      aria-label="Уменьшить количество"
                      @click="changeQuantity(item.product_id, item.quantity - 1)"
                    >
                      −
                    </button>
                    <span class="w-6 text-center text-coal">{{ item.quantity }}</span>
                    <button
                      type="button"
                      class="flex h-11 w-11 items-center justify-center rounded-full border border-coal/20 text-coal transition-all duration-200 hover:border-olive hover:bg-olive/5 active:scale-95 disabled:opacity-50"
                      :disabled="isUpdating === item.product_id"
                      aria-label="Увеличить количество"
                      @click="changeQuantity(item.product_id, item.quantity + 1)"
                    >
                      +
                    </button>
                  </div>
                </div>
                <span class="whitespace-nowrap font-display text-lg font-semibold text-terra">
                  {{ formatPrice(item.item_total_price) }}
                </span>
              </div>
            </TransitionGroup>
          </div>

          <div v-if="cart?.items.length" class="border-t border-sand px-6 py-4">
            <div class="flex items-center justify-between text-lg font-semibold text-coal">
              <span>Итого</span>
              <span>{{ formatPrice(cart.total_price) }}</span>
            </div>
            <button type="button" class="btn-primary mt-4 w-full" @click="goToCheckout">
              Оформить заказ
            </button>
          </div>
        </aside>
      </Transition>
    </div>
  </Transition>
</template>
