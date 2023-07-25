from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('<int:question_id>/', views.detail, name='detail'),
    path('question/craete/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    # path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    
    # path('reply/create/<int:answer_id>/', views.reply_create, name='reply_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)