from django.conf.urls import url
from . import views


app_name='vote'

urlpatterns=[
    url('^register/$',views.register,name='register'),
    url('^login/$',views.login,name='login'),
    url('^logout/$',views.logout,name='logout'),
    url('^index/$',views.index,name='index'),
    url('^option/(\d+)/$',views.option,name='option'),
    url('^result/(\d+)/$',views.result,name='result'),

]

