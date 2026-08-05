export interface OrderItemDTO {
  product_id: string
  name: string
  price_at_order: string
  item_total_price: string
  quantity: number
}

export interface OrderDTO {
  id: string
  order_number: string
  status: 'PENDING' | 'CONFIRMED' | 'READY' | 'COMPLETED' | 'CANCELLED'
  order_type: 'PICKUP' | 'DELIVERY'
  desired_time: string
  total_amount: string
  comment: string | null
  created_at: string
  items: OrderItemDTO[]
  customer_phone_number: string | null
  cancel_reason: string | null
}

export interface OrderListDTO {
  total_count: number
  count: number
  orders: OrderDTO[]
}
