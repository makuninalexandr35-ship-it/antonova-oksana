# Состояние проекта

## 2026-09-21 — Инициализация памяти
- Проект: сайт домашней кондитерской Oksana Antonova — Art of Desserts, Москва.
- Архитектура: статические index.html, styles.css, script.js; изображения в assets/.
- Документация: README.md, PROJECT_SPEC.md, SEO_NOTES.md.
- Основной адрес, подтверждённый пользователем: https://antonovaoksana.ru/; записан в canonical и CNAME.
- Выполнено SEO-обновление: title/H1, canonical, Open Graph, favicon, Organization JSON-LD, sitemap.xml, robots.txt.
- Добавлены адаптивные WebP-копии, srcset/sizes, width/height, decoding=async, lazy loading ниже первого экрана.
- Hero переведён из CSS-фона в img с fetchpriority=high; Google Fonts подключены без CSS @import.
- scripts/optimize_images.py генерирует изображения; scripts/check_seo.py проверяет SEO и пути (Python + Pillow).
- На мобильных надпись «Домашняя кондитерская · Москва» поднята на 24 px, размер 14–16 px.
- На мобильных фото торта с лебедями показано целиком: auto height и object-fit:contain.
- В блоке цены пункт 03: «Доставка, самовывоз или курьер»; ниже «Доставка рассчитывается отдельно».
- При инициализации рабочее дерево Git чистое, HEAD c8ac3c8; перечисленные изменения присутствуют в файлах.
- Публикация и актуальное состояние HTTPS после прошлых проверок не подтверждены; перед выводами проверить заново.
- Google Search Console: подтверждение домена, отправка sitemap и запрос индексирования ранее не выполнялись агентом.
- Текущая задача: инициализация FSDB; после завершения ожидать следующую команду пользователя.
