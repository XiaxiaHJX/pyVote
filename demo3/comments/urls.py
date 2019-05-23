from django.conf.urls import include,url
from . import views


app_name='comments'

urlpatterns=[
        url('^comment/(\d+)$',views.comment,name='comment')
]