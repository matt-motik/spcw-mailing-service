# SkyPro Модуль Django. Курсовой проект: Сервис управления рассылками

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1+-green.svg)](https://www.djangoproject.com/)
[![Ruff](https://img.shields.io/badge/Ruff-0.16+-purple.svg)](https://docs.astral.sh/ruff/)

Курсовой проект сервиса управления рассылками на Django с Bootstrap-вёрсткой.


## 🚀 Возможности программы

Проект представляет собой сервис управления рассылками, написанный на Python с применением фреймворка Django.
- **Главная страница** со статистикой: всего рассылок, активные, уникальные получатели
- **Управление получателями** (клиентами) — CRUD через формы с валидацией
- **Управление сообщениями** — CRUD через формы с валидацией
- **Управление рассылками** — CRUD через формы с валидацией
- **Динамический статус рассылки** — «Создана», «Запущена», «Завершена» через `update_status()`
- **Валидация дат рассылки** — `start_time` не в прошлом, `start_time` раньше `end_time`
- **Ручной запуск рассылки** через веб-интерфейс и management command
- **История попыток** отправки со статусом и ответом почтового сервера
- **Batch-создание попыток** через `bulk_create()`
- **Статистика по рассылкам** — количество успешных/неуспешных попыток
- **Регистрация пользователей** с подтверждением пароля
- **Активация аккаунта** по email через токен
- **Авторизация** по email и паролю
- **Восстановление пароля** по email
- **Выход из системы** через POST-форму
- **Просмотр и редактирование профиля** пользователя
- **Смена пароля** пользователя
- **Роли и группы прав**: «Пользователь», «Менеджер»
- **Разграничение прав** на страницах и в админ-панели
- **Кеширование** серверное (Redis) и клиентское (`Cache-Control`)
- **Адаптивная вёрстка** с Bootstrap 5
- **Админ-панель** для управления рассылками, клиентами, сообщениями и пользователями

## 📋 Содержание

- [Технологии](#технологии)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Роли и права](#роли-и-права)
- [Разработка](#разработка)
  - [Структура проекта](#структура-проекта)
  - [Линтеры и форматирование](#линтеры)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

<div id="технологии"></div>

## Технологии

| Компонент   | Технология |
|-------------|------------|
| **Язык**        | Python 3.14 |
| **Фреймворк**   | Django 6.1 |
| **База данных** | PostgreSQL |
| **ORM**         | Django ORM |
| **Кеширование** | Redis |
| **Вёрстка**     | Bootstrap 5 |
| **Иконки**      | Bootstrap Icons |
| **Управление зависимостями** | uv |
| **Линтинг**     | Ruff |
| **Типизация**   | MyPy |
| **Pre-commit**  | pre-commit |


<div id="установка"></div>

## Установка

```bash
git clone https://github.com/matt-motik/spcw-mailing-service.git
cd spcw-mailing-service
uv sync --with dev,lint
```

### Redis

Установите и запустите Redis (для кеширования):

```bash
# Manjaro / Arch
sudo pacman -S redis
sudo systemctl enable --now redis

# Проверка
redis-cli ping  # PONG
```

Затем:

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

<div id="конфигурация"></div>

## ⚙️ Конфигурация
### Переменные окружения

Скопируй `.env.example` в `.env` и настройте:

```bash
cp .env.example .env
```
| Переменная             | Описание                  | По умолчанию             |
|------------------------|---------------------------|--------------------------|
| **SECRET_KEY**         | Секретный ключ Django     | -                        |
| **DEBUG**              | Режим отладки             | True                     |
| **ALLOWED_HOSTS**      | Разрешённые хосты         | localhost,127.0.0.1      |
| **DB_NAME**            | Имя базы данных PostgreSQL| -                        |
| **DB_USER**            | Пользователь PostgreSQL   | -                        |
| **DB_PASSWORD**        | Пароль PostgreSQL         | -                        |
| **DB_HOST**            | Хост PostgreSQL           | -                        |
| **DB_PORT**            | Порт PostgreSQL           | 5432                     |
| **EMAIL_USE_CONSOLE**  | Письма в консоль (dev)    | True                     |
| **EMAIL_HOST_USER**    | Логин для email           | -                        |
| **EMAIL_HOST_PASSWORD**| Пароль приложения         | -                        |
| **DEFAULT_FROM_EMAIL** | Email отправителя         | noreply@example.com      |
| **USE_CACHES**         | Включить кеширование      | False                    |
| **REDIS_LOCATION**     | Адрес Redis               | redis://127.0.0.1:6379/0 |
| **PASSWORD_RESET_TIMEOUT** | Время жизни токена сброса пароля, сек | 86400        |

<div id="использование"></div>

## 💻 Использование

### Запуск программы

```bash
uv run python manage.py runserver
```
Открыть в браузере
http://127.0.0.1:8000/

### 🌐 URL-маршруты

| URL                                 | Описание                                      |
|-------------------------------------|-----------------------------------------------|
| `/`                                 | Главная страница (статистика)                 |
| `/recipients/`                      | Список получателей                            |
| `/recipients/create/`               | Добавление получателя                         |
| `/recipients/<id>/`                 | Детали получателя                             |
| `/recipients/<id>/update/`          | Редактирование получателя                     |
| `/recipients/<id>/delete/`          | Удаление получателя                           |
| `/messages/`                        | Список сообщений                              |
| `/messages/create/`                 | Добавление сообщения                          |
| `/messages/<id>/`                   | Детали сообщения                              |
| `/messages/<id>/update/`            | Редактирование сообщения                      |
| `/messages/<id>/delete/`            | Удаление сообщения                            |
| `/mailings/`                        | Список рассылок                               |
| `/mailings/create/`                 | Добавление рассылки                           |
| `/mailings/<id>/`                   | Детали рассылки                               |
| `/mailings/<id>/update/`            | Редактирование рассылки                       |
| `/mailings/<id>/delete/`            | Удаление рассылки                             |
| `/mailings/<id>/send/`              | Ручной запуск рассылки                        |
| `/mailings/<id>/disable/`           | Отключение рассылки (менеджер)                |
| `/statistics/`                      | Статистика по рассылкам пользователя          |
| `/users/register/`                  | Регистрация                                   |
| `/users/login/`                     | Вход                                          |
| `/users/logout/`                    | Выход                                         |
| `/users/activate/<uidb64>/<token>/` | Активация аккаунта по email                   |
| `/users/password/reset/`            | Восстановление пароля                         |
| `/users/profile/`                   | Просмотр профиля                              |
| `/users/profile/edit/`              | Редактирование профиля                        |
| `/users/password/change/`           | Смена пароля                                  |
| `/users/`                           | Список пользователей (менеджер)               |

## 📦 Управление данными

```bash
# Очистка БД
uv run python manage.py dell_all

# Загрузка тестовых данных из фикстур
uv run python manage.py seed_db

# Отправка рассылок по требованию
uv run python manage.py run_mailings

# Создание групп и выдача ролей
uv run python manage.py create_user_group
uv run python manage.py create_manager_group
uv run python manage.py add_manager --email=manager@example.com --password=secret123
```

## 👤 Админ-панель

```bash
# Создание суперпользователя
uv run python manage.py createsuperuser
```
Админка доступна по адресу: /admin

Зарегистрированные модели: Recipient, Message, Mailing, MailingAttempt, CustomUser

<div id="роли-и-права"></div>

## 👥 Роли и права

Права выдаются через группы. Пользователь с ролью получает `is_staff` и работает в админ-панели в пределах прав своей группы.

| Группа | Права |
|--------|-------|
| **Пользователь** | Создание, просмотр, редактирование и удаление своих клиентов, сообщений и рассылок. Просмотр статистики по своим рассылкам |
| **Менеджер** | Просмотр всех клиентов, сообщений и рассылок. Просмотр списка пользователей. Блокировка пользователей. Отключение рассылок |
| **Суперпользователь** | Полный доступ ко всем разделам |

Права на страницах сайта:

- получателей, сообщения и рассылки создаёт любой авторизованный пользователь;
- редактирует и удаляет только владелец;
- менеджер видит все данные, но не редактирует чужие;
- менеджер может блокировать пользователей и отключать рассылки;
- статистика доступна только по своим рассылкам.

<div id="разработка"></div>

## Разработка
<div id="структура-проекта"></div>

### Структура проекта
<!-- СЕКЦИЯ_AUTO_STRUCTURE: СТАРТ -->
<details>
<summary>📁 Структура проекта (развернуть)</summary>

*Этот раздел генерируется автоматически.*

```text
spcw-mailing-service/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── mixins.py
│   ├── settings.py
│   ├── urls.py
│   ├── validators.py
│   └── wsgi.py
├── mailing/
│   ├── fixtures/
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── templates/
│   │   └── mailing/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── management/
│   │   └── commands/
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── managers.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── include/
│   │   ├── footer.html
│   │   └── navbar.html
│   └── base.html
├── static/
│   ├── css/
│   │   ├── font/
│   │   │   ├── fonts/
│   │   │   │   ├── bootstrap-icons.woff
│   │   │   │   └── bootstrap-icons.woff2
│   │   │   ├── bootstrap-icons.css
│   │   │   └── bootstrap-icons.min.css
│   │   ├── bootstrap.min.css
│   │   └── bootstrap.min.css.map
│   └── js/
│       ├── bootstrap.bundle.min.js
│       ├── bootstrap.bundle.min.js.map
│       └── navigation.js
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
```

</details>
<!-- СЕКЦИЯ_AUTO_STRUCTURE: КОНЕЦ -->


<div id="линтеры"></div>

### 🔍 Линтеры и форматирование

Проект использует `ruff` для линтинга и форматирования, `mypy` для проверки типов.

### Проверка кода

```bash
# Линтинг
uv run ruff check mailing/ config/ users/

# Автоисправление ошибок
uv run ruff check --fix mailing/ config/ users/

# Форматирование
uv run ruff format mailing/ config/ users/

# Проверка типов
uv run mypy mailing/ config/ users/
```
### Pre-commit hooks
```bash
# Установить hooks (выполняется автоматически перед каждым коммитом)
uv run pre-commit install

# Проверить все файлы вручную
uv run pre-commit run --all-files
```

<!-- СЕКЦИЯ_AUTO_API: СТАРТ -->
<details>
<summary>📚 Документация API (развернуть)</summary>

*Этот раздел генерируется автоматически из docstring.*

| Модуль | Функция/Класс | Краткое описание |
|--------|---------------|------------------|
| *(заполняется автоматически)* | | |

> 📘 **Полная документация** с примерами и описанием параметров доступна в папке [`docs/api`](docs/api).
</details>
<!-- СЕКЦИЯ_AUTO_API: КОНЕЦ -->

<div id="to-do"></div>

## To do

- [x] Структура проекта, `pyproject.toml`, `README.md`, `.gitignore`, uv, линтеры
- [x] Виртуальное окружение, установка зависимостей через uv
- [ ] Инициализация Django-проекта
- [ ] Приложение mailing с URL-роутингом
- [ ] Модели `Recipient`, `Message`, `Mailing`, `MailingAttempt`
- [ ] Миграции и регистрация в админке
- [ ] CRUD получателей, сообщений и рассылок на CBV
- [ ] Валидация дат рассылки (`start_time`, `end_time`)
- [ ] Динамический статус рассылки через `update_status()`
- [ ] Сервис `send_mailing()` с batch-созданием попыток
- [ ] Management command `run_mailings`
- [ ] Главная страница со статистикой
- [ ] Приложение users с URL-роутингом
- [ ] Кастомная модель `CustomUser` на базе `AbstractUser` с email как `USERNAME_FIELD`
- [ ] Кастомный менеджер `CustomUserManager`
- [ ] Регистрация с подтверждением email
- [ ] Активация аккаунта по email через токен
- [ ] Авторизация по email и паролю
- [ ] Выход из системы через POST-форму
- [ ] Восстановление пароля по email
- [ ] Просмотр и редактирование профиля
- [ ] Смена пароля
- [ ] Роли и группы прав: «Пользователь», «Менеджер»
- [ ] Ограничение доступа: пользователь — только своё, менеджер — read-only ко всем
- [ ] Блокировка пользователей менеджером
- [ ] Отключение рассылок менеджером
- [ ] Статистика по успешным/неуспешным попыткам
- [ ] Кеширование серверное (Redis)
- [ ] Кеширование клиентское (`Cache-Control`)
- [ ] Инвалидация кеша через сигналы
- [ ] Проверить линтеры (`ruff`, `mypy`)
- [ ] Финальная вычитка документации и обновление README
- [ ] `readme_gen.py` под новый проект

## Команда проекта

- Matvey Bakirov — [mabakirov@gmail.com](mailto:mabakirov@gmail.com) — Back-End Engineer
