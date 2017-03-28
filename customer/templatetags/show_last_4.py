from django import template

register = template.Library()


@register.simple_tag()
def show_last_4(qty, *args, **kwargs):
    # you would need to do any localization of the result here
    return "**** **** **** " + qty[-4:]
