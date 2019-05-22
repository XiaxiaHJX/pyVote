from django import template
from ..models import Article,Category,Tag
register=template.Library()

@register.filter(name='mylower')
def myslicce(value,length):
    result=value[:length]
    return result

@register.simple_tag(name='getcategorys')
def getcategorys():
    return Category.objects.all()

