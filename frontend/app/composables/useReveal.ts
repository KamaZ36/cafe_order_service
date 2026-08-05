// Плавное появление элемента при попадании во вьюпорт (один раз, дальше не следит)
export const useReveal = () => {
  const el = ref<HTMLElement | null>(null)
  const visible = ref(false)

  onMounted(() => {
    if (!el.value) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry?.isIntersecting) {
          visible.value = true
          observer.disconnect()
        }
      },
      { threshold: 0.15 }
    )
    observer.observe(el.value)
    onBeforeUnmount(() => observer.disconnect())
  })

  return { el, visible }
}
