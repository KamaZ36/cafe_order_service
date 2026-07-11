<template>
  <section id="top" class="relative flex min-h-dvh items-center justify-center overflow-hidden">
    <!-- Фоновое фото (интерьер кафе — специального hero-фото в исходниках нет) -->
    <img
      src="/images/hero.jpg"
      alt="Интерьер кафе «Мясная деревня»"
      class="absolute inset-0 h-full w-full object-cover"
    />
    <!-- Затемняющий оверлей: усилен к низу для читаемости текста -->
    <div class="absolute inset-0 bg-black/20 bg-gradient-to-b from-black/40 via-black/20 to-black/40" />

    <div class="relative z-10 px-4 text-center">
      <h1 class="font-display text-6xl font-semibold text-white sm:text-7xl lg:text-[96px] lg:leading-none">
        Мясная деревня
      </h1>
      <p class="mt-6 text-base uppercase tracking-[4px] text-white sm:text-lg">
        Кафе • Магазин • Своё производство
      </p>
    </div>
  </section>
</template>
