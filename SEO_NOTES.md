# SEO-настройка

Основной адрес: https://antonovaoksana.ru/ (подтверждён владельцем).
Русский контент, все разделы, цены, социальные ссылки и сценарии заказа сохранены.
Из видимого текста изменён только H1 по заданию. Description оставлен прежним.

## Изменения

- `index.html`: title, H1, canonical, Open Graph, favicon, Organization JSON-LD,
  раннее подключение Google Fonts с preconnect и display=swap; размеры изображений,
  srcset/sizes, decoding=async и lazy loading ниже первого экрана.
- Главное фото: настоящий img с fetchpriority=high и eager loading. Сохранены
  object-fit:cover, положение изображения и прежний градиент на компьютере и телефоне.
- `styles.css`: удалён @import шрифтов, поддержан прежний размер изображений после
  добавления width/height, фон блока заказа переведён в WebP.
- `assets/optimized/`: адаптивные WebP-копии 32 используемых изображений и manifest.json.
  Оригиналы сохранены. Наибольшие варианты: 8 794 230 байт вместо 45 702 595 байт
  оригиналов (примерно на 81% меньше). Это сравнение файлов, не замер скорости загрузки.
  На небольших экранах браузер выбирает ещё меньшие варианты.
- `assets/og-cake.jpg`, `assets/favicon-48.png`, `assets/apple-touch-icon.png`,
  `favicon.ico`: превью и значки на основе имеющихся фотографий и логотипа.
- `sitemap.xml`: единственная публичная HTML-страница по основному canonical URL.
  Якоря разделов и дубликат index.html не добавлены. Бриф и исходные материалы
  не являются посадочными страницами сайта.
- `robots.txt`: разрешает обход; указывает абсолютный адрес sitemap.
- `CNAME`: сохраняет выбранный собственный домен при публикации GitHub Pages.
- `scripts/optimize_images.py`: повторяемая генерация изображений (Python + Pillow).
  Зависимости для работы самого сайта не добавлены; script.js не изменён.

## Домен и публикация

При проверке 21 сентября 2026 GitHub Pages вернул 301 с адреса
https://makuninalexandr35-ship-it.github.io/antonova-oksana/ на http://antonovaoksana.ru/.
Локальная проверка HTTPS завершилась ошибкой доверия к сертификату. Это необходимо
перепроверить после настройки сертификата; причина ошибки на сервере не установлена.

1. Проверить DNS и Custom domain в Settings → Pages, дождаться сертификата и включить
   Enforce HTTPS. Не публиковать метаданные как завершённую настройку до доступности
   https://antonovaoksana.ru/ с корректным сертификатом.
2. Опубликовать изменения. Проверить ответы 200 для главной, sitemap.xml, robots.txt,
   favicon.ico и OG-изображения на HTTPS-домене; HTTP должен перенаправлять на HTTPS.
3. На собственном домене файл должен находиться по адресу
   https://antonovaoksana.ru/robots.txt. Копия по пути
   /antonova-oksana/robots.txt НЕ управляет обходом hostname github.io.
   Для github.io нужен файл в корне hostname, управляемый отдельным пользовательским
   репозиторием Pages. Не менять правила всего hostname ради одного проекта.
4. Если потребуется вернуться к проектному URL GitHub Pages, согласованно изменить
   canonical, og:url, og:image, JSON-LD (@id, url, logo), sitemap и Sitemap в robots.txt.
   Относительные ссылки на CSS, JS, изображения и favicon работают и в подкаталоге.

## Google Search Console

После публикации подтвердить владение antonovaoksana.ru (доменное свойство через DNS),
отправить https://antonovaoksana.ru/sitemap.xml и проверить главную через URL Inspection.
Запросить индексирование, проверить выбранный Google canonical и отчёты индексирования
и Core Web Vitals. Эти действия требуют доступа владельца и не выполнялись локально.

Разметка Organization содержит только имеющиеся сведения: название, Москва, телефон,
логотип, Telegram, Instagram, два VK-профиля, Threads и контакт WhatsApp.
Адрес, часы работы, рейтинги и отзывы не добавлены. Bakery/LocalBusiness можно
рассматривать только после получения реального публичного адреса.

Справка: [правила robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt),
[Organization](https://schema.org/Organization).

## Проверки

`python scripts/check_seo.py` проверяет метаданные, JSON-LD, 33 img и их srcset,
реальные размеры файлов, локальные ссылки и якоря, согласованность sitemap, robots и CNAME.
Проверка выполнена успешно. Дополнительно сравнены с исходной версией все ссылки,
русский текст body (кроме заданного H1), H2/H3, семантические разделы и alt.
Проверены первый экран при ширине 1440 и 390 px, кадрирование hero и отсутствие
горизонтального переполнения. В журнале браузера ошибок не обнаружено.
Google Rich Results Test, полевые Core Web Vitals и доступность новых файлов на
рабочем домене нужно проверять после публикации и настройки HTTPS.
