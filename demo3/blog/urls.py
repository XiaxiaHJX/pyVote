from django.conf.urls import include,url
from . import views
from . import feed

app_name='blog'
urlpatterns = [

    url(r'^detail/(\d+)/$',views.detail,name='detail'),
    url(r'^archives/(\d+)/(\d+)/$',views.archives,name='archives'),
    url(r'^category/(\d+)/$',views.category,name='category'),
    url(r'^tag/(\d+)/$',views.tag,name='tag'),
    url(r'^rss/$',feed.BlogFeed(),name='rss'),
    url(r'^contacts/$',views.Contacts.as_view(),name='contacts'),
    # url(r'^contacts/$',views.contacts,name='contacts'),
    url(r'^addads/$', views.Ads.as_view(), name='addads'),
    url(r'^$',views.index,name='index'),


]