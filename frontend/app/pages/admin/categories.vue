<script setup lang="ts">
definePageMeta({ middleware: 'admin-auth', layout: 'admin' })
useHead({ title: 'Категории — Админка' })

interface CategoryDTO {
  id: string
  name: string
}

const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined
const { data: categories, refresh } = await useFetch<CategoryDTO[]>('/api/categories', {
  headers
})

const newCategoryName = ref('')
const isSubmitting = ref(false)
const error = ref('')

const createCategory = async () => {
  error.value = ''
  isSubmitting.value = true
  try {
    await $fetch('/api/categories', {
      method: 'POST',
      body: { category_name: newCategoryName.value }
    })
    newCategoryName.value = ''
    await refresh()
  } catch {
    error.value = 'Не удалось создать категорию.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div>
    <span class="kicker">Меню</span>
    <h1 class="font-display text-3xl font-semibold text-coal">Категории</h1>

    <form class="card mt-8 flex flex-wrap items-end gap-4 p-6" @submit.prevent="createCategory">
      <label class="min-w-[240px] flex-1 text-sm font-medium text-coal">
        Название категории
        <input v-model="newCategoryName" type="text" required class="input-field mt-1 block w-full" />
      </label>
      <button type="submit" :disabled="isSubmitting" class="btn-primary px-6 py-2">
        {{ isSubmitting ? 'Добавляем…' : 'Добавить' }}
      </button>
    </form>
    <p v-if="error" class="mt-2 text-sm text-terra">{{ error }}</p>

    <ul class="mt-10 space-y-3">
      <li
        v-for="category in categories"
        :key="category.id"
        class="card flex items-center justify-between px-5 py-4 transition-shadow duration-200 hover:shadow-md"
      >
        <span class="font-medium text-coal">{{ category.name }}</span>
      </li>
      <li v-if="!categories?.length" class="card px-5 py-8 text-center text-warmgray">
        Категорий пока нет — добавь первую формой выше.
      </li>
    </ul>
  </div>
</template>
