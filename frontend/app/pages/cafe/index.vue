<script setup lang="ts">
// Страница меню кафе: категории и товары приходят с бэкенда через /api-прокси.

interface CategoryDTO {
  id: string
  name: string
}

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

interface ProductListResponseDTO {
  total_count: number
  count: number
  products: ProductListItemDTO[]
}

useHead({
  title: 'Меню кафе — Мясная деревня'
})

const { data: categories } = await useFetch<CategoryDTO[]>('/api/categories')
const { data: productList } = await useFetch<ProductListResponseDTO>('/api/products', {
  query: { limit: 100, offset: 0 }
})

// Поиск по названию + фильтр по категории
const searchQuery = ref('')
const selectedCategoryId = ref<string | null>(null)
const normalizedQuery = computed(() => searchQuery.value.trim().toLowerCase())

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategoryId.value = null
}

// Группировка отфильтрованных товаров по категории для вывода секциями меню
const productsByCategory = computed(() => {
  const map = new Map<string, ProductListItemDTO[]>()
  for (const product of productList.value?.products ?? []) {
    if (normalizedQuery.value && !product.name.toLowerCase().includes(normalizedQuery.value)) continue
    const list = map.get(product.category_id) ?? []
    list.push(product)
    map.set(product.category_id, list)
  }
  return map
})

// Категории для рендера: с активным фильтром — только выбранная;
// при поиске — только те, где что-то нашлось (не показываем пустые секции)
const visibleCategories = computed(() => {
  const all = categories.value ?? []
  const bySelection = selectedCategoryId.value
    ? all.filter((category) => category.id === selectedCategoryId.value)
    : all
  if (!normalizedQuery.value) return bySelection
  return bySelection.filter((category) => (productsByCategory.value.get(category.id)?.length ?? 0) > 0)
})

const isFiltering = computed(() => Boolean(normalizedQuery.value || selectedCategoryId.value))
const hasVisibleProducts = computed(() =>
  visibleCategories.value.some((category) => (productsByCategory.value.get(category.id)?.length ?? 0) > 0)
)

const addingProductId = ref<string | null>(null)

const handleAddToCart = async (productId: string) => {
  addingProductId.value = productId
  try {
    await addToCart(productId)
  } finally {
    addingProductId.value = null
  }
}
</script>

<template>
  <div>
    <Header />

    <main class="pt-20">
      <!-- Заголовок страницы -->
      <section class="bg-sand py-16 lg:py-24">
        <div class="mx-auto max-w-7xl px-4 text-center sm:px-8">
          <h1 class="font-display text-4xl font-semibold text-coal lg:text-[56px]">
            Меню кафе
          </h1>
          <p class="mx-auto mt-4 max-w-xl text-base leading-relaxed text-text-soft">
            Блюда из мяса нашего производства и десерты собственного кондитера.
          </p>
        </div>
      </section>

      <!-- Поиск и фильтр по категориям -->
      <div
        v-if="categories?.length"
        class="sticky top-20 z-30 border-b border-sand bg-milk/95 py-4 backdrop-blur-sm"
      >
        <div class="mx-auto flex max-w-7xl flex-col gap-4 px-4 sm:px-8 lg:flex-row lg:items-center">
          <label class="relative block w-full lg:max-w-xs">
            <span class="sr-only">Поиск по меню</span>
            <svg
              class="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-warmgray"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Найти блюдо…"
              class="input-field h-11 w-full rounded-full bg-white pl-10 pr-3"
            />
          </label>

          <div class="flex gap-2 overflow-x-auto pb-1 lg:pb-0" role="group" aria-label="Фильтр по категориям">
            <button
              type="button"
              class="h-11 shrink-0 whitespace-nowrap rounded-full px-4 text-sm font-medium uppercase tracking-wide transition-all duration-200"
              :class="
                selectedCategoryId === null
                  ? 'bg-olive text-white shadow-sm'
                  : 'border border-coal/20 bg-white text-coal hover:border-olive hover:shadow-sm'
              "
              @click="selectedCategoryId = null"
            >
              Все
            </button>
            <button
              v-for="category in categories"
              :key="category.id"
              type="button"
              class="h-11 shrink-0 whitespace-nowrap rounded-full px-4 text-sm font-medium uppercase tracking-wide transition-all duration-200"
              :class="
                selectedCategoryId === category.id
                  ? 'bg-olive text-white shadow-sm'
                  : 'border border-coal/20 bg-white text-coal hover:border-olive hover:shadow-sm'
              "
              @click="selectedCategoryId = category.id"
            >
              {{ category.name }}
            </button>
          </div>
        </div>
      </div>

      <!-- Меню по категориям -->
      <section class="bg-milk py-16 lg:py-24">
        <div class="mx-auto max-w-7xl px-4 sm:px-8">
          <p v-if="!categories?.length" class="text-center text-warmgray">
            Меню скоро появится.
          </p>

          <div v-else-if="isFiltering && !hasVisibleProducts" class="text-center text-warmgray">
            <p>Ничего не нашлось.</p>
            <button type="button" class="mt-3 text-olive underline" @click="resetFilters">
              Сбросить фильтры
            </button>
          </div>

          <div v-for="category in visibleCategories" :key="category.id" class="mb-16 last:mb-0">
            <h2 class="font-display text-3xl font-semibold text-coal">
              {{ category.name }}
            </h2>

            <p
              v-if="!productsByCategory.get(category.id)?.length"
              class="mt-4 text-sm text-warmgray"
            >
              В этой категории пока нет позиций.
            </p>

            <div v-else class="mt-8 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <ProductCard
                v-for="(product, i) in productsByCategory.get(category.id)"
                :key="product.id"
                :product="product"
                :adding="addingProductId === product.id"
                :index="i"
                @add="handleAddToCart"
              />
            </div>
          </div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>
