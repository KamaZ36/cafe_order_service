// Корзина текущей сессии. Мутации (добавление/изменение количества) сами
// перезапрашивают состояние — компоненты просто читают useCart().

export interface CartItemDTO {
  product_id: string
  name: string
  image: string | null
  price: string
  item_total_price: string
  quantity: number
}

export interface CartDTO {
  id: string | null
  total_items: number
  total_price: string
  items: CartItemDTO[]
}

export const useCart = () => useState<CartDTO | null>('cart', () => null)

export const fetchCart = async () => {
  const cart = useCart()
  const headers = import.meta.server ? useRequestHeaders(['cookie']) : undefined

  cart.value = await $fetch<CartDTO>('/api/users/@me/cart', { headers })

  return cart.value
}

export const addToCart = async (productId: string, quantity = 1) => {
  await $fetch('/api/users/@me/cart/items', {
    method: 'POST',
    body: { product_id: productId, quantity }
  })

  // Добавление в корзину может анонимно создать новую сессию — обновляем оба стора
  await Promise.all([fetchCart(), fetchCurrentUser()])
}

export const updateCartItemQuantity = async (productId: string, quantity: number) => {
  if (quantity < 0) return

  await $fetch(`/api/users/@me/cart/items/${productId}/quantity`, {
    method: 'PATCH',
    body: { quantity }
  })

  await fetchCart()
}
