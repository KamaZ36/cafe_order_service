<script setup lang="ts">
interface CategoryDTO {
  id: string
  name: string
}

interface ProductDetailsDTO {
  id: string
  name: string
  description: string
  weight: string
  category_id: string
  image: string | null
  price: string
  is_available: boolean
  is_popular: boolean
  is_new: boolean
}

const props = defineProps<{ productId: string; categories: CategoryDTO[] }>()
const emit = defineEmits<{ close: []; updated: [] }>()

const visible = ref(true)
const close = () => {
  visible.value = false
}
useModalLifecycle(close)

const isLoading = ref(true)
const isSubmitting = ref(false)
const error = ref('')

const name = ref('')
const description = ref('')
const weight = ref('')
const categoryId = ref('')
const price = ref('')
const isAvailable = ref(true)
const isPopular = ref(false)
const isNew = ref(false)
const currentImage = ref<string | null>(null)
const file = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

onMounted(async () => {
  try {
    const product = await $fetch<ProductDetailsDTO>(`/api/products/${props.productId}`)
    name.value = product.name
    description.value = product.description
    weight.value = product.weight
    categoryId.value = product.category_id
    price.value = product.price
    isAvailable.value = product.is_available
    isPopular.value = product.is_popular
    isNew.value = product.is_new
    currentImage.value = product.image
  } catch {
    error.value = 'Не удалось загрузить товар.'
  } finally {
    isLoading.value = false
  }
})

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  file.value = target.files?.[0] ?? null
}

const submit = async () => {
  error.value = ''

  const formData = new FormData()
  formData.append('name', name.value)
  formData.append('description', description.value)
  formData.append('weight', weight.value)
  formData.append('category_id', categoryId.value)
  formData.append('price', price.value)
  formData.append('is_available', String(isAvailable.value))
  formData.append('is_popular', String(isPopular.value))
  formData.append('is_new', String(isNew.value))
  if (file.value) formData.append('file', file.value)

  isSubmitting.value = true
  try {
    await $fetch(`/api/products/${props.productId}`, { method: 'PATCH', body: formData })
    emit('updated')
    close()
  } catch {
    error.value = 'Не удалось сохранить изменения. Проверьте поля формы.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
    appear
    @after-leave="emit('close')"
  >
    <div
      v-if="visible"
      class="fixed inset-0 z-[70] flex items-center justify-center bg-coal/50 px-4 backdrop-blur-sm"
      @click.self="close"
    >
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
        appear
      >
        <div v-if="visible" class="card max-h-[90vh] w-full max-w-lg overflow-y-auto p-8">
          <div class="flex items-start justify-between">
            <h2 class="font-display text-2xl font-semibold text-coal">Редактировать товар</h2>
            <button
              type="button"
              class="flex h-8 w-8 items-center justify-center rounded-full text-xl leading-none text-warmgray transition-colors duration-200 hover:bg-coal/5 hover:text-coal"
              aria-label="Закрыть"
              @click="close"
            >
              ✕
            </button>
          </div>

          <p v-if="isLoading" class="mt-6 text-sm text-warmgray">Загружаем…</p>

          <form v-else class="mt-6 grid gap-4" @submit.prevent="submit">
            <label class="text-sm font-medium text-coal">
              Название
              <input v-model="name" type="text" required class="input-field mt-1 block w-full" />
            </label>

            <label class="text-sm font-medium text-coal">
              Категория
              <select v-model="categoryId" required class="input-field mt-1 block w-full">
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </label>

            <label class="text-sm font-medium text-coal">
              Описание
              <textarea v-model="description" required rows="2" class="input-field mt-1 block w-full" />
            </label>

            <div class="grid grid-cols-2 gap-4">
              <label class="text-sm font-medium text-coal">
                Вес/объём
                <input v-model="weight" type="text" required class="input-field mt-1 block w-full" />
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
            </div>

            <label class="text-sm font-medium text-coal">
              Фото
              <img
                v-if="currentImage && !file"
                :src="`/api/uploads/${currentImage}`"
                alt=""
                class="mt-2 h-24 w-24 rounded-lg object-cover"
              />
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="mt-2 block w-full text-sm"
                @change="onFileChange"
              />
              <span class="mt-1 block text-xs font-normal text-warmgray">
                Оставь пустым, чтобы не менять текущее фото.
              </span>
            </label>

            <div class="flex flex-wrap gap-6 text-sm text-coal">
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

            <p v-if="error" class="text-sm text-terra">{{ error }}</p>

            <button type="submit" :disabled="isSubmitting" class="btn-primary w-full">
              {{ isSubmitting ? 'Сохраняем…' : 'Сохранить изменения' }}
            </button>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
