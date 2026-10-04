# Модуль: `validators.py`

*Сгенерировано: 2026-10-04 23:59:45*

---

<div id="validate_image_file"></div>

## validate_image_file

**Тип:** function

**Кратко:** Проверяет размер и формат загружаемого изображения.

### Полная документация

```python
Проверяет размер и формат загружаемого изображения.

Args:
    image: Загруженный файл изображения.

Raises:
    ValidationError: Если размер больше MAX_IMAGE_SIZE
        или формат не JPG/PNG/WEBP.
```

---

