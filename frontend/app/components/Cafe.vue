<script setup lang="ts">
// Секция «Кафе»: примеры блюд (демонстрация формата, не актуальное меню)
const { dishes } = useSiteData()
</script>

<template>
  <section id="cafe" class="scroll-mt-20 bg-sand py-24 lg:py-[120px]">
    <div class="mx-auto max-w-7xl px-4 sm:px-8">
      <h2 class="text-center font-display text-4xl font-semibold text-coal lg:text-[48px]">
        Кафе
      </h2>
      <p class="mx-auto mt-4 max-w-xl text-center text-base leading-relaxed text-text-soft">
        Уютный зал, десерты собственного кондитера и блюда из мяса нашего
        производства. Фотографии — примеры того, что готовит наша кухня.
      </p>

      <!-- Атмосферный кадр зала -->
      <img
        src="/images/cafe/hall.jpg"
        alt="Зал кафе: мягкие диваны и столики у окна"
        class="mt-12 h-64 w-full border border-coal/10 object-cover lg:h-96"
        loading="lazy"
      />

      <div class="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="dish in dishes"
          :key="dish.name"
          class="group border border-coal/10 bg-milk"
        >
          <!-- Фото: масштабируется при наведении, обрезка через overflow-hidden -->
          <div class="aspect-square overflow-hidden">
            <img
              :src="dish.image"
              :alt="dish.alt"
              class="h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
              loading="lazy"
            />
          </div>
          <div class="p-6">
            <h3 class="font-display text-2xl font-semibold text-coal">
              {{ dish.name }}
            </h3>
            <p class="mt-2 text-sm leading-relaxed text-warmgray">
              {{ dish.description }}
            </p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
