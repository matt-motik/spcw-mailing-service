"""Общие миксины для форм проекта."""

from typing import Any

from django import forms


class BootstrapStyleMixin(forms.Form):
    """Миксин для стилизации полей формы под Bootstrap."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Навешивает CSS-классы на виджеты полей."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            else:
                css_class = "form-control"
            widget.attrs["class"] = css_class
