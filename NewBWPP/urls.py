"""NewBWPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from main import views as main_views
from django.contrib.auth.views import login,logout
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',  main_views.index,  name='index'),
    url(r'^mail/(?P<mail_id>[0-9]+)$', main_views.mailpage,  name='mail_page'),
    url(r'^new/$',main_views.Mail,name='new_mail'),
    url(r'^login/$',login,{'template_name':  'login.html'},  name='login'),
    url(r'^register/$',main_views.register,name='register'),
    url(r'^logout/$', logout,{'next_page': '/login'},  name='logout'),
    url(r'^user/$',main_views.user, name='user'),
    url(r'^take/(?P<mail_id>[0-9]+)$',main_views.take, name='take'),
    url(r'^get/(?P<mail_id>[0-9]+)$',main_views.get, name='get')
]
