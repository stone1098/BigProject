from django.urls import path
from .views import send_email
from . import views
app_name = 'contact'
urlpatterns = [
    path('', views.send_email, name='send_email'),
    
]