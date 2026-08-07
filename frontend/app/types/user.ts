export interface StaffUserListItemDTO {
  id: string
  phone_number: string | null
  role: 'CUSTOMER' | 'ADMIN' | 'MANAGER'
}

export interface StaffUserListDTO {
  total_count: number
  count: number
  users: StaffUserListItemDTO[]
}

export interface UserSessionDTO {
  session_id: string
  ip_address: string | null
  created_at: string
  expires_at: string
}

export interface StaffUserDetailDTO {
  id: string
  phone_number: string | null
  role: 'CUSTOMER' | 'ADMIN' | 'MANAGER'
  sessions: UserSessionDTO[]
}

export interface UserPaymentDTO {
  id: string
  order_id: string
  order_number: string
  amount: number
  status: 'PENDING' | 'CONFIRMED' | 'CANCELED'
  created_at: string
}

export interface StaffUserPaymentListDTO {
  total_count: number
  count: number
  payments: UserPaymentDTO[]
}
