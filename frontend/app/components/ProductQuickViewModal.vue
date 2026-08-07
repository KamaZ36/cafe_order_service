<script setup lang="ts">
interface ProductDetailsDTO {
  id: string
  name: string
  description: string
  weight: string
  composition: string | null
  category_id: string
  image: string | null
  price: string
  is_available: boolean
  is_popular: boolean
  is_new: boolean
}

const props = defineProps<{ productId: string }>()
const emit = defineEmits<{ close: [] }>()

const visible = ref(true)
const close = () => {
  visible.value = false
}
useModalLifecycle(close)

const isLoading = ref(true)
const loadError = ref(false)
const product = ref<ProductDetailsDTO | null>(null)
const imageLoaded = ref(false)

onMounted(async () => {
  try {
    product.value = await $fetch<ProductDetailsDTO>(`/api/products/${props.productId}`)
  } catch {
    loadError.value = true
  } finally {
    isLoading.value = false
  }
})

const imageUrl = computed(() =>
  product.value?.image ? `/api/uploads/${product.value.image}` : null
)
const formatPrice = (price: string) => `${Math.round(Number(price))} ₽`

const isAdding = ref(false)
const addError = ref('')

const handleAdd = async () => {
  if (!product.value) return
  addError.value = ''
  isAdding.value = true
  try {
    await addToCart(product.value.id)
  } catch {
    addError.value = 'Не удалось добавить в корзину.'
  } finally {
    isAdding.value = false
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
      <!-- Спрингованный вход — та же кривая, что и у "поп" бейджа корзины
           в шапке, чтобы моушен по сайту не рассыпался на разные почерки -->
      <Transition
        enter-active-class="transition duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
        enter-from-class="opacity-0 scale-90 translate-y-3"
        enter-to-class="opacity-100 scale-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 scale-100 translate-y-0"
        leave-to-class="opacity-0 scale-95 translate-y-2"
        appear
      >
        <!-- Крестик снаружи карточки (за верхний правый угол) — так он
             физически не может наехать на контент внутри, независимо от
             раскладки/состояния загрузки -->
        <div v-if="visible" class="relative w-full max-w-2xl">
          <button
            type="button"
            class="absolute -right-2 -top-2 z-20 flex h-11 w-11 items-center justify-center rounded-full bg-white text-coal shadow-lg transition-all duration-150 hover:scale-105 active:scale-90 sm:-right-3 sm:-top-3"
            aria-label="Закрыть"
            @click="close"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <div class="card max-h-[85vh] overflow-y-auto">
            <p v-if="isLoading" class="p-10 text-center text-warmgray">Загружаем…</p>
            <p v-else-if="loadError || !product" class="p-10 text-center text-warmgray">
              Не удалось загрузить товар.
            </p>

            <div v-else class="sm:grid sm:grid-cols-2">
              <div class="relative aspect-square overflow-hidden bg-sand sm:aspect-auto">
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
                <img
                  v-if="imageUrl"
                  :src="imageUrl"
                  :alt="product.name"
                  class="h-full w-full object-cover transition-opacity duration-500 ease-out"
                  :class="imageLoaded ? 'opacity-100' : 'opacity-0'"
                  @load="imageLoaded = true"
                />
              </div>

              <!-- Три чётких яруса — шапка / текст о товаре / действие —
                   каждый отделён тонкой линией, чтобы карточка читалась
                   единым целым, а не набором случайно расставленных блоков -->
              <div class="flex flex-col p-6 sm:p-8">
                <div>
                  <div class="flex items-start justify-between gap-4">
                    <h2 class="font-display text-2xl font-semibold text-coal">
                      {{ product.name }}
                    </h2>
                    <span class="whitespace-nowrap font-display text-xl font-semibold text-terra">
                      {{ formatPrice(product.price) }}
                    </span>
                  </div>
                  <p class="mt-1 text-sm text-warmgray">{{ product.weight }}</p>
                </div>

                <div class="mt-4 space-y-4 border-t border-sand pt-4">
                  <p class="text-sm leading-relaxed text-coal">{{ product.description }}</p>

                  <div v-if="product.composition">
                    <h3 class="text-xs font-semibold uppercase tracking-wide text-warmgray">
                      Состав
                    </h3>
                    <p class="mt-1 text-sm leading-relaxed text-coal">{{ product.composition }}</p>
                  </div>
                </div>

                <div class="mt-6 border-t border-sand pt-6 sm:mt-auto">
                  <p v-if="addError" class="mb-3 text-sm text-terra">{{ addError }}</p>
                  <p v-if="!product.is_available" class="text-sm text-warmgray">
                    Временно недоступно
                  </p>
                  <button
                    v-else
                    type="button"
                    :disabled="isAdding"
                    class="btn-primary w-full"
                    @click="handleAdd"
                  >
                    {{ isAdding ? 'Добавляем…' : 'В корзину' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
