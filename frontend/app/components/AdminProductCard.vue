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

defineProps<{ product: ProductListItemDTO }>()
defineEmits<{ edit: [productId: string]; delete: [productId: string] }>()

const imageUrl = (image: string | null) => (image ? `/api/uploads/${image}` : null)
const formatPrice = (price: string) => `${Math.round(Number(price))} ₽`
</script>

<template>
  <article
    class="card relative overflow-hidden transition-shadow duration-200 hover:shadow-lg"
    :class="{ 'opacity-60': !product.is_available }"
  >
    <!-- Тот же бейдж, что видит клиент — так сразу понятно, как карточка выглядит в меню -->
    <span
      v-if="product.is_popular"
      class="absolute left-4 top-4 z-10 rounded-full bg-terra px-3 py-1 text-xs font-medium uppercase tracking-wide text-white shadow-sm"
    >
      Хит
    </span>
    <span
      v-else-if="product.is_new"
      class="absolute left-4 top-4 z-10 rounded-full bg-olive px-3 py-1 text-xs font-medium uppercase tracking-wide text-white shadow-sm"
    >
      Новинка
    </span>
    <span
      v-if="!product.is_available"
      class="absolute right-4 top-4 z-10 rounded-full bg-coal/80 px-3 py-1 text-xs font-medium uppercase tracking-wide text-white shadow-sm"
    >
      Недоступен
    </span>

    <div class="aspect-square overflow-hidden bg-sand">
      <img
        v-if="imageUrl(product.image)"
        :src="imageUrl(product.image)!"
        :alt="product.name"
        class="h-full w-full object-cover"
        loading="lazy"
      />
    </div>

    <div class="p-6">
      <div class="flex items-start justify-between gap-4">
        <h3 class="font-display text-2xl font-semibold text-coal">
          {{ product.name }}
        </h3>
        <span class="whitespace-nowrap font-display text-xl font-semibold text-terra">
          {{ formatPrice(product.price) }}
        </span>
      </div>

      <div class="mt-4 flex gap-4">
        <button
          type="button"
          class="text-xs font-medium uppercase tracking-wide text-olive transition-colors duration-200 hover:text-olive-dark"
          @click="$emit('edit', product.id)"
        >
          Редактировать
        </button>
        <button
          type="button"
          class="text-xs font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra"
          @click="$emit('delete', product.id)"
        >
          Удалить
        </button>
      </div>
    </div>
  </article>
</template>
