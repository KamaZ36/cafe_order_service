<script setup lang="ts">
// Секция «Витрина магазина»: горизонтальная карусель товаров со стрелками
const { products } = useSiteData()

const currentIndex = ref(0)
// Сколько карточек видно одновременно (адаптив: 1 / 2 / 3)
const visibleCount = ref(3)

const updateVisibleCount = () => {
  const w = window.innerWidth
  visibleCount.value = w < 640 ? 1 : w < 1024 ? 2 : 3
  // При изменении ширины не даём индексу выйти за допустимый предел
  currentIndex.value = Math.min(currentIndex.value, maxIndex.value)
}

// Последняя допустимая позиция карусели
const maxIndex = computed(() => Math.max(products.length - visibleCount.value, 0))

const prev = () => {
  currentIndex.value = Math.max(currentIndex.value - 1, 0)
}
const next = () => {
  currentIndex.value = Math.min(currentIndex.value + 1, maxIndex.value)
}

// Сдвиг ленты: одна карточка = 100% / visibleCount ширины контейнера
const trackStyle = computed(() => ({
  transform: `translateX(-${currentIndex.value * (100 / visibleCount.value)}%)`
}))

onMounted(() => {
  updateVisibleCount()
  window.addEventListener('resize', updateVisibleCount, { passive: true })
})

onBeforeUnmount(() => window.removeEventListener('resize', updateVisibleCount))
</script>

<template>
  <section id="shop" class="scroll-mt-20 bg-milk py-24 lg:py-[120px]">
    <div class="mx-auto max-w-7xl px-4 sm:px-8">
      <div class="flex items-end justify-between gap-4">
        <div>
          <h2 class="font-display text-4xl font-semibold text-coal lg:text-[48px]">
            Витрина магазина
          </h2>
          <p class="mt-4 max-w-xl text-base leading-relaxed text-text-soft">
            Примеры продукции нашего цеха — ветчина и колбасы ручной работы.
            Полный ассортимент — на витрине магазина.
          </p>
        </div>

        <!-- Стрелки управления каруселью -->
        <div class="flex gap-2">
          <button
            type="button"
            class="flex h-12 w-12 items-center justify-center border border-olive text-olive transition-colors duration-200 hover:bg-olive hover:text-white disabled:cursor-not-allowed disabled:border-warmgray/40 disabled:text-warmgray/40 disabled:hover:bg-transparent"
            :disabled="currentIndex === 0"
            aria-label="Предыдущий товар"
            @click="prev"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          </button>
          <button
            type="button"
            class="flex h-12 w-12 items-center justify-center border border-olive text-olive transition-colors duration-200 hover:bg-olive hover:text-white disabled:cursor-not-allowed disabled:border-warmgray/40 disabled:text-warmgray/40 disabled:hover:bg-transparent"
            :disabled="currentIndex === maxIndex"
            aria-label="Следующий товар"
            @click="next"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Лента карусели -->
      <div class="mt-16 overflow-hidden">
        <div
          class="flex transition-transform duration-300 ease-out"
          :style="trackStyle"
        >
          <article
            v-for="product in products"
            :key="product.name"
            class="w-full shrink-0 px-3 sm:w-1/2 lg:w-1/3"
          >
            <div
              class="group relative border border-sand bg-white p-6 transition-shadow duration-300 hover:shadow-[0_10px_30px_rgba(0,0,0,0.05)]"
            >
              <!-- Бейдж «Хит» для флагманского товара -->
              <span
                v-if="product.hit"
                class="absolute left-4 top-4 z-10 bg-terra px-3 py-1 text-xs font-medium uppercase tracking-wide text-white"
              >
                Хит
              </span>
              <div class="aspect-square overflow-hidden">
                <img
                  :src="product.image"
                  :alt="product.alt"
                  class="h-full w-full object-cover"
                  loading="lazy"
                />
              </div>
              <h3
                class="mt-5 font-display text-xl font-semibold text-coal transition-colors duration-200 group-hover:text-olive"
              >
                {{ product.name }}
              </h3>
              <p class="mt-1 text-sm leading-relaxed text-warmgray">{{ product.description }}</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>
