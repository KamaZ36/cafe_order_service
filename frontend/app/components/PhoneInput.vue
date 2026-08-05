<script setup lang="ts">
// Маскированный ввод телефона: показывает +7 (___) ___-__-__, а наружу
// (v-model) отдаёт нормализованный E.164 вроде +79991234567 — то, что
// ожидает бэкенд. Курсор всегда уводится в конец: для 10-значного номера,
// который обычно не редактируют посередине, это надёжнее, чем считать
// позицию каретки внутри маски.

const model = defineModel<string>({ default: '' })

const digitsOf = (value: string) => value.replace(/\D/g, '').replace(/^7|^8/, '').slice(0, 10)

const format = (digits: string) => {
  if (!digits) return ''
  let out = '+7'
  out += ` (${digits.slice(0, 3)}`
  if (digits.length >= 3) out += ')'
  if (digits.length > 3) out += ` ${digits.slice(3, 6)}`
  if (digits.length > 6) out += `-${digits.slice(6, 8)}`
  if (digits.length > 8) out += `-${digits.slice(8, 10)}`
  return out
}

const displayValue = computed(() => format(digitsOf(model.value)))

const onInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  const digits = digitsOf(input.value)
  model.value = digits ? `+7${digits}` : ''
  nextTick(() => {
    input.value = format(digits)
  })
}
</script>

<template>
  <input
    type="tel"
    inputmode="tel"
    autocomplete="tel"
    placeholder="+7 (___) ___-__-__"
    :value="displayValue"
    @input="onInput"
  />
</template>
