# Модуль: `forms.py`

*Сгенерировано: 2026-10-04 23:59:45*

---

<div id="CustomUserCreationForm"></div>

## CustomUserCreationForm

**Тип:** class

**Кратко:** Форма регистрации нового пользователя.

### Полная документация

```python
Форма регистрации нового пользователя.

Использует email вместо username. Включает встроенные поля password1
и password2 (пароль и его подтверждение) из UserCreationForm.

Attributes:
    Meta: Внутренний класс с настройками формы.
```

---

<div id="CustomUserCreationForm.clean_email"></div>

## CustomUserCreationForm.clean_email

**Тип:** method

**Кратко:** Проверяет, что email ещё не занят.

### Полная документация

```python
Проверяет, что email ещё не занят.

Returns:
    str: Email в нижнем регистре.

Raises:
    ValidationError: Если пользователь с таким email уже существует.
```

---

<div id="CustomAuthenticationForm"></div>

## CustomAuthenticationForm

**Тип:** class

**Кратко:** Форма авторизации по email и паролю.

### Полная документация

```python
Форма авторизации по email и паролю.

Переопределяет стандартную AuthenticationForm: поле username
переименовано в email для отображения в шаблоне.
```

---

<div id="CustomUserChangeForm"></div>

## CustomUserChangeForm

**Тип:** class

**Кратко:** Форма редактирования профиля пользователя.

### Полная документация

```python
Форма редактирования профиля пользователя.

Позволяет изменить имя, фамилию, страну и аватар.
Email и пароль через эту форму не редактируются.

Attributes:
    Meta: Внутренний класс с настройками формы.
```

---

<div id="CustomPasswordChangeForm"></div>

## CustomPasswordChangeForm

**Тип:** class

**Кратко:** Форма смены пароля с Bootstrap-стилями.

### Полная документация

```python
Форма смены пароля с Bootstrap-стилями.

Наследуется от стандартной PasswordChangeForm, которая уже содержит
поля old_password, new_password1 и new_password2 с валидацией.
```

---

<div id="CustomPasswordResetForm"></div>

## CustomPasswordResetForm

**Тип:** class

**Кратко:** Форма запроса восстановления пароля с Bootstrap-стилями.

### Полная документация

```python
Форма запроса восстановления пароля с Bootstrap-стилями.
```

---

<div id="Meta"></div>

## Meta

**Тип:** class

**Кратко:** Внутренний класс с настройками формы.

### Полная документация

```python
Внутренний класс с настройками формы.

Attributes:
    model (Model): Модель, с которой связана форма.
    fields (tuple): Список полей, включённых в форму.
    widgets (dict): Словарь с настройками виджетов для полей.
```

---

<div id="clean_email"></div>

## clean_email

**Тип:** function

**Кратко:** Проверяет, что email ещё не занят.

### Полная документация

```python
Проверяет, что email ещё не занят.

Returns:
    str: Email в нижнем регистре.

Raises:
    ValidationError: Если пользователь с таким email уже существует.
```

---

<div id="Meta"></div>

## Meta

**Тип:** class

**Кратко:** Внутренний класс с настройками формы.

### Полная документация

```python
Внутренний класс с настройками формы.

Attributes:
    model (Model): Модель, с которой связана форма.
    fields (tuple): Список полей, доступных для редактирования.
    widgets (dict): Словарь с настройками виджетов для полей.
```

---

