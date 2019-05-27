from django.contrib import admin
from blog.models import Category,Tag,Article,MessageInfo,Ads
# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(MessageInfo)
admin.site.register(Ads)