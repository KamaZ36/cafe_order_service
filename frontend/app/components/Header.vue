<script setup lang="ts">
// Шапка: прозрачная на старте, при скролле становится белой с тонкой тенью
const { nav } = useSiteData()

const isScrolled = ref(false)
const isMenuOpen = ref(false)

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

// Плавный переход к секции и закрытие мобильного меню
const goTo = (anchor: string) => {
  isMenuOpen.value = false
  scrollToSection(anchor)
}
</script>

<template>
  <header
    class="fixed inset-x-0 top-0 z-50 transition-colors duration-300"
    :class="
      isScrolled || isMenuOpen
        ? 'bg-white/95 shadow-[0_1px_0_0_#E5D9C5,0_4px_16px_rgba(0,0,0,0.06)]'
        : 'bg-transparent'
    "
  >
    <div class="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-8">
      <!-- Текстовый логотип -->
      <a
        href="#top"
        class="font-display text-[28px] font-semibold leading-none transition-colors"
        :class="isScrolled || isMenuOpen ? 'text-coal' : 'text-white'"
        @click.prevent="goTo('top')"
      >
        Мясная деревня
      </a>

      <!-- Навигация: десктоп -->
      <nav class="hidden items-center gap-8 lg:flex" aria-label="Основная навигация">
        <a
          v-for="item in nav"
          :key="item.anchor"
          :href="`#${item.anchor}`"
          class="text-sm font-medium uppercase tracking-wide transition-colors hover:text-terra"
          :class="isScrolled ? 'text-coal' : 'text-white'"
          @click.prevent="goTo(item.anchor)"
        >
          {{ item.label }}
        </a>
      </nav>

      <!-- Кнопка мобильного меню -->
      <button
        type="button"
        class="flex h-11 w-11 items-center justify-center lg:hidden"
        :class="isScrolled || isMenuOpen ? 'text-coal' : 'text-white'"
        :aria-expanded="isMenuOpen"
        aria-label="Открыть меню"
        @click="isMenuOpen = !isMenuOpen"
      >
        <svg v-if="!isMenuOpen" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
        </svg>
        <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" d="M6 18 18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Навигация: мобильное выпадающее меню -->
    <nav
      v-if="isMenuOpen"
      class="border-t border-sand bg-white/95 px-4 pb-6 pt-2 lg:hidden"
      aria-label="Мобильная навигация"
    >
      <a
        v-for="item in nav"
        :key="item.anchor"
        :href="`#${item.anchor}`"
        class="block border-b border-sand py-3 text-sm font-medium uppercase tracking-wide text-coal"
        @click.prevent="goTo(item.anchor)"
      >
        {{ item.label }}
      </a>
    </nav>
  </header>
</template>
