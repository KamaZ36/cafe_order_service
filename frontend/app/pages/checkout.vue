<script setup lang="ts">
// Оформление заказа: время самовывоза, комментарий, при необходимости —
// подтверждение телефона (тот же код send/verify, что и в LoginModal).

useHead({ title: 'Оформление заказа — Мясная деревня' })

const user = useCurrentUser()
const cart = useCart()

const hasPhone = computed(() => Boolean(user.value?.phone_number))

// Подтверждение телефона
const phoneStep = ref<'phone' | 'code'>('phone')
const phoneNumber = ref('')
const code = ref('')
const phoneError = ref('')
const isSendingCode = ref(false)
const isVerifyingCode = ref(false)
const isPhoneValid = computed(() => /^\+7\d{10}$/.test(phoneNumber.value))

const sendCode = async () => {
  phoneError.value = ''
  isSendingCode.value = true
  try {
    await $fetch('/api/users/phone/code', {
      method: 'POST',
      body: { phone_number: phoneNumber.value }
    })
    phoneStep.value = 'code'
  } catch {
    phoneError.value = 'Не удалось отправить код. Попробуйте ещё раз.'
  } finally {
    isSendingCode.value = false
  }
}

const verifyCode = async () => {
  phoneError.value = ''
  isVerifyingCode.value = true
  try {
    await $fetch('/api/users/phone/login', {
      method: 'POST',
      body: { phone_number: phoneNumber.value, code: code.value }
    })
    await Promise.all([fetchCurrentUser(), fetchCart()])
  } catch {
    phoneError.value = 'Неверный код.'
  } finally {
    isVerifyingCode.value = false
  }
}

// Оформление заказа: самовывоз всегда "сегодня или завтра", вводить дату
// незачем — просим только время, а дату довычисляем сами (если выбранное
// время уже прошло — значит это на завтра).
const desiredTimeInput = ref('')
const comment = ref('')
const orderError = ref('')
const isSubmitting = ref(false)
const orderPlaced = ref(false)

const pad = (value: number) => String(value).padStart(2, '0')

onMounted(() => {
  // Дефолт — через 30 минут от текущего момента, округлённый до 5 минут,
  // чтобы поле не было пустым и не заставляло гадать разумное время
  const suggested = new Date(Date.now() + 30 * 60_000)
  suggested.setMinutes(Math.ceil(suggested.getMinutes() / 5) * 5, 0, 0)
  desiredTimeInput.value = `${pad(suggested.getHours())}:${pad(suggested.getMinutes())}`
})

const resolvedDesiredTime = computed(() => {
  if (!desiredTimeInput.value) return null
  const [hours, minutes] = desiredTimeInput.value.split(':').map(Number)
  const candidate = new Date()
  candidate.setHours(hours, minutes, 0, 0)
  if (candidate.getTime() < Date.now()) {
    candidate.setDate(candidate.getDate() + 1)
  }
  return candidate
})

const desiredTimeHint = computed(() => {
  if (!resolvedDesiredTime.value) return ''
  const isToday = resolvedDesiredTime.value.toDateString() === new Date().toDateString()
  const time = resolvedDesiredTime.value.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
  return `Заберём ${isToday ? 'сегодня' : 'завтра'} в ${time}`
})

const formatPrice = (price: string) => `${Math.round(Number(price))} ₽`

const placeOrder = async () => {
  if (!resolvedDesiredTime.value) return

  orderError.value = ''
  isSubmitting.value = true
  try {
    await $fetch('/api/users/@me/orders/pickup', {
      method: 'POST',
      body: {
        desired_time: resolvedDesiredTime.value.toISOString(),
        comment: comment.value || null
      }
    })
    orderPlaced.value = true
    await fetchCart()
  } catch {
    orderError.value = 'Не удалось оформить заказ. Проверьте время самовывоза.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div>
    <Header />

    <main class="min-h-screen bg-milk pt-32 pb-24">
      <div class="mx-auto max-w-2xl px-4 sm:px-8">
        <h1 class="font-display text-4xl font-semibold text-coal">Оформление заказа</h1>

        <!-- Успех -->
        <div v-if="orderPlaced" class="card mt-10 p-8 text-center">
          <p class="font-display text-2xl font-semibold text-coal">Заказ оформлен!</p>
          <p class="mt-2 text-warmgray">Мы свяжемся с вами, когда заказ будет готов.</p>
          <NuxtLink to="/account" class="btn-primary mt-6 inline-block">
            Мои заказы
          </NuxtLink>
        </div>

        <!-- Пустая корзина -->
        <div v-else-if="!cart?.items.length" class="card mt-10 p-8 text-center text-warmgray">
          Корзина пуста.
          <NuxtLink to="/cafe" class="text-olive underline">Перейти в меню</NuxtLink>
        </div>

        <template v-else>
          <!-- Состав заказа -->
          <div class="card mt-10 p-6">
            <h2 class="font-display text-xl font-semibold text-coal">Ваш заказ</h2>
            <div
              v-for="item in cart.items"
              :key="item.product_id"
              class="mt-4 flex items-center justify-between text-sm"
            >
              <span class="text-coal">{{ item.name }} × {{ item.quantity }}</span>
              <span class="text-warmgray">{{ formatPrice(item.item_total_price) }}</span>
            </div>
            <div
              class="mt-4 flex items-center justify-between border-t border-sand pt-4 text-lg font-semibold text-coal"
            >
              <span>Итого</span>
              <span>{{ formatPrice(cart.total_price) }}</span>
            </div>
          </div>

          <!-- Телефон -->
          <div v-if="!hasPhone" class="card mt-6 p-6">
            <h2 class="font-display text-xl font-semibold text-coal">Телефон</h2>
            <p class="mt-1 text-sm text-warmgray">
              Нужен для связи по заказу — подтвердите кодом из SMS.
            </p>

            <form v-if="phoneStep === 'phone'" class="mt-4" @submit.prevent="sendCode">
              <PhoneInput v-model="phoneNumber" required class="input-field block w-full tabular-nums" />
              <button
                type="submit"
                :disabled="isSendingCode || !isPhoneValid"
                class="btn-primary mt-3 px-6 py-2"
              >
                {{ isSendingCode ? 'Отправляем…' : 'Получить код' }}
              </button>
            </form>

            <form v-else class="mt-4" @submit.prevent="verifyCode">
              <p class="text-sm text-warmgray">Код отправлен на {{ phoneNumber }}</p>
              <input
                v-model="code"
                type="text"
                inputmode="numeric"
                autocomplete="one-time-code"
                required
                class="input-field mt-2 block w-full"
              />
              <button
                type="submit"
                :disabled="isVerifyingCode"
                class="btn-primary mt-3 px-6 py-2"
              >
                {{ isVerifyingCode ? 'Проверяем…' : 'Подтвердить' }}
              </button>
              <button
                type="button"
                class="ml-3 text-sm text-warmgray transition-colors duration-200 hover:text-coal"
                @click="phoneStep = 'phone'"
              >
                Изменить номер
              </button>
            </form>

            <p v-if="phoneError" class="mt-3 text-sm text-terra">{{ phoneError }}</p>
          </div>

          <!-- Детали заказа -->
          <form class="card mt-6 p-6" @submit.prevent="placeOrder">
            <h2 class="font-display text-xl font-semibold text-coal">Детали заказа</h2>

            <label class="mt-4 block text-sm font-medium text-coal">
              Время самовывоза
              <input
                v-model="desiredTimeInput"
                type="time"
                required
                class="input-field mt-1 block w-full"
              />
            </label>
            <p v-if="desiredTimeHint" class="mt-1 text-sm text-warmgray">{{ desiredTimeHint }}</p>

            <label class="mt-4 block text-sm font-medium text-coal">
              Комментарий (необязательно)
              <textarea v-model="comment" rows="2" class="input-field mt-1 block w-full" />
            </label>

            <p v-if="orderError" class="mt-3 text-sm text-terra">{{ orderError }}</p>

            <button type="submit" :disabled="!hasPhone || isSubmitting" class="btn-primary mt-6 w-full">
              {{ isSubmitting ? 'Оформляем…' : 'Подтвердить заказ' }}
            </button>
          </form>
        </template>
      </div>
    </main>

    <Footer />
  </div>
</template>
