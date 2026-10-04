# Модуль: `managers.py`

*Сгенерировано: 2026-10-04 23:59:45*

---

<div id="CustomUserManager"></div>

## CustomUserManager

**Тип:** class

**Кратко:** Менеджер пользователей, использующий email вместо username.

### Полная документация

```python
Менеджер пользователей, использующий email вместо username.
```

---

<div id="CustomUserManager.create_user"></div>

## CustomUserManager.create_user

**Тип:** method

**Кратко:** Создаёт и сохраняет обычного пользователя.

### Полная документация

```python
Создаёт и сохраняет обычного пользователя.

Args:
    email: Email пользователя (используется как идентификатор).
    password: Пароль в открытом виде (будет захеширован).
    **extra_fields: Дополнительные поля модели пользователя.

Returns:
    CustomUser: Созданный пользователь.

Raises:
    ValueError: Если email не передан.
```

---

<div id="CustomUserManager.create_superuser"></div>

## CustomUserManager.create_superuser

**Тип:** method

**Кратко:** Создаёт и сохраняет суперпользователя.

### Полная документация

```python
Создаёт и сохраняет суперпользователя.

Args:
    email: Email пользователя.
    password: Пароль в открытом виде.
    **extra_fields: Дополнительные поля модели пользователя.

Returns:
    CustomUser: Созданный суперпользователь.

Raises:
    ValueError: Если email не передан или не заданы is_staff/is_superuser.
```

---

<div id="create_user"></div>

## create_user

**Тип:** function

**Кратко:** Создаёт и сохраняет обычного пользователя.

### Полная документация

```python
Создаёт и сохраняет обычного пользователя.

Args:
    email: Email пользователя (используется как идентификатор).
    password: Пароль в открытом виде (будет захеширован).
    **extra_fields: Дополнительные поля модели пользователя.

Returns:
    CustomUser: Созданный пользователь.

Raises:
    ValueError: Если email не передан.
```

---

<div id="create_superuser"></div>

## create_superuser

**Тип:** function

**Кратко:** Создаёт и сохраняет суперпользователя.

### Полная документация

```python
Создаёт и сохраняет суперпользователя.

Args:
    email: Email пользователя.
    password: Пароль в открытом виде.
    **extra_fields: Дополнительные поля модели пользователя.

Returns:
    CustomUser: Созданный суперпользователь.

Raises:
    ValueError: Если email не передан или не заданы is_staff/is_superuser.
```

---

