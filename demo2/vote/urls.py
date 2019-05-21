from django.conf.urls import url
from . import views


app_name='vote'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^newpwd/$',views.newpwd,name='newpwd'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^index/$',views.index,name='index'),
    url(r'^option/(\d+)/$',views.option,name='option'),
    url(r'^result/(\d+)/$',views.result,name='result'),

]

