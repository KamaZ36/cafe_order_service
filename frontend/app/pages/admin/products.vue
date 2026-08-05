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

const categoryName = (id: string) =>
  categories.value?.find((category) => category.id === id)?.name ?? '—'

const name = ref('')
const description = ref('')
const weight = ref('')
const categoryId = ref('')
const price = ref('')
const isAvailable = ref(true)
const isPopular = ref(false)
const isNew = ref(false)
const file = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const isSubmitting = ref(false)
const error = ref('')

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  file.value = target.files?.[0] ?? null
}

const resetForm = () => {
  name.value = ''
  description.value = ''
  weight.value = ''
  categoryId.value = ''
  price.value = ''
  isAvailable.value = true
  isPopular.value = false
  isNew.value = false
  file.value = null
  if (fileInput.value) fileInput.value.value = ''
}

const createProduct = async () => {
  error.value = ''

  if (!file.value) {
    error.value = 'Выберите фото товара.'
    return
  }

  const formData = new FormData()
  formData.append('name', name.value)
  formData.append('description', description.value)
  formData.append('weight', weight.value)
  formData.append('category_id', categoryId.value)
  formData.append('price', price.value)
  formData.append('is_available', String(isAvailable.value))
  formData.append('is_popular', String(isPopular.value))
  formData.append('is_new', String(isNew.value))
  formData.append('file', file.value)

  isSubmitting.value = true
  try {
    await $fetch('/api/products', { method: 'POST', body: formData })
    resetForm()
    await refresh()
  } catch {
    error.value = 'Не удалось создать товар. Проверьте поля формы.'
  } finally {
    isSubmitting.value = false
  }
}

const deleteProduct = async (id: string) => {
  if (!confirm('Удалить товар?')) return
  await $fetch(`/api/products/${id}`, { method: 'DELETE' })
  await refresh()
}

const editingProductId = ref<string | null>(null)

const onProductUpdated = async () => {
  await refresh()
}
</script>

<template>
  <div>
    <span class="kicker">Меню</span>
    <h1 class="font-display text-3xl font-semibold text-coal">Товары</h1>

    <form class="card mt-8 grid gap-4 p-6 sm:grid-cols-2" @submit.prevent="createProduct">
      <label class="text-sm font-medium text-coal">
        Название
        <input v-model="name" type="text" required class="input-field mt-1 block w-full" />
      </label>

      <label class="text-sm font-medium text-coal">
        Категория
        <select v-model="categoryId" required class="input-field mt-1 block w-full">
          <option value="" disabled>Выберите категорию</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </label>

      <label class="text-sm font-medium text-coal sm:col-span-2">
        Описание
        <textarea v-model="description" required rows="2" class="input-field mt-1 block w-full" />
      </label>

      <label class="text-sm font-medium text-coal">
        Вес/объём
        <input
          v-model="weight"
          type="text"
          required
          placeholder="200г"
          class="input-field mt-1 block w-full"
        />
      </label>

      <label class="text-sm font-medium text-coal">
        Цена, ₽
        <input
          v-model="price"
          type="number"
          min="0"
          step="0.01"
          required
          class="input-field mt-1 block w-full"
        />
      </label>

      <label class="text-sm font-medium text-coal sm:col-span-2">
        Фото
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          required
          class="mt-1 block w-full text-sm"
          @change="onFileChange"
        />
      </label>

      <div class="flex flex-wrap gap-6 text-sm text-coal sm:col-span-2">
        <label class="flex items-center gap-2">
          <input v-model="isAvailable" type="checkbox" /> В наличии
        </label>
        <label class="flex items-center gap-2">
          <input v-model="isPopular" type="checkbox" /> Хит
        </label>
        <label class="flex items-center gap-2">
          <input v-model="isNew" type="checkbox" /> Новинка
        </label>
      </div>

      <div class="sm:col-span-2">
        <p v-if="error" class="mb-3 text-sm text-terra">{{ error }}</p>
        <button type="submit" :disabled="isSubmitting" class="btn-primary px-6 py-2">
          {{ isSubmitting ? 'Сохраняем…' : 'Добавить товар' }}
        </button>
      </div>
    </form>

    <div class="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="product in productList?.products"
        :key="product.id"
        class="card flex gap-4 p-4 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
        :class="{ 'opacity-60': !product.is_available }"
      >
        <div class="h-16 w-16 shrink-0 overflow-hidden rounded-lg bg-sand">
          <img
            v-if="product.image"
            :src="`/api/uploads/${product.image}`"
            :alt="product.name"
            class="h-full w-full object-cover"
          />
        </div>

        <div class="min-w-0 flex-1">
          <div class="flex items-start justify-between gap-2">
            <h3 class="truncate font-display text-lg font-semibold text-coal">{{ product.name }}</h3>
            <span class="whitespace-nowrap font-display text-lg font-semibold text-terra">
              {{ Math.round(Number(product.price)) }} ₽
            </span>
          </div>
          <p class="text-xs uppercase tracking-wide text-warmgray">
            {{ categoryName(product.category_id) }}
          </p>

          <div class="mt-1 flex flex-wrap gap-1">
            <span
              v-if="!product.is_available"
              class="rounded-full bg-coal/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-warmgray"
            >
              Недоступен
            </span>
            <span
              v-if="product.is_popular"
              class="rounded-full bg-terra/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-terra"
            >
              Хит
            </span>
            <span
              v-if="product.is_new"
              class="rounded-full bg-olive/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-olive-dark"
            >
              Новинка
            </span>
          </div>

          <div class="mt-3 flex gap-4">
            <button
              type="button"
              class="text-xs font-medium uppercase tracking-wide text-olive transition-colors duration-200 hover:text-olive-dark"
              @click="editingProductId = product.id"
            >
              Редактировать
            </button>
            <button
              type="button"
              class="text-xs font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra"
              @click="deleteProduct(product.id)"
            >
              Удалить
            </button>
          </div>
        </div>
      </article>
      <p v-if="!productList?.products.length" class="card px-5 py-8 text-center text-warmgray sm:col-span-2 lg:col-span-3">
        Товаров пока нет — добавь первый формой выше.
      </p>
    </div>

    <ProductEditModal
      v-if="editingProductId"
      :product-id="editingProductId"
      :categories="categories ?? []"
      @close="editingProductId = null"
      @updated="onProductUpdated"
    />
  </div>
</template>
