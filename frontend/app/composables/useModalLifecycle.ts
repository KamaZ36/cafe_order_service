// Общее поведение модалок/шторок: закрытие по Esc и блокировка скролла
// страницы, пока открыты. Используется в LoginModal и CartDrawer.
export const useModalLifecycle = (close: () => void) => {
  const onKeydown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') close()
  }

  onMounted(() => {
    document.addEventListener('keydown', onKeydown)
    document.body.style.overflow = 'hidden'
  })

  onBeforeUnmount(() => {
    document.removeEventListener('keydown', onKeydown)
    document.body.style.overflow = ''
  })
}
