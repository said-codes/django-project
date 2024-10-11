from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    if isinstance(value, BoundField):  # Verificamos si es un campo de formulario
        return value.as_widget(attrs={'class': css_class})
    return value  # Si no es un campo de formulario, lo devolvemos sin cambios
