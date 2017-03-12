from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^index$', views.index, name='index'),
        url(r'^about$', views.about, name='about'),
        url(r'^detail/(?P<item_id>\d+)/$', views.detail, name='detail'),
        url(r'^newitem$', views.newitem, name='newitem'),
        url(r'^suggestions$', views.suggestions, name='suggestions'),
        url(r'^search$', views.searchlib, name='search'),
        url(r'^login$', views.user_login, name='login'),
        url(r'^logout$', views.user_logout, name='logout'),
        url(r'^myitems$', views.myitems, name='myitems'),
        url(r'^register$', views.register, name='register'),
        url(r'^base', views.base, name='base'),
        ]

