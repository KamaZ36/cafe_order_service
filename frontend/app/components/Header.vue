<script setup lang="ts">
// Шапка: прозрачная на старте, при скролле становится белой с тонкой тенью
const { nav } = useSiteData()
const route = useRoute()
const user = useCurrentUser()
const cart = useCart()

const isScrolled = ref(false)
const isMenuOpen = ref(false)
const isCartOpen = ref(false)
const isLoginOpen = ref(false)

// Прозрачная шапка с белым текстом рассчитана на тёмный hero-баннер —
// он есть только на главной. На остальных страницах фон под шапкой светлый,
// поэтому там шапка всегда непрозрачная и тёмная, без ожидания скролла.
const isHome = computed(() => route.path === '/')
const isSolid = computed(() => !isHome.value || isScrolled.value || isMenuOpen.value)

// «Войти» — пока нет верифицированного телефона (в т.ч. анонимная сессия
// без телефона), иначе — ссылка в личный кабинет
const isLoggedIn = computed(() => Boolean(user.value?.phone_number))

// ADMIN и MANAGER видят ссылку в свой раздел — админ должен видеть и заказы,
// поэтому ссылка одна на обе роли, без разделения по названию
const isStaff = computed(() => user.value?.role === 'ADMIN' || user.value?.role === 'MANAGER')

const onScroll = () => {
  isScrolled.value = window.scrollY > 40
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})

// Переход к секции лендинга: если мы уже на главной — скролл,
// если на другой странице — сначала переход на главную с якорем
const goTo = (anchor: string) => {
  isMenuOpen.value = false
  if (route.path === '/') {
    scrollToSection(anchor)
  } else {
    navigateTo(`/#${anchor}`)
  }
}

const goHome = () => {
  isMenuOpen.value = false
  if (route.path === '/') {
    scrollToSection('top')
  }
}
</script>

<template>
  <header
    class="fixed inset-x-0 top-0 z-50 transition-colors duration-300"
    :class="
      isSolid
        ? 'bg-white/95 shadow-[0_1px_0_0_#E5D9C5,0_4px_16px_rgba(0,0,0,0.06)]'
        : 'bg-transparent'
    "
  >
    <div class="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-8">
      <!-- Текстовый логотип -->
      <NuxtLink
        to="/"
        class="font-display text-[28px] font-semibold leading-none transition-colors"
        :class="isSolid ? 'text-coal' : 'text-white'"
        @click="goHome"
      >
        Мясная деревня
      </NuxtLink>

      <!-- Навигация: десктоп -->
      <nav class="hidden items-center gap-8 lg:flex" aria-label="Основная навигация">
        <template v-for="item in nav" :key="item.label">
          <NuxtLink
            v-if="item.to"
            :to="item.to"
            class="text-sm font-medium uppercase tracking-wide transition-colors hover:text-terra"
            :class="isSolid ? 'text-coal' : 'text-white'"
            @click="isMenuOpen = false"
          >
            {{ item.label }}
          </NuxtLink>
          <a
            v-else
            :href="`#${item.anchor}`"
            class="text-sm font-medium uppercase tracking-wide transition-colors hover:text-terra"
            :class="isSolid ? 'text-coal' : 'text-white'"
            @click.prevent="goTo(item.anchor!)"
          >
            {{ item.label }}
          </a>
        </template>
      </nav>

      <!-- Корзина, вход/кабинет и кнопка мобильного меню -->
      <div class="flex items-center gap-2">
        <!-- Корзина -->
        <button
          type="button"
          class="relative flex h-11 w-11 items-center justify-center rounded-full transition-colors duration-200"
          :class="isSolid ? 'text-coal hover:bg-coal/5' : 'text-white hover:bg-white/10'"
          aria-label="Открыть корзину"
          @click="isCartOpen = true"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.836l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 1.994-4.708 2.602-7.201.232-.95-.492-1.849-1.47-1.849H5.106M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
          </svg>
          <span
            :key="cart?.total_items ?? 0"
            class="animate-badge-pop absolute right-1 top-1 flex h-4 w-4 items-center justify-center rounded-full text-[10px] font-semibold transition-colors duration-200"
            :class="cart?.total_items ? 'bg-terra text-white' : 'bg-coal/10 text-warmgray'"
          >
            {{ cart?.total_items ?? 0 }}
          </span>
        </button>

        <!-- Кабинет сотрудника: ADMIN и MANAGER, ссылка одна на обе роли -->
        <NuxtLink
          v-if="isStaff"
          to="/admin"
          class="hidden text-sm font-medium uppercase tracking-wide transition-colors hover:text-terra lg:block"
          :class="isSolid ? 'text-coal' : 'text-white'"
        >
          Кабинет сотрудника
        </NuxtLink>

        <!-- Вход / личный кабинет -->
        <NuxtLink
          v-if="isLoggedIn"
          to="/account"
          class="hidden text-sm font-medium uppercase tracking-wide transition-colors hover:text-terra lg:block"
          :class="isSolid ? 'text-coal' : 'text-white'"
        >
          Кабинет
        </NuxtLink>
        <button
          v-else
          type="button"
          class="hidden text-sm font-medium uppercase tracking-wide transition-colors hover:text-terra lg:block"
          :class="isSolid ? 'text-coal' : 'text-white'"
          @click="isLoginOpen = true"
        >
          Войти
        </button>

        <!-- Кнопка мобильного меню -->
        <button
          type="button"
          class="flex h-11 w-11 items-center justify-center rounded-full transition-colors duration-200 lg:hidden"
          :class="isSolid ? 'text-coal hover:bg-coal/5' : 'text-white hover:bg-white/10'"
          :aria-expanded="isMenuOpen"
          aria-label="Открыть меню"
          @click="isMenuOpen = !isMenuOpen"
        >
          <svg class="h-6 w-6 transition-transform duration-300" :class="{ 'rotate-90': isMenuOpen }" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
            <path v-if="!isMenuOpen" stroke-linecap="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
            <path v-else stroke-linecap="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Навигация: мобильное выпадающее меню -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <nav
        v-if="isMenuOpen"
        class="border-t border-sand bg-white/95 px-4 pb-6 pt-2 lg:hidden"
        aria-label="Мобильная навигация"
      >
        <template v-for="item in nav" :key="item.label">
          <NuxtLink
            v-if="item.to"
            :to="item.to"
            class="block border-b border-sand py-3 text-sm font-medium uppercase tracking-wide text-coal"
            @click="isMenuOpen = false"
          >
            {{ item.label }}
          </NuxtLink>
          <a
            v-else
            :href="`#${item.anchor}`"
            class="block border-b border-sand py-3 text-sm font-medium uppercase tracking-wide text-coal"
            @click.prevent="goTo(item.anchor!)"
          >
            {{ item.label }}
          </a>
        </template>

        <NuxtLink
          v-if="isStaff"
          to="/admin"
          class="block border-b border-sand py-3 text-sm font-medium uppercase tracking-wide text-coal"
          @click="isMenuOpen = false"
        >
          Кабинет сотрудника
        </NuxtLink>

        <NuxtLink
          v-if="isLoggedIn"
          to="/account"
          class="block py-3 text-sm font-medium uppercase tracking-wide text-coal"
          @click="isMenuOpen = false"
        >
          Кабинет
        </NuxtLink>
        <button
          v-else
          type="button"
          class="block w-full py-3 text-left text-sm font-medium uppercase tracking-wide text-coal"
          @click="isMenuOpen = false; isLoginOpen = true"
        >
          Войти
        </button>
      </nav>
    </Transition>
  </header>

  <CartDrawer v-if="isCartOpen" @close="isCartOpen = false" />
  <LoginModal v-if="isLoginOpen" @close="isLoginOpen = false" />
</template>
