import type { Config } from 'tailwindcss'

// Дизайн-токены проекта «Мясная деревня» (см. ТЗ)
export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        olive: '#556B2F', // основной цвет: кнопки, акценты
        'olive-dark': '#445625', // hover-состояние кнопок
        milk: '#F9F8F6', // фон страницы
        sand: '#E5D9C5', // карточки и секции
        coal: '#2C2A29', // основной текст
        warmgray: '#8C857B', // второстепенный текст
        terra: '#A64B2A', // акцент: цены, бейджи «Хит»
        'text-soft': '#5A5551' // текст абзацев в секции «Производство»
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', 'serif'],
        sans: ['"Albert Sans"', 'sans-serif']
      },
      borderRadius: {
        // Строгий минимализм: скругления 0 или 2px
        DEFAULT: '2px'
      }
    }
  }
}
