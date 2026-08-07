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

const isCreateModalOpen = ref(false)

const onCategoryCreated = async () => {
  await refresh()
}

const editingCategoryId = ref<string | null>(null)
const editingName = ref('')
const isRenaming = ref(false)
const renameError = ref('')

const startEditing = (category: CategoryDTO) => {
  editingCategoryId.value = category.id
  editingName.value = category.name
  renameError.value = ''
}

const cancelEditing = () => {
  editingCategoryId.value = null
  renameError.value = ''
}

const renameCategory = async () => {
  if (!editingCategoryId.value) return

  renameError.value = ''
  isRenaming.value = true
  try {
    await $fetch(`/api/categories/${editingCategoryId.value}`, {
      method: 'PATCH',
      body: { category_name: editingName.value }
    })
    editingCategoryId.value = null
    await refresh()
  } catch {
    renameError.value = 'Не удалось переименовать — возможно, такое имя уже занято.'
  } finally {
    isRenaming.value = false
  }
}

const deletingCategoryId = ref<string | null>(null)
const deleteErrorId = ref<string | null>(null)
const deleteErrorMessage = ref('')

const deleteCategory = async (category: CategoryDTO) => {
  if (!confirm(`Удалить категорию «${category.name}»?`)) return

  deleteErrorId.value = null
  deletingCategoryId.value = category.id
  try {
    await $fetch(`/api/categories/${category.id}`, { method: 'DELETE' })
    await refresh()
  } catch (err: unknown) {
    const errorCode = (err as { data?: { error_code?: string } })?.data?.error_code
    deleteErrorId.value = category.id
    deleteErrorMessage.value =
      errorCode === 'CATEGORY_HAS_PRODUCTS'
        ? 'В категории есть товары — сначала перенеси или удали их.'
        : 'Не удалось удалить категорию.'
  } finally {
    deletingCategoryId.value = null
  }
}
</script>

<template>
  <div>
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <span class="kicker">Меню</span>
        <h1 class="font-display text-3xl font-semibold text-coal">Категории</h1>
      </div>
      <button type="button" class="btn-primary px-6 py-2" @click="isCreateModalOpen = true">
        Добавить
      </button>
    </div>

    <ul class="mt-10 space-y-3">
      <li
        v-for="category in categories"
        :key="category.id"
        class="card px-5 py-4 transition-shadow duration-200 hover:shadow-md"
      >
        <form
          v-if="editingCategoryId === category.id"
          class="flex flex-wrap items-end gap-3"
          @submit.prevent="renameCategory"
        >
          <label class="min-w-[200px] flex-1 text-sm font-medium text-coal">
            Название категории
            <input
              v-model="editingName"
              type="text"
              required
              autofocus
              class="input-field mt-1 block w-full"
            />
          </label>
          <button type="submit" :disabled="isRenaming" class="btn-primary px-4 py-2 text-sm">
            {{ isRenaming ? 'Сохраняем…' : 'Сохранить' }}
          </button>
          <button
            type="button"
            class="px-2 py-2 text-xs font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra"
            @click="cancelEditing"
          >
            Отмена
          </button>
        </form>
        <div v-else class="flex items-center justify-between">
          <span class="font-medium text-coal">{{ category.name }}</span>
          <div class="flex gap-4">
            <button
              type="button"
              class="text-xs font-medium uppercase tracking-wide text-olive transition-colors duration-200 hover:text-olive-dark"
              @click="startEditing(category)"
            >
              Переименовать
            </button>
            <button
              type="button"
              :disabled="deletingCategoryId === category.id"
              class="text-xs font-medium uppercase tracking-wide text-warmgray transition-colors duration-200 hover:text-terra disabled:opacity-50"
              @click="deleteCategory(category)"
            >
              {{ deletingCategoryId === category.id ? 'Удаляем…' : 'Удалить' }}
            </button>
          </div>
        </div>
        <p v-if="editingCategoryId === category.id && renameError" class="mt-2 text-sm text-terra">
          {{ renameError }}
        </p>
        <p v-if="deleteErrorId === category.id" class="mt-2 text-sm text-terra">
          {{ deleteErrorMessage }}
        </p>
      </li>
      <li v-if="!categories?.length" class="card px-5 py-8 text-center text-warmgray">
        Категорий пока нет — добавь первую кнопкой выше.
      </li>
    </ul>

    <CategoryCreateModal
      v-if="isCreateModalOpen"
      @close="isCreateModalOpen = false"
      @created="onCategoryCreated"
    />
  </div>
</template>
