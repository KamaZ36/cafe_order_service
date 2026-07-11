<script setup lang="ts">
// Секция «Наше ремесло»: два блока текст/фото и анимированные счётчики

const stats = [
  { label: 'Натурально' },
  { label: 'Своё производство' },
  { label: 'Без добавок' }
]

// Текущие значения счётчиков (анимируются от 0 до 100)
const counters = ref([0, 0, 0])
const statsBlock = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

// Анимация чисел через requestAnimationFrame с плавным замедлением
const animateCounters = () => {
  const duration = 1400
  const start = performance.now()

  const tick = (now: number) => {
    const progress = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
    counters.value = counters.value.map(() => Math.round(eased * 100))
    if (progress < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

onMounted(() => {
  // Запускаем анимацию один раз, когда блок счётчиков появляется в зоне видимости
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0]?.isIntersecting) {
        animateCounters()
        observer?.disconnect()
      }
    },
    { threshold: 0.4 }
  )
  if (statsBlock.value) observer.observe(statsBlock.value)
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <!-- scroll-mt-20 — отступ под фиксированную шапку при якорном переходе -->
  <section id="production" class="scroll-mt-20 py-24 lg:py-[120px]">
    <div class="mx-auto max-w-7xl px-4 sm:px-8">
      <h2 class="text-center font-display text-4xl font-semibold text-coal lg:text-[48px]">
        Наше ремесло
      </h2>

      <!-- Блок 1: текст слева, фото справа -->
      <div class="mt-16 grid items-center gap-10 lg:grid-cols-2 lg:gap-16">
        <div>
          <h3 class="font-display text-2xl font-semibold text-coal lg:text-3xl">
            Производство полного цикла
          </h3>
          <p class="mt-6 text-lg leading-[1.6] text-text-soft">
            Мы не ферма, а собственное производство полного цикла. Контролируем каждый
            этап: от закупки сырья до разделки, созревания и упаковки. Никаких усилителей
            вкуса — только классические рецепты и натуральные ингредиенты.
          </p>
        </div>
        <img
          src="/images/production_1.jpg"
          alt="Колбасы ручной работы на разделочной доске"
          class="h-72 w-full border border-sand object-cover lg:h-96"
          loading="lazy"
        />
      </div>

      <!-- Блок 2: фото слева, текст справа (чередование через order) -->
      <div class="mt-14 grid items-center gap-10 lg:grid-cols-2 lg:gap-16">
        <img
          src="/images/production_2.jpg"
          alt="Сыровяленая колбаса со специями"
          class="order-last h-72 w-full border border-sand object-cover lg:order-first lg:h-96"
          loading="lazy"
        />
        <div>
          <h3 class="font-display text-2xl font-semibold text-coal lg:text-3xl">
            Ручная работа и выдержка
          </h3>
          <p class="mt-6 text-lg leading-[1.6] text-text-soft">
            Вяжем колбасы вручную, выдерживаем деликатесы в камерах созревания и коптим
            на натуральной щепе. Каждая партия проходит контроль качества, прежде чем
            попасть на витрину магазина и в меню кафе.
          </p>
        </div>
      </div>

      <!-- Счётчики: анимируются при появлении в окне просмотра -->
      <div ref="statsBlock" class="mt-20 grid gap-10 border-y border-sand py-12 sm:grid-cols-3">
        <div v-for="(stat, i) in stats" :key="stat.label" class="text-center">
          <div class="font-display text-5xl font-semibold text-olive lg:text-6xl">
            {{ counters[i] }}%
          </div>
          <div class="mt-2 text-sm uppercase tracking-wide text-warmgray">
            {{ stat.label }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
