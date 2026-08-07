<script setup lang="ts">
// Пока не подключён боевой мерчант ЮKassa, оплата подтверждается прямо
// здесь кнопкой «Оплатить». Дальше это станет открытием paymentUrl в новой
// вкладке (window.open) — сам заказ уже создан, дизайн модалки под это готов.
const props = defineProps<{ orderId: string }>()
const emit = defineEmits<{ close: []; paid: [] }>()

const visible = ref(true)
const close = () => {
  visible.value = false
}
useModalLifecycle(close)

const isPaying = ref(false)
const error = ref('')

const pay = async () => {
  error.value = ''
  isPaying.value = true
  try {
    await $fetch(`/api/users/@me/orders/${props.orderId}/simulate-payment`, {
      method: 'POST'
    })
    emit('paid')
    close()
  } catch {
    error.value = 'Не удалось подтвердить оплату. Попробуйте ещё раз.'
  } finally {
    isPaying.value = false
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
        <div v-if="visible" class="card relative w-full max-w-md p-8 text-center">
          <button
            type="button"
            class="absolute right-3 top-3 flex h-11 w-11 items-center justify-center rounded-full text-warmgray transition-all duration-150 hover:bg-coal/5 hover:text-coal active:scale-90"
            aria-label="Закрыть"
            @click="close"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <span class="kicker">Оплата</span>
          <h2 class="font-display text-2xl font-semibold text-coal">Осталось оплатить</h2>
          <p class="mt-2 text-sm text-warmgray">
            Заказ появится в работе у кафе сразу после оплаты.
          </p>

          <p v-if="error" class="mt-4 text-sm text-terra">{{ error }}</p>

          <button
            type="button"
            :disabled="isPaying"
            class="btn-primary mt-6 w-full"
            @click="pay"
          >
            {{ isPaying ? 'Оплачиваем…' : 'Оплатить' }}
          </button>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
