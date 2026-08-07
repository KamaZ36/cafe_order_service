<script setup lang="ts">
interface Tab {
  key: string
  label: string
  count?: number | null
}

const props = defineProps<{
  tabs: Tab[]
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [key: string]
}>()

function selectTab(key: string) {
  emit('update:modelValue', key)
}

function onKeydown(event: KeyboardEvent) {
  const keys = props.tabs.map((tab) => tab.key)
  const index = keys.indexOf(props.modelValue)
  let nextIndex: number | null = null

  if (event.key === 'ArrowRight') nextIndex = (index + 1) % keys.length
  else if (event.key === 'ArrowLeft') nextIndex = (index - 1 + keys.length) % keys.length
  else if (event.key === 'Home') nextIndex = 0
  else if (event.key === 'End') nextIndex = keys.length - 1

  if (nextIndex === null) return

  event.preventDefault()
  const key = keys[nextIndex]!
  selectTab(key)
  const target = event.currentTarget as HTMLElement | null
  const tabEl = target
    ?.closest('[role="tablist"]')
    ?.querySelector<HTMLElement>(`#admin-tab-${key}`)
  tabEl?.focus()
}
</script>

<template>
  <div class="flex gap-1 overflow-x-auto border-b border-sand" role="tablist" aria-label="Разделы">
    <button
      v-for="tab in tabs"
      :id="`admin-tab-${tab.key}`"
      :key="tab.key"
      type="button"
      role="tab"
      :aria-selected="modelValue === tab.key"
      :aria-controls="`admin-tabpanel-${tab.key}`"
      :tabindex="modelValue === tab.key ? 0 : -1"
      class="relative inline-flex min-h-11 items-center gap-2 whitespace-nowrap px-4 text-sm font-semibold text-warmgray transition-colors duration-150 hover:text-coal focus-visible:outline focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-terra"
      :class="{
        'text-coal after:absolute after:inset-x-3 after:-bottom-px after:h-0.5 after:rounded-t after:bg-terra':
          modelValue === tab.key
      }"
      @click="selectTab(tab.key)"
      @keydown="onKeydown"
    >
      {{ tab.label }}
      <span
        v-if="tab.count !== null && tab.count !== undefined"
        class="min-w-[22px] rounded-full px-1.5 py-0.5 text-center text-xs font-bold tabular-nums"
        :class="modelValue === tab.key ? 'bg-terra/10 text-terra' : 'bg-sand text-warmgray'"
      >
        {{ tab.count }}
      </span>
    </button>
  </div>
</template>
