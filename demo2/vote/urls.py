from django.conf.urls import url
from . import views

app_name='vote'

urlpatterns=[
    url('^index/$',views.index,name='index'),
    url('^option/(\d+)/$',views.option,name='option'),
    url('^result/(\d+)/$',views.result,name='result')
]

