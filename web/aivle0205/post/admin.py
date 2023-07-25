from django.contrib import admin
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'create_date')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)