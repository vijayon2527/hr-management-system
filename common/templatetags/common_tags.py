from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, *urls):
    request = context['request']
    if request.resolver_match and request.resolver_match.url_name in urls:
        return 'active'
    return ''
