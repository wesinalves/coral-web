from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='maskcpf')
def maskcpf(value):
    return f"***{value[4:11]}***" 