<script setup lang="ts">
definePageMeta({ middleware: 'admin-auth' })

useHead({ title: 'Вход — Админка' })

const phoneNumber = ref('')
const password = ref('')
const error = ref('')
const isSubmitting = ref(false)
const isPhoneValid = computed(() => /^\+7\d{10}$/.test(phoneNumber.value))

const submit = async () => {
  error.value = ''
  isSubmitting.value = true
  try {
    await $fetch('/api/users/login', {
      method: 'POST',
      body: { phone_number: phoneNumber.value, password: password.value }
    })
    await navigateTo('/admin/categories')
  } catch {
    error.value = 'Неверный номер телефона или пароль.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-sand px-4">
    <form class="card w-full max-w-sm p-8 shadow-xl" @submit.prevent="submit">
      <span class="kicker">Персонал</span>
      <h1 class="font-display text-2xl font-semibold text-coal">Вход в админку</h1>

      <label class="mt-6 block text-sm font-medium text-coal">
        Телефон
        <PhoneInput v-model="phoneNumber" required class="input-field mt-1 block w-full tabular-nums" />
      </label>

      <label class="mt-4 block text-sm font-medium text-coal">
        Пароль
        <input v-model="password" type="password" required class="input-field mt-1 block w-full" />
      </label>

      <p v-if="error" class="mt-4 text-sm text-terra">{{ error }}</p>

      <button
        type="submit"
        :disabled="isSubmitting || !isPhoneValid"
        class="btn-primary mt-6 w-full"
      >
        {{ isSubmitting ? 'Входим…' : 'Войти' }}
      </button>
    </form>
  </div>
</template>
