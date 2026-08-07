<script setup lang="ts">
// Постоянно видимая корзина для десктопа (страница меню, lg+) — вместо
// иконки в шапке, которую легко не заметить. На мобильном её роль
// по-прежнему выполняет CartDrawer.
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

const goToCheckout = () => navigateTo('/checkout')
</script>

<template>
  <aside class="card sticky top-40 p-6">
    <h2 class="font-display text-xl font-semibold text-coal">Корзина</h2>

    <p v-if="!cart?.items.length" class="mt-6 text-center text-sm text-warmgray">
      Пока пусто — добавьте что-нибудь из меню.
    </p>

    <template v-else>
      <TransitionGroup
        tag="div"
        class="mt-4"
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 -translate-x-2"
        enter-to-class="opacity-100 translate-x-0"
        leave-active-class="transition duration-200 ease-in absolute"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        move-class="transition duration-300 ease-out"
      >
        <div
          v-for="item in cart.items"
          :key="item.product_id"
          class="flex gap-3 border-b border-sand py-3 last:border-b-0"
        >
          <div class="h-14 w-14 shrink-0 overflow-hidden rounded-lg bg-sand">
            <img
              v-if="item.image"
              :src="`/api/uploads/${item.image}`"
              :alt="item.name"
              class="h-full w-full object-cover"
            />
          </div>
          <div class="min-w-0 flex-1">
            <h3 class="truncate text-sm font-semibold text-coal">{{ item.name }}</h3>
            <div class="mt-1.5 flex items-center gap-2">
              <button
                type="button"
                class="flex h-6 w-6 items-center justify-center rounded-full border border-coal/20 text-xs text-coal transition-all duration-200 hover:border-olive hover:bg-olive/5 active:scale-95 disabled:opacity-50"
                :disabled="isUpdating === item.product_id"
                aria-label="Уменьшить количество"
                @click="changeQuantity(item.product_id, item.quantity - 1)"
              >
                −
              </button>
              <span class="w-4 text-center text-sm text-coal">{{ item.quantity }}</span>
              <button
                type="button"
                class="flex h-6 w-6 items-center justify-center rounded-full border border-coal/20 text-xs text-coal transition-all duration-200 hover:border-olive hover:bg-olive/5 active:scale-95 disabled:opacity-50"
                :disabled="isUpdating === item.product_id"
                aria-label="Увеличить количество"
                @click="changeQuantity(item.product_id, item.quantity + 1)"
              >
                +
              </button>
            </div>
          </div>
          <span class="whitespace-nowrap text-sm font-semibold text-terra">
            {{ formatPrice(item.item_total_price) }}
          </span>
        </div>
      </TransitionGroup>

      <div class="mt-4 border-t border-sand pt-4">
        <div class="flex items-center justify-between text-base font-semibold text-coal">
          <span>Итого</span>
          <span>{{ formatPrice(cart.total_price) }}</span>
        </div>
        <button type="button" class="btn-primary mt-4 w-full" @click="goToCheckout">
          Оформить заказ
        </button>
      </div>
    </template>
  </aside>
</template>
