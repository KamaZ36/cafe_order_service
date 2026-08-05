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
  // Навигация: якоря ведут на секции лендинга, «Кафе» — на отдельную страницу меню
  const nav: { label: string; anchor?: string; to?: string }[] = [
    { label: 'Производство', anchor: 'production' },
    { label: 'Кафе', to: '/cafe' },
    { label: 'Магазин', anchor: 'shop' },
    { label: 'Контакты', anchor: 'contact' }
  ]

  const contacts = {
    phone: '+7 (920) 412-46-83',
    phoneHref: 'tel:+79204124683',
    address: 'Воронежская обл., пгт. Грибановский, ул. Советская, 208',
    hours: 'Ежедневно с 08:00 до 18:00',
    // Ссылка на Яндекс.Карты для кнопки «Построить маршрут»
    routeUrl:
      'https://yandex.ru/maps/?text=' +
      encodeURIComponent('Воронежская обл., пгт. Грибановский, ул. Советская, 208')
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
      description: 'Сочная свиная котлета и свежие овощи',
      image: '/images/cafe/burger.jpg',
      alt: 'Чёрный бургер со свиной котлетой, томатами и салатом'
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
      name: 'Дрогобычская колбаса',
      description: 'Полукопчёная колбаса по галицкому рецепту с чесноком и крупным шпиком',
      image: '/images/shop/vetchina.jpg',
      alt: 'Дрогобычская колбаса, нарезанная ломтиками',
      hit: true
    },
    {
      name: 'Лонганиза',
      description: 'Тонкие сыровяленые колбаски с пряностями',
      image: '/images/shop/kolbaski.jpg',
      alt: 'Колбаски лонганиза на доске'
    },
    {
      name: 'Колбаса из говядины',
      description: 'Сыровяленая, из отборной говядины',
      image: '/images/shop/syrovyalenaya.jpg',
      alt: 'Сыровяленая говяжья колбаса в разрезе'
    },
    {
      name: 'Деревенская',
      description: 'Полукопчёная колбаса, копчение на натуральной щепе',
      image: '/images/shop/polukopchenaya.jpg',
      alt: 'Кольца полукопчёной колбасы «Деревенская»'
    },
    {
      name: 'Докторская',
      description: 'Классическая варёная колбаса с нежной текстурой',
      image: '/images/shop/varenaya.jpg',
      alt: 'Варёная колбаса «Докторская», нарезанная ломтиками'
    }
  ]

  return { nav, contacts, dishes, products }
}

// Плавный скролл к секции по id (используется в шапке и hero)
export const scrollToSection = (id: string) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
