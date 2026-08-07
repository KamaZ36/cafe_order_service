<script setup lang="ts">
// Вход по телефону: код из SMS. Если телефон уже привязан к аккаунту —
// бэкенд сам логинит в него, иначе привязывает к текущей сессии.

const emit = defineEmits<{ close: [] }>()

const step = ref<'phone' | 'code'>('phone')
const phoneNumber = ref('')
const code = ref('')
const error = ref('')
const isSubmitting = ref(false)
const isPhoneValid = computed(() => /^\+7\d{10}$/.test(phoneNumber.value))

// Плавное закрытие: сначала проигрываем transition, реальный emit('close')
// (который убирает компонент из дерева родителя) — после его завершения
const visible = ref(true)
const close = () => {
  visible.value = false
}

useModalLifecycle(close)

const sendCode = async () => {
  error.value = ''
  isSubmitting.value = true
  try {
    await $fetch('/api/users/phone/code', {
      method: 'POST',
      body: { phone_number: phoneNumber.value }
    })
    step.value = 'code'
  } catch {
    error.value = 'Не удалось отправить код. Попробуйте ещё раз.'
  } finally {
    isSubmitting.value = false
  }
}

const verifyCode = async () => {
  error.value = ''
  isSubmitting.value = true
  try {
    await $fetch('/api/users/phone/login', {
      method: 'POST',
      body: { phone_number: phoneNumber.value, code: code.value }
    })
    await Promise.all([fetchCurrentUser(), fetchCart()])
    close()
  } catch {
    error.value = 'Неверный код.'
  } finally {
    isSubmitting.value = false
  }
}

const changePhone = () => {
  step.value = 'phone'
  code.value = ''
  error.value = ''
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
        <div v-if="visible" class="card w-full max-w-sm p-8 shadow-xl">
          <div class="flex items-start justify-between">
            <h2 class="font-display text-2xl font-semibold text-coal">
              {{ step === 'phone' ? 'Вход по телефону' : 'Введите код' }}
            </h2>
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

          <form v-if="step === 'phone'" class="mt-6" @submit.prevent="sendCode">
            <label class="block text-sm font-medium text-coal">
              Телефон
              <PhoneInput
                v-model="phoneNumber"
                required
                class="input-field mt-1 block w-full tabular-nums"
              />
            </label>

            <p v-if="error" class="mt-3 text-sm text-terra">{{ error }}</p>

            <button
              type="submit"
              :disabled="isSubmitting || !isPhoneValid"
              class="btn-primary mt-6 w-full"
            >
              {{ isSubmitting ? 'Отправляем…' : 'Получить код' }}
            </button>
          </form>

          <form v-else class="mt-6" @submit.prevent="verifyCode">
            <p class="text-sm text-warmgray">Код отправлен на {{ phoneNumber }}</p>

            <label class="mt-4 block text-sm font-medium text-coal">
              Код из SMS
              <input
                v-model="code"
                type="text"
                inputmode="numeric"
                autocomplete="one-time-code"
                required
                class="input-field mt-1 block w-full"
              />
            </label>

            <p v-if="error" class="mt-3 text-sm text-terra">{{ error }}</p>

            <button type="submit" :disabled="isSubmitting" class="btn-primary mt-6 w-full">
              {{ isSubmitting ? 'Проверяем…' : 'Войти' }}
            </button>
            <button
              type="button"
              class="mt-3 w-full text-center text-sm text-warmgray transition-colors duration-200 hover:text-coal"
              @click="changePhone"
            >
              Изменить номер
            </button>
          </form>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
