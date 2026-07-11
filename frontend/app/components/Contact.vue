<script setup lang="ts">
// Секция «Контакты»: информация слева, кнопка маршрута вместо iframe-карты справа
const { contacts } = useSiteData()
</script>

<template>
  <section id="contact" class="scroll-mt-20 bg-milk pb-24 lg:pb-[120px]">
    <div class="mx-auto max-w-7xl px-4 sm:px-8">
      <h2 class="text-center font-display text-4xl font-semibold text-coal lg:text-[48px]">
        Контакты
      </h2>

      <div class="mt-16 grid gap-10 lg:grid-cols-2">
        <!-- Информация -->
        <div class="flex flex-col justify-center border border-sand p-8 lg:p-12">
          <div class="font-display text-lg text-coal">{{ contacts.address }}</div>
          <div class="mt-3 text-base text-warmgray">{{ contacts.hours }}</div>
          <a
            :href="contacts.phoneHref"
            class="mt-6 inline-block text-2xl font-medium text-olive transition-colors hover:text-olive-dark"
          >
            {{ contacts.phone }}
          </a>
        </div>

        <!-- Вместо карты — кнопка построения маршрута в Яндекс.Картах -->
        <div class="flex flex-col items-center justify-center gap-6 bg-sand p-8 text-center lg:p-12">
          <svg class="h-12 w-12 text-olive" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
          </svg>
          <p class="max-w-xs text-sm leading-relaxed text-text-soft">
            Мы находимся в пяти минутах от центра Пригородного. Парковка — напротив входа.
          </p>
          <a
            :href="contacts.routeUrl"
            target="_blank"
            rel="noopener"
            class="inline-flex h-14 items-center justify-center bg-olive px-10 text-sm font-medium uppercase tracking-wide text-white transition-colors duration-200 hover:bg-olive-dark"
          >
            Построить маршрут
          </a>
        </div>
      </div>
    </div>
  </section>
</template>
