<script setup lang="ts">
interface CategoryDTO {
  id: string
  name: string
}

const props = defineProps<{ categories: CategoryDTO[] }>()
const emit = defineEmits<{ close: []; created: [] }>()

const visible = ref(true)
const close = () => {
  visible.value = false
}
useModalLifecycle(close)

const isSubmitting = ref(false)
const error = ref('')

const name = ref('')
const description = ref('')
const weight = ref('')
const composition = ref('')
const categoryId = ref(props.categories[0]?.id ?? '')
const price = ref('')
const isAvailable = ref(true)
const isPopular = ref(false)
const isNew = ref(false)
const file = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  file.value = target.files?.[0] ?? null
}

const submit = async () => {
  error.value = ''

  if (!file.value) {
    error.value = 'Выберите фото товара.'
    return
  }

  const formData = new FormData()
  formData.append('name', name.value)
  formData.append('description', description.value)
  formData.append('weight', weight.value)
  formData.append('composition', composition.value)
  formData.append('category_id', categoryId.value)
  formData.append('price', price.value)
  formData.append('is_available', String(isAvailable.value))
  formData.append('is_popular', String(isPopular.value))
  formData.append('is_new', String(isNew.value))
  formData.append('file', file.value)

  isSubmitting.value = true
  try {
    await $fetch('/api/products', { method: 'POST', body: formData })
    emit('created')
    close()
  } catch {
    error.value = 'Не удалось создать товар. Проверьте поля формы.'
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
            <h2 class="font-display text-2xl font-semibold text-coal">Новый товар</h2>
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

          <form class="mt-6 grid gap-4" @submit.prevent="submit">
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

            <label class="text-sm font-medium text-coal">
              Описание
              <textarea v-model="description" required rows="2" class="input-field mt-1 block w-full" />
            </label>

            <label class="text-sm font-medium text-coal">
              Состав
              <textarea
                v-model="composition"
                rows="2"
                placeholder="Говядина, лук, специи…"
                class="input-field mt-1 block w-full"
              />
            </label>

            <div class="grid grid-cols-2 gap-4">
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
            </div>

            <label class="text-sm font-medium text-coal">
              Фото
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                required
                class="mt-2 block w-full text-sm"
                @change="onFileChange"
              />
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
              {{ isSubmitting ? 'Создаём…' : 'Создать товар' }}
            </button>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
