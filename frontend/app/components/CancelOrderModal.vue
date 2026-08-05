<script setup lang="ts">
const props = defineProps<{ orderNumber: string }>()
const emit = defineEmits<{ close: []; confirm: [reason: string | null] }>()

const reason = ref('')

const visible = ref(true)
const close = () => {
  visible.value = false
}
useModalLifecycle(close)

const confirmCancel = () => {
  emit('confirm', reason.value.trim() || null)
  close()
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
        <div v-if="visible" class="card w-full max-w-sm p-8">
          <div class="flex items-start justify-between">
            <h2 class="font-display text-2xl font-semibold text-coal">
              Отменить заказ №{{ orderNumber }}?
            </h2>
            <button
              type="button"
              class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xl leading-none text-warmgray transition-colors duration-200 hover:bg-coal/5 hover:text-coal"
              aria-label="Закрыть"
              @click="close"
            >
              ✕
            </button>
          </div>

          <label class="mt-6 block text-sm font-medium text-coal">
            Причина (необязательно)
            <textarea
              v-model="reason"
              rows="3"
              placeholder="Например: клиент не приехал"
              class="input-field mt-1 block w-full"
            />
          </label>

          <div class="mt-6 flex gap-3">
            <button
              type="button"
              class="flex-1 rounded-lg border border-coal/20 px-4 py-3 text-sm font-medium uppercase tracking-wide text-coal transition-colors duration-200 hover:bg-coal/5"
              @click="close"
            >
              Не отменять
            </button>
            <button type="button" class="btn-primary flex-1" @click="confirmCancel">
              Отменить заказ
            </button>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
