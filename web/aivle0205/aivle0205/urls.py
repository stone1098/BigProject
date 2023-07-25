# urls.py

"""
URL configuration for aivle0205 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/',include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
   
    path('main/', views.main, name='main'),

    
    

    path('post/', include('post.urls')),
    path('repair_cost/', include('repair_cost.urls')),
    path('fault_ratio/', include('fault_ratio.urls')),

    
    path('contact/',include('contact.urls')),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name = 'about'),
    path('account/', views.account, name='account'),
    
    path('test/', views.test_view, name='test'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)