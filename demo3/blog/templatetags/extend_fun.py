from django import template
from ..models import Article,Category,Tag,Ads
register=template.Library()

@register.filter(name='mylower')
def myslicce(value,length):
    result=value[:length]
    return result

@register.simple_tag(name='getcategorys')
def getcategorys():
    return Category.objects.all()

@register.simple_tag
def getlatestarticles(num=3):
    return Article.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def getarchives(num=3):
    re=Article.objects.dates('create_time','month',order='DESC')[:num]
    return re

@register.simple_tag
def gettags():
    return Tag.objects.all()

@register.simple_tag
def getads():
    print(Ads.objects.all())
    return Ads.objects.all()

