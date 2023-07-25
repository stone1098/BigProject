from django.urls import path,include
from . import views
from .views import AuthSmsSendView,SMSVerificationConfirmView
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('update/',views.update, name='update'),
    path('sms/', AuthSmsSendView.as_view(), name='send_sms'),
    path('phone_verification/',views.phone_verification,name='phone_verification'),
    path('sms/check/', SMSVerificationConfirmView.as_view(), name='snscheck'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/', views.delete, name='delete'),
]