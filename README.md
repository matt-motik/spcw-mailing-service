# SkyPro Модуль Django. Курсовой проект: Сервис управления рассылками BlastMail

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1+-green.svg)](https://www.djangoproject.com/)
[![Ruff](https://img.shields.io/badge/Ruff-0.16+-purple.svg)](https://docs.astral.sh/ruff/)

Курсовой проект сервиса управления рассылками на Django с Bootstrap-вёрсткой.

**BMA — Blast Mail Agency. Взрывной охват вашей аудитории.**


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
uv sync --group dev --group lint
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
| `/mailings/<id>/enable/`            | Включение рассылки (менеджер)                 |
| `/statistics/`                      | Статистика по рассылкам пользователя          |
| `/users/register/`                  | Регистрация                                   |
| `/users/login/`                     | Вход                                          |
| `/users/logout/`                    | Выход                                         |
| `/users/activate/<uidb64>/<token>/` | Активация аккаунта по email                   |
| `/users/password/reset/`            | Восстановление пароля                         |
| `/users/profile/`                   | Просмотр профиля                              |
| `/users/profile/edit/`              | Редактирование профиля                        |
| `/users/password/change/`           | Смена пароля                                  |


## 📦 Управление данными

```bash
# Создание групп
uv run python manage.py create_user_group
uv run python manage.py create_manager_group

# Создание менеджера
uv run python manage.py add_manager --email=manager@example.com --password=secret123

# Создание суперпользователя
uv run python manage.py addsu --email=admin@example.com --password=secret123

# Отправка активных рассылок
uv run python manage.py run_mailings
```

## 👤 Админ-панель
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
<summary>📁 Структура проекта (развёрнуть)</summary>

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
│   ├── management/
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── add_manager.py
│   │   │   ├── create_manager_group.py
│   │   │   ├── create_user_group.py
│   │   │   └── run_mailings.py
│   │   └── __init__.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_message_owner_recipient_owner.py
│   │   ├── 0003_mailing_is_disabled.py
│   │   └── __init__.py
│   ├── templates/
│   │   └── mailing/
│   │       ├── index.html
│   │       ├── mailing_confirm_delete.html
│   │       ├── mailing_detail.html
│   │       ├── mailing_form.html
│   │       ├── mailing_list.html
│   │       ├── message_confirm_delete.html
│   │       ├── message_detail.html
│   │       ├── message_form.html
│   │       ├── message_list.html
│   │       ├── recipient_confirm_delete.html
│   │       ├── recipient_detail.html
│   │       ├── recipient_form.html
│   │       ├── recipient_list.html
│   │       └── statistics.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
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
├── templates/
│   ├── include/
│   │   ├── footer.html
│   │   └── navbar.html
│   └── base.html
├── users/
│   ├── management/
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   └── addsu.py
│   │   └── __init__.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── templates/
│   │   └── users/
│   │       ├── activation_invalid.html
│   │       ├── activation_sent.html
│   │       ├── logged_out.html
│   │       ├── login.html
│   │       ├── password_change.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset_email.html
│   │       ├── password_reset_form.html
│   │       ├── password_reset_subject.txt
│   │       ├── profile.html
│   │       ├── profile_form.html
│   │       └── register.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── managers.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
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
uv run --group lint ruff check mailing/ config/ users/

# Автоисправление ошибок
uv run --group lint ruff check --fix mailing/ config/ users/

# Форматирование
uv run --group lint ruff format mailing/ config/ users/

# Проверка типов
uv run --group lint mypy mailing/ config/ users/
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
<summary>📚 Документация API (развёрнуть)</summary>

*Этот раздел генерируется автоматически из docstring.*

| Модуль | Функция/Класс | Краткое описание |
|--------|---------------|------------------|
| [**`addsu.py`**](docs/api/addsu.md) | | |
| | [📦 Command](docs/api/addsu.md#Command) | Создаёт суперпользователя с указанными email и паролем. |
| | [⚙️ Command.add_arguments](docs/api/addsu.md#Command.add_arguments) | Добавляет аргументы командной строки. |
| | [⚙️ Command.handle](docs/api/addsu.md#Command.handle) | Создаёт или обновляет суперпользователя. |
| | [🔧 add_arguments](docs/api/addsu.md#add_arguments) | Добавляет аргументы командной строки. |
| | [🔧 handle](docs/api/addsu.md#handle) | Создаёт или обновляет суперпользователя. |
| [**`admin.py`**](docs/api/admin.md) | | |
| | [📦 CustomUserCreationForm](docs/api/admin.md#CustomUserCreationForm) | Форма создания пользователя в админке. |
| | [📦 CustomUserChangeForm](docs/api/admin.md#CustomUserChangeForm) | Форма редактирования пользователя в админке. |
| | [📦 CustomUserAdmin](docs/api/admin.md#CustomUserAdmin) | Настройки административной панели для модели CustomUser. |
| | [⚙️ CustomUserAdmin.get_fieldsets](docs/api/admin.md#CustomUserAdmin.get_fieldsets) | Возвращает fieldsets в зависимости от режима (создание/редактирование). |
| | [📦 Meta](docs/api/admin.md#Meta) | Мета-параметры формы. |
| | [📦 Meta](docs/api/admin.md#Meta) | Мета-параметры формы. |
| | [🔧 get_fieldsets](docs/api/admin.md#get_fieldsets) | Возвращает fieldsets в зависимости от режима (создание/редактирование). |
| [**`apps.py`**](docs/api/apps.md) | | |
| | [📦 UsersConfig](docs/api/apps.md#UsersConfig) | Конфигурация приложения пользователей. |
| [**`forms.py`**](docs/api/forms.md) | | |
| | [📦 CustomUserCreationForm](docs/api/forms.md#CustomUserCreationForm) | Форма регистрации нового пользователя. |
| | [⚙️ CustomUserCreationForm.clean_email](docs/api/forms.md#CustomUserCreationForm.clean_email) | Проверяет, что email ещё не занят. |
| | [📦 CustomAuthenticationForm](docs/api/forms.md#CustomAuthenticationForm) | Форма авторизации по email и паролю. |
| | [📦 CustomUserChangeForm](docs/api/forms.md#CustomUserChangeForm) | Форма редактирования профиля пользователя. |
| | [📦 CustomPasswordChangeForm](docs/api/forms.md#CustomPasswordChangeForm) | Форма смены пароля с Bootstrap-стилями. |
| | [📦 CustomPasswordResetForm](docs/api/forms.md#CustomPasswordResetForm) | Форма запроса восстановления пароля с Bootstrap-стилями. |
| | [📦 Meta](docs/api/forms.md#Meta) | Внутренний класс с настройками формы. |
| | [🔧 clean_email](docs/api/forms.md#clean_email) | Проверяет, что email ещё не занят. |
| | [📦 Meta](docs/api/forms.md#Meta) | Внутренний класс с настройками формы. |
| [**`manage.py`**](docs/api/manage.md) | | |
| | [🔧 main](docs/api/manage.md#main) | Run administrative tasks. |
| [**`managers.py`**](docs/api/managers.md) | | |
| | [📦 CustomUserManager](docs/api/managers.md#CustomUserManager) | Менеджер пользователей, использующий email вместо username. |
| | [⚙️ CustomUserManager.create_user](docs/api/managers.md#CustomUserManager.create_user) | Создаёт и сохраняет обычного пользователя. |
| | [⚙️ CustomUserManager.create_superuser](docs/api/managers.md#CustomUserManager.create_superuser) | Создаёт и сохраняет суперпользователя. |
| | [🔧 create_user](docs/api/managers.md#create_user) | Создаёт и сохраняет обычного пользователя. |
| | [🔧 create_superuser](docs/api/managers.md#create_superuser) | Создаёт и сохраняет суперпользователя. |
| [**`mixins.py`**](docs/api/mixins.md) | | |
| | [📦 BootstrapStyleMixin](docs/api/mixins.md#BootstrapStyleMixin) | Миксин для стилизации полей формы под Bootstrap. |
| [**`models.py`**](docs/api/models.md) | | |
| | [📦 CustomUser](docs/api/models.md#CustomUser) | Кастомная модель пользователя. |
| | [📦 Meta](docs/api/models.md#Meta) | Мета-параметры модели CustomUser. |
| [**`validators.py`**](docs/api/validators.md) | | |
| | [🔧 validate_image_file](docs/api/validators.md#validate_image_file) | Проверяет размер и формат загружаемого изображения. |
| [**`views.py`**](docs/api/views.md) | | |
| | [📦 RegisterView](docs/api/views.md#RegisterView) | Регистрация нового пользователя. |
| | [⚙️ RegisterView.form_valid](docs/api/views.md#RegisterView.form_valid) | Сохраняет пользователя и отправляет письмо с токеном активации. |
| | [⚙️ RegisterView.send_activation_email](docs/api/views.md#RegisterView.send_activation_email) | Отправляет письмо со ссылкой активации. |
| | [📦 ActivationSentView](docs/api/views.md#ActivationSentView) | Страница «проверьте почту» после регистрации. |
| | [⚙️ ActivationSentView.get](docs/api/views.md#ActivationSentView.get) | Отображает страницу с инструкцией. |
| | [📦 ActivateView](docs/api/views.md#ActivateView) | Активация аккаунта по ссылке из письма. |
| | [⚙️ ActivateView.get](docs/api/views.md#ActivateView.get) | Обрабатывает переход по ссылке активации. |
| | [📦 CustomLoginView](docs/api/views.md#CustomLoginView) | Авторизация пользователя по email и паролю. |
| | [📦 CustomLogoutView](docs/api/views.md#CustomLogoutView) | Выход пользователя из системы. |
| | [📦 ProfileDetailView](docs/api/views.md#ProfileDetailView) | Просмотр профиля текущего пользователя. |
| | [⚙️ ProfileDetailView.get_object](docs/api/views.md#ProfileDetailView.get_object) | Возвращает текущего пользователя. |
| | [📦 ProfileUpdateView](docs/api/views.md#ProfileUpdateView) | Редактирование профиля текущего пользователя. |
| | [⚙️ ProfileUpdateView.get_object](docs/api/views.md#ProfileUpdateView.get_object) | Возвращает текущего пользователя. |
| | [⚙️ ProfileUpdateView.form_valid](docs/api/views.md#ProfileUpdateView.form_valid) | Сохраняет профиль и добавляет сообщение об успехе. |
| | [📦 CustomPasswordChangeView](docs/api/views.md#CustomPasswordChangeView) | Смена пароля текущего пользователя. |
| | [⚙️ CustomPasswordChangeView.form_valid](docs/api/views.md#CustomPasswordChangeView.form_valid) | Сохраняет новый пароль и добавляет сообщение об успехе. |
| | [📦 CustomPasswordResetView](docs/api/views.md#CustomPasswordResetView) | Запрос на восстановление пароля. |
| | [📦 CustomPasswordResetDoneView](docs/api/views.md#CustomPasswordResetDoneView) | Страница «письмо отправлено» после запроса на сброс пароля. |
| | [📦 CustomPasswordResetConfirmView](docs/api/views.md#CustomPasswordResetConfirmView) | Установка нового пароля по ссылке из письма. |
| | [📦 CustomPasswordResetCompleteView](docs/api/views.md#CustomPasswordResetCompleteView) | Страница «пароль изменён» после успешного сброса. |
| | [🔧 form_valid](docs/api/views.md#form_valid) | Сохраняет пользователя и отправляет письмо с токеном активации. |
| | [🔧 send_activation_email](docs/api/views.md#send_activation_email) | Отправляет письмо со ссылкой активации. |
| | [🔧 get](docs/api/views.md#get) | Отображает страницу с инструкцией. |
| | [🔧 get](docs/api/views.md#get) | Обрабатывает переход по ссылке активации. |
| | [🔧 get_object](docs/api/views.md#get_object) | Возвращает текущего пользователя. |
| | [🔧 get_object](docs/api/views.md#get_object) | Возвращает текущего пользователя. |
| | [🔧 form_valid](docs/api/views.md#form_valid) | Сохраняет профиль и добавляет сообщение об успехе. |
| | [🔧 form_valid](docs/api/views.md#form_valid) | Сохраняет новый пароль и добавляет сообщение об успехе. |

> 📘 **Полная документация** с примерами и описанием параметров доступна в папке [`docs/api`](docs/api).
</details>
<!-- СЕКЦИЯ_AUTO_API: КОНЕЦ -->

<div id="to-do"></div>

## To do

- [x] Структура проекта, `pyproject.toml`, `README.md`, `.gitignore`, uv, линтеры
- [x] Виртуальное окружение, установка зависимостей через uv
- [x] Инициализация Django-проекта
- [x] Приложение mailing с URL-роутингом
- [x] Модели `Recipient`, `Message`, `Mailing`, `MailingAttempt`
- [x] Миграции и регистрация в админке
- [x] CRUD получателей, сообщений и рассылок на CBV
- [x] Валидация дат рассылки (`start_time`, `end_time`)
- [x] Динамический статус рассылки через `update_status()`
- [x] Сервис `send_mailing()` с batch-созданием попыток
- [x] Management command `run_mailings`
- [x] Главная страница со статистикой
- [x] Приложение users с URL-роутингом
- [x] Кастомная модель `CustomUser` на базе `AbstractUser` с email как `USERNAME_FIELD`
- [x] Кастомный менеджер `CustomUserManager`
- [x] Регистрация с подтверждением email
- [x] Активация аккаунта по email через токен
- [x] Авторизация по email и паролю
- [x] Выход из системы через POST-форму
- [x] Восстановление пароля по email
- [x] Просмотр и редактирование профиля
- [x] Смена пароля
- [x] Роли и группы прав: «Пользователь», «Менеджер»
- [x] Ограничение доступа: пользователь — только своё, менеджер — read-only ко всем
- [x] Блокировка пользователей менеджером
- [x] Отключение рассылок менеджером
- [x] Статистика по успешным/неуспешным попыткам
- [x] Кеширование серверное (Redis)
- [x] Кеширование клиентское (`Cache-Control`)
- [x] Инвалидация кеша через сигналы
- [x] Проверить линтеры (`ruff`, `mypy`)
- [x] Финальная вычитка документации и обновление README


## Команда проекта

- Matvey Bakirov — [mabakirov@gmail.com](mailto:mabakirov@gmail.com) — Back-End Engineer
