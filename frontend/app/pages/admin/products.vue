<script setup lang="ts">
definePageMeta({ middleware: 'admin-auth', layout: 'admin' })
useHead({ title: 'Товары — Админка' })

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

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: categories } = await useFetch<CategoryDTO[]>('/api/categories', { headers })
const { data: productList, refresh } = await useFetch<ProductListResponseDTO>(
  '/api/products',
  { query: { limit: 100, offset: 0 }, headers }
)

// Та же группировка по категориям, что и в меню кафе, — секции совпадают
// с тем, что видит клиент
const productsByCategory = computed(() => {
  const map = new Map<string, ProductListItemDTO[]>()
  for (const product of productList.value?.products ?? []) {
    const list = map.get(product.category_id) ?? []
    list.push(product)
    map.set(product.category_id, list)
  }
  return map
})

const isCreateModalOpen = ref(false)

const editingProductId = ref<string | null>(null)

const onProductCreated = async () => {
  await refresh()
}

const onProductUpdated = async () => {
  await refresh()
}

const deleteProduct = async (id: string) => {
  if (!confirm('Удалить товар?')) return
  await $fetch(`/api/products/${id}`, { method: 'DELETE' })
  await refresh()
}
</script>

<template>
  <div>
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <span class="kicker">Меню</span>
        <h1 class="font-display text-3xl font-semibold text-coal">Товары</h1>
      </div>
      <button type="button" class="btn-primary px-6 py-2" @click="isCreateModalOpen = true">
        Добавить товар
      </button>
    </div>

    <p v-if="!categories?.length" class="card mt-8 px-5 py-8 text-center text-warmgray">
      Сначала добавь хотя бы одну категорию — товар не к чему будет привязать.
    </p>

    <template v-else>
      <p
        v-if="!productList?.products.length"
        class="card mt-8 px-5 py-8 text-center text-warmgray"
      >
        Товаров пока нет — добавь первый кнопкой выше.
      </p>

      <div v-for="category in categories" v-else :key="category.id" class="mt-12 first:mt-8">
        <h2 class="font-display text-2xl font-semibold text-coal">
          {{ category.name }}
          <span class="ml-1 text-base font-normal text-warmgray">
            ({{ productsByCategory.get(category.id)?.length ?? 0 }})
          </span>
        </h2>

        <p
          v-if="!productsByCategory.get(category.id)?.length"
          class="mt-4 text-sm text-warmgray"
        >
          В этой категории пока нет позиций.
        </p>

        <div v-else class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <AdminProductCard
            v-for="product in productsByCategory.get(category.id)"
            :key="product.id"
            :product="product"
            @edit="editingProductId = $event"
            @delete="deleteProduct"
          />
        </div>
      </div>
    </template>

    <ProductCreateModal
      v-if="isCreateModalOpen"
      :categories="categories ?? []"
      @close="isCreateModalOpen = false"
      @created="onProductCreated"
    />

    <ProductEditModal
      v-if="editingProductId"
      :product-id="editingProductId"
      :categories="categories ?? []"
      @close="editingProductId = null"
      @updated="onProductUpdated"
    />
  </div>
</template>
