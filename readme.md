## Парсер с интерфейсом на Flask

В качестве примера реализован парсер, записывающий результат работы в БД (PostgreSQL). Далее можно выполнять любые манипуляции с этими данными. 

Часть функционала, требуемого в ТЗ не закончена - будет дополняться.

**Для запуска:**
- клонировать репозиторий
- переименовать .env.example -> .env
- установить зависимости
- запустить app.py

**Эндпойнты:**
- GET /category/parse - выполнить парсинг категорий и подкатегорий
- GET /category - получить список всех категорий (выводится иерархическая структура подкатегорий и товаров, входящих в каждую категорию)
- GET /category/:id - получить категорию по id
- GET /category/:id/parse_products - выполнить парсинг всех товаров для категории

**TODO:**
- логирование
- экспорт в csv
- расширение списка эндпойнтов