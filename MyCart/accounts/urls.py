from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.loginpage,name='login'),
    path('logout',views.logoutpage,name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate,name='activate')
]