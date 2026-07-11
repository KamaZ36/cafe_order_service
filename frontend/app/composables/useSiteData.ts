// Данные лендинга: навигация, контакты, примеры блюд и продукции.
// Фотографии носят демонстрационный характер.

export interface Dish {
  name: string
  description: string
  image: string
  alt: string
}

export interface Product {
  name: string
  description: string
  image: string
  alt: string
  hit?: boolean
}

export const useSiteData = () => {
  // Якорная навигация по секциям
  const nav = [
    { label: 'Производство', anchor: 'production' },
    { label: 'Кафе', anchor: 'cafe' },
    { label: 'Магазин', anchor: 'shop' },
    { label: 'Контакты', anchor: 'contact' }
  ]

  const contacts = {
    phone: '+7 (999) 123-45-67',
    phoneHref: 'tel:+79991234567',
    address: 'ул. Фермерская, 12, Пригородный',
    hours: 'Ежедневно с 09:00 до 22:00',
    // Ссылка на Яндекс.Карты для кнопки «Построить маршрут»
    routeUrl:
      'https://yandex.ru/maps/?text=' +
      encodeURIComponent('ул. Фермерская, 12, Пригородный')
  }

  // Примеры блюд кафе (демонстрация, не актуальное меню)
  const dishes: Dish[] = [
    {
      name: 'Пицца из печи',
      description: 'Пепперони и «Четыре сыра» на тесте собственного замеса',
      image: '/images/cafe/pizza.jpg',
      alt: 'Пиццы пепперони и четыре сыра на деревянных досках'
    },
    {
      name: 'Бургер на угольной булочке',
      description: 'Котлета из мраморной говядины и свежие овощи',
      image: '/images/cafe/burger.jpg',
      alt: 'Чёрный бургер с говядиной, томатами и салатом'
    },
    {
      name: 'Макаруны ручной работы',
      description: 'Десерт от нашего кондитера — идеально к кофе',
      image: '/images/cafe/macarons.jpg',
      alt: 'Ассорти макарунов на тарелке в зале кафе'
    }
  ]

  // Примеры продукции магазина (демонстрация, не актуальный ассортимент)
  const products: Product[] = [
    {
      name: 'Ветчина домашняя',
      description: 'Классическая ветчина по домашнему рецепту',
      image: '/images/shop/vetchina.jpg',
      alt: 'Домашняя ветчина, нарезанная ломтиками',
      hit: true
    },
    {
      name: 'Колбаски охотничьи',
      description: 'Пикантные вяленые колбаски к закуске',
      image: '/images/shop/kolbaski.jpg',
      alt: 'Охотничьи колбаски на доске'
    },
    {
      name: 'Колбаса сыровяленая',
      description: 'Длительное созревание в камере выдержки',
      image: '/images/shop/syrovyalenaya.jpg',
      alt: 'Сыровяленая колбаса в разрезе'
    },
    {
      name: 'Колбаса полукопчёная',
      description: 'Копчение на натуральной щепе',
      image: '/images/shop/polukopchenaya.jpg',
      alt: 'Кольца полукопчёной колбасы'
    },
    {
      name: 'Колбаса варёная «Деревенская»',
      description: 'Нежная текстура, только натуральные ингредиенты',
      image: '/images/shop/varenaya.jpg',
      alt: 'Варёная колбаса, нарезанная тонкими ломтиками'
    }
  ]

  return { nav, contacts, dishes, products }
}

// Плавный скролл к секции по id (используется в шапке и hero)
export const scrollToSection = (id: string) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
