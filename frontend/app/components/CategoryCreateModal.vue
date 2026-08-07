<script setup lang="ts">
const emit = defineEmits<{ close: []; created: [] }>()

const visible = ref(true)
const close = () => {
  visible.value = false
}
useModalLifecycle(close)

const name = ref('')
const isSubmitting = ref(false)
const error = ref('')

const submit = async () => {
  error.value = ''
  isSubmitting.value = true
  try {
    await $fetch('/api/categories', {
      method: 'POST',
      body: { category_name: name.value }
    })
    emit('created')
    close()
  } catch {
    error.value = 'Не удалось создать категорию — возможно, такое имя уже занято.'
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
        <div v-if="visible" class="card w-full max-w-md p-8">
          <div class="flex items-start justify-between">
            <h2 class="font-display text-2xl font-semibold text-coal">Новая категория</h2>
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
              Название категории
              <input
                v-model="name"
                type="text"
                required
                autofocus
                class="input-field mt-1 block w-full"
              />
            </label>

            <p v-if="error" class="text-sm text-terra">{{ error }}</p>

            <button type="submit" :disabled="isSubmitting" class="btn-primary w-full">
              {{ isSubmitting ? 'Создаём…' : 'Создать категорию' }}
            </button>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
