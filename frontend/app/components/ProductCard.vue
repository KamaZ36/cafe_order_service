<script setup lang="ts">
interface ProductListItemDTO {
  id: string
  name: string
  image: string | null
  price: string
  category_id: string
  is_available: boolean
  is_popular: boolean
  is_new: boolean
}

defineProps<{ product: ProductListItemDTO; adding: boolean; index: number }>()
defineEmits<{ add: [productId: string]; open: [productId: string] }>()

const { el, visible } = useReveal()

const imageUrl = (image: string | null) => (image ? `/api/uploads/${image}` : null)
const formatPrice = (price: string) => `${Math.round(Number(price))} ₽`
</script>

<template>
  <article
    ref="el"
    class="card group relative overflow-hidden transition-all duration-500 ease-out hover:-translate-y-1 hover:shadow-lg"
    :class="[
      visible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0',
      { 'opacity-50 hover:translate-y-0 hover:shadow-sm': !product.is_available }
    ]"
    :style="{ transitionDelay: visible ? `${Math.min(index, 8) * 60}ms` : '0ms' }"
  >
    <!-- Бейдж «Хит» / «Новинка» -->
    <span
      v-if="product.is_popular"
      class="pointer-events-none absolute left-4 top-4 z-10 rounded-full bg-terra px-3 py-1 text-xs font-medium uppercase tracking-wide text-white shadow-sm"
    >
      Хит
    </span>
    <span
      v-else-if="product.is_new"
      class="pointer-events-none absolute left-4 top-4 z-10 rounded-full bg-olive px-3 py-1 text-xs font-medium uppercase tracking-wide text-white shadow-sm"
    >
      Новинка
    </span>

    <!-- Открывает быстрый просмотр — фото и название/цена, но не сама
         кнопка «В корзину» (она отдельный элемент ниже, чтобы не вкладывать
         кнопку в кнопку) -->
    <button
      type="button"
      class="block w-full text-left"
      :aria-label="`Подробнее о товаре «${product.name}»`"
      @click="$emit('open', product.id)"
    >
      <div class="aspect-square overflow-hidden bg-sand">
        <img
          v-if="imageUrl(product.image)"
          :src="imageUrl(product.image)!"
          :alt="product.name"
          class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
          loading="lazy"
        />
      </div>

      <div class="p-6 pb-4">
        <div class="flex items-start justify-between gap-4">
          <h3 class="font-display text-2xl font-semibold text-coal">
            {{ product.name }}
          </h3>
          <span class="whitespace-nowrap font-display text-xl font-semibold text-terra">
            {{ formatPrice(product.price) }}
          </span>
        </div>
      </div>
    </button>

    <div class="px-6 pb-6">
      <p v-if="!product.is_available" class="text-sm text-warmgray">
        Временно недоступно
      </p>
      <button
        v-else
        type="button"
        :disabled="adding"
        class="btn-primary w-full"
        @click="$emit('add', product.id)"
      >
        {{ adding ? 'Добавляем…' : 'В корзину' }}
      </button>
    </div>
  </article>
</template>
